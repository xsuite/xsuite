# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2025.                 #
# ######################################### #
import json
import os
import warnings
from multiprocessing import Pool
from pathlib import Path
from pprint import pformat
from typing import Iterator, Optional, Tuple

import xcoll as xc
import xfields as xf
import xobjects as xo
import xtrack as xt
from xcoll.prebuilt_kernel_definitions import XCOLL_ELEMENTS_INIT_DEFAULTS
from xfields.prebuilt_kernel_definitions import XFIELDS_ELEMENTS_INIT_DEFAULTS
from xtrack.general import _print
from xtrack.prebuilt_kernel_definitions import XTRACK_ELEMENTS_INIT_DEFAULTS

import xsuite as xs
from xsuite.kernel_definitions import kernel_definitions, NAME_CLASS_MAP

XSK_PREBUILT_KERNELS_LOCATION = Path(xs.__file__).parent / 'lib'

BEAM_ELEMENTS_INIT_DEFAULTS = XTRACK_ELEMENTS_INIT_DEFAULTS| XFIELDS_ELEMENTS_INIT_DEFAULTS \
                            | XCOLL_ELEMENTS_INIT_DEFAULTS




def save_kernel_metadata(
        module_name: str,
        config: dict,
        tracker_element_classes,
        all_classes,
        location,
):
    location = Path(location)
    out_file = location / f'{module_name}.json'

    kernel_metadata = {
        'config': config.data,
        'tracker_element_classes': [cls._DressingClass.__name__ for cls in tracker_element_classes],
        'classes': [getattr(cls, '_DressingClass', cls).__name__ for cls in all_classes],
        'versions': {
            'xtrack': xt.__version__,
            'xfields': xf.__version__,
            'xcoll': xc.__version__,
            'xobjects': xo.__version__,
        }
    }

    with out_file.open('w') as fd:
        json.dump(kernel_metadata, fd, indent=4)


def enumerate_kernels(verbose=False) -> Iterator[Tuple[str, dict]]:
    """
    Iterate over the prebuilt kernels compatible with the current version of
    xsuite. The first element of the tuple is the name of the kernel module
    and the second is a dictionary with the kernel metadata.
    """
    for kernel_name, _ in kernel_definitions:
        metadata_file = XSK_PREBUILT_KERNELS_LOCATION / f'{kernel_name}.json'

        if not metadata_file.exists():
            continue

        with metadata_file.open('r') as fd:
            kernel_metadata = json.load(fd)

        needed_versions = kernel_metadata['versions']
        have_versions = {
            'xtrack': xt.__version__,
            'xfields': xf.__version__,
            'xcoll': xc.__version__,
            'xobjects': xo.__version__,
        }

        version_mismatch = False
        for package in needed_versions.keys():
            need = needed_versions[package]
            have = have_versions[package]
            if need == have:
                continue

            version_mismatch = True
            if verbose:
                _print(
                    f'Version mismatch for kernel `{kernel_name}`: needs '
                    f'{package}=={need}, but have {package}=={have}.'
                )

        if version_mismatch:
            continue

        yield metadata_file.stem, kernel_metadata


def get_suitable_kernel(
        config: dict,
        tracker_element_classes,
        classes,
        verbose=False,
) -> Optional[Tuple[str, list]]:
    """
    Given a configuration and a list of element classes, return a tuple with
    the name of a suitable prebuilt kernel module together with the list of
    element classes that were used to build it. Set `verbose` to True, to
    obtain a justification of the choice (or lack thereof) on standard output.
    """
    env_var = os.environ.get("XSUITE_PREBUILT_KERNELS")
    if env_var and env_var == '0':
        if verbose:
            print('Skipping the search for a suitable kernel, as the '
                   'environment variable XSUITE_PREBUILT_KERNELS == "0".')
        return

    if os.environ.get("XSUITE_VERBOSE", None) is not None:
        verbose = True

    requested_tracker_class_names = [
        cls._DressingClass.__name__ for cls in tracker_element_classes
    ]
    requested_class_names = [getattr(cls, '_DressingClass', cls).__name__ for cls in classes]

    for module_name, kernel_metadata in enumerate_kernels(verbose=verbose):
        if verbose:
            print(f"==> Considering the precompiled kernel `{module_name}`...")

        if kernel_metadata['config'] != config:
            if verbose:
                lhs = kernel_metadata['config']
                rhs = config
                config_diff = {kk: (lhs.get(kk), rhs.get(kk))
                               for kk in set(lhs.keys()) | set(rhs.keys())
                               if lhs.get(kk) != rhs.get(kk)}
                print(f'The kernel `{module_name}` is unsuitable. Its config '
                      f'(left) and the requested one (right) differ at the '
                      f'following keys:\n'
                      f'{pformat(config_diff)}')
                print(f'Skipping class compatibility check for `{module_name}`.')

            continue

        if verbose:
            print(f'The kernel `{module_name}` has the right config.')

        module_tracker_element_names = kernel_metadata['tracker_element_classes']
        module_class_names = kernel_metadata['classes']

        if not set(requested_tracker_class_names) <= set(module_tracker_element_names):
            if verbose:
                class_diff = set(requested_tracker_class_names) - set(module_tracker_element_names)
                print(f'The kernel `{module_name}` is unsuitable. It does not '
                      f'provide the following requested classes: '
                      f'{", ".join(class_diff)}.')
            continue

        all_class_names = set(module_tracker_element_names) | set(module_class_names)
        if not set(requested_class_names) <= all_class_names:
            if verbose:
                class_diff = set(requested_class_names) - all_class_names
                print(f'The kernel `{module_name}` is unsuitable. It does not '
                      f'provide the following requested classes: '
                      f'{", ".join(class_diff)}.')
                breakpoint()
            continue

        tracker_element_classes = []
        for ccnn in module_tracker_element_names:
            cc = NAME_CLASS_MAP.get(ccnn, None)
            if cc is None:
                raise ValueError(f'Class `{ccnn}` from kernel `{module_name}` is not available in the current version of xsuite.')
            tracker_element_classes.append(cc)
        if verbose:
            print(f'Found suitable prebuilt kernel `{module_name}`.')
        return {
            'module_name': module_name,
            'tracker_element_classes': tracker_element_classes,
        }

    if verbose:
        print('==> No suitable precompiled kernel found.')


def regenerate_kernels(
        kernels=None,
        location=XSK_PREBUILT_KERNELS_LOCATION,
        n_threads=None,
):
    """
    Use the kernel definitions in the `kernel_definitions.py` file to
    regenerate kernel shared objects using the current version of xsuite.
    """
    if kernels is not None and (
    isinstance(kernels, str) or not hasattr(kernels, '__iter__')):
        kernels = [kernels]

    location = Path(location)

    # Delete existing kernels to avoid accidentally loading in existing C code
    clear_kernels(kernels=kernels, location=location)

    kernels_to_build = []
    for module_name, metadata in kernel_definitions:
        if kernels is not None and module_name not in kernels:
            continue
        kernels_to_build.append((module_name, metadata))

    thread_pool = Pool(processes=n_threads)
    results = []
    for idx, (module_name, metadata) in enumerate(kernels_to_build):
        args = (idx, len(kernels_to_build), location, metadata, module_name)
        result = thread_pool.apply_async(build_single_kernel, args=args)
        results.append(result)

    thread_pool.close()
    thread_pool.join()

    # Ensure no errors
    for result in results:
        result.get()

    _print(f'Built {len(kernels_to_build)} kernels.')


def build_single_kernel(idx, total, location, metadata, module_name):
    _print(f'[{idx + 1}/{total}] Building `{module_name}`...')

    config = metadata['config']
    element_classes = metadata['classes']
    extra_classes = metadata.get('extra_classes', [])

    with warnings.catch_warnings():
        # We still include deprecated elements in the kernels, so silence the warnings
        warnings.filterwarnings('ignore', category=FutureWarning)

        elements = []
        buffer = xo.context_default.new_buffer()
        for cls in element_classes:
            if cls.__name__ in BEAM_ELEMENTS_INIT_DEFAULTS:
                element = cls(**BEAM_ELEMENTS_INIT_DEFAULTS[cls.__name__],
                              _buffer=buffer)
            else:
                element = cls(_buffer=buffer)
            elements.append(element)

    line = xt.Line(elements=elements)
    tracker = xt.Tracker(line=line, compile=False, _prebuilding_kernels=True)
    assert tracker.iscollective == False
    tracker.config.clear()
    tracker.config.update(config)
    tracker_classes = tracker._tracker_data_base.kernel_element_classes
    expected_classes = [getattr(el, '_XoStruct', el) for el in element_classes]
    all_extra_classes = extra_classes + [ee for ee in expected_classes if ee not in tracker_classes]

    # Get all kernels in the elements
    extra_kernels = {}
    extra_xostructs = [getattr(el, '_XoStruct', el) for el in all_extra_classes]

    all_classes = tracker._tracker_data_base.kernel_element_classes + extra_xostructs

    assert len(set(all_classes)) == len(all_classes), 'Duplicate classes in kernel definition.'

    for el in all_classes:
        extra_kernels.update(el._kernels)

    tracker._build_kernel(
        module_name=module_name,
        containing_dir=location,
        compile='force',
        extra_classes=extra_xostructs,
        extra_kernels=extra_kernels,
    )

    save_kernel_metadata(
        module_name=module_name,
        config=tracker.config,
        tracker_element_classes=tracker._tracker_data_base.kernel_element_classes,
        all_classes=all_classes,
        location=location,
    )


def clear_kernels(kernels=None, verbose=False, location=XSK_PREBUILT_KERNELS_LOCATION):
    if kernels is not None and (
            isinstance(kernels, str) or not hasattr(kernels, '__iter__')):
        kernels = [kernels]

    location = Path(location)

    for file in location.iterdir():
        if file.name.startswith('_'):
            continue
        if file.suffix not in ('.c', '.so', '.json'):
            continue
        if kernels is not None and file.stem.split('.')[0] not in kernels:
            continue
        file.unlink()

        if verbose:
            print(f'Removed `{file}`.')


if __name__ == '__main__':
    regenerate_kernels()

