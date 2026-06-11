# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2025.                 #
# ######################################### #
import json
import os
import warnings
from multiprocessing import get_context
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

SERIAL_CONTEXT = 'serial'
OPENMP_CONTEXT = 'omp'
CONTEXT_SUFFIXES = {
    SERIAL_CONTEXT: '_cpu_serial',
    OPENMP_CONTEXT: '_cpu_openmp',
}


def _context_key_from_cli(context: Optional[str]) -> Optional[str]:
    if context is None:
        return None
    if context not in (SERIAL_CONTEXT, OPENMP_CONTEXT):
        raise ValueError(f'Unsupported prebuild context `{context}`.')
    return context


def _context_key_from_runtime(context) -> Optional[str]:
    if context is None:
        return None
    if not isinstance(context, xo.ContextCpu):
        return None
    if context.openmp_enabled:
        return OPENMP_CONTEXT
    return SERIAL_CONTEXT


def _context_key_from_metadata(kernel_metadata: dict) -> str:
    return kernel_metadata.get('context', SERIAL_CONTEXT)


def _split_module_name(module_name: str) -> Tuple[str, str]:
    for context_key, suffix in CONTEXT_SUFFIXES.items():
        if module_name.endswith(suffix):
            return module_name[:-len(suffix)], context_key
    return module_name, SERIAL_CONTEXT


def _module_name_for_context(base_module_name: str, context_key: str) -> str:
    return f'{base_module_name}{CONTEXT_SUFFIXES[context_key]}'


def _iter_kernel_metadata_files():
    for metadata_file in sorted(XSK_PREBUILT_KERNELS_LOCATION.glob('*.json')):
        if metadata_file.name.startswith('_'):
            continue
        yield metadata_file


def save_kernel_metadata(
        module_name: str,
        base_module_name: str,
        context_key: str,
        config: dict,
        tracker_element_classes,
        all_classes,
        location,
):
    location = Path(location)
    out_file = location / f'{module_name}.json'

    kernel_metadata = {
        'base_module_name': base_module_name,
        'context': context_key,
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
    kernel_order = {name: idx for idx, (name, _) in enumerate(kernel_definitions)}
    candidates = []
    for metadata_file in _iter_kernel_metadata_files():
        module_name = metadata_file.stem

        with metadata_file.open('r') as fd:
            kernel_metadata = json.load(fd)

        base_module_name = kernel_metadata.get('base_module_name')
        if base_module_name is None:
            base_module_name, _ = _split_module_name(module_name)
            kernel_metadata['base_module_name'] = base_module_name

        explicit_context = 'context' in kernel_metadata
        context_key = _context_key_from_metadata(kernel_metadata)
        kernel_metadata['context'] = context_key

        if base_module_name not in kernel_order:
            continue

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
                    f'Version mismatch for kernel `{module_name}`: needs '
                    f'{package}=={need}, but have {package}=={have}.'
                )

        if version_mismatch:
            continue

        candidates.append((
            kernel_order[base_module_name],
            0 if explicit_context else 1,
            module_name,
            kernel_metadata,
        ))

    for _, _, module_name, kernel_metadata in sorted(candidates):
        yield module_name, kernel_metadata


def get_suitable_kernel(
        config: dict,
        tracker_element_classes,
        classes,
        context=None,
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
    requested_context = _context_key_from_runtime(context)

    for module_name, kernel_metadata in enumerate_kernels(verbose=verbose):
        if verbose:
            print(f"==> Considering the precompiled kernel `{module_name}`...")

        kernel_context = _context_key_from_metadata(kernel_metadata)
        if requested_context is not None and kernel_context != requested_context:
            if verbose:
                print(f'The kernel `{module_name}` is unsuitable. Its context '
                      f'is `{kernel_context}`, but the requested one is '
                      f'`{requested_context}`.')
            continue

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
        context='serial',
):
    """
    Use the kernel definitions in the `kernel_definitions.py` file to
    regenerate kernel shared objects using the current version of xsuite.
    """
    if kernels is not None and (
    isinstance(kernels, str) or not hasattr(kernels, '__iter__')):
        kernels = [kernels]

    location = Path(location)
    context_key = _context_key_from_cli(context)

    # Delete existing kernels to avoid accidentally loading in existing C code
    clear_kernels(kernels=kernels, location=location, context=context)

    old_prebuilt_env = os.environ.get("XSUITE_PREBUILT_KERNELS")
    os.environ["XSUITE_PREBUILT_KERNELS"] = "0"
    try:
        kernels_to_build = []
        for base_module_name, metadata in kernel_definitions:
            if kernels is not None and base_module_name not in kernels:
                continue
            module_name = _module_name_for_context(base_module_name, context_key)
            kernels_to_build.append((base_module_name, module_name, metadata))

        if n_threads == 0:
            for idx, (base_module_name, module_name, metadata) in enumerate(kernels_to_build):
                build_single_kernel(
                    idx, len(kernels_to_build), location, metadata, module_name,
                    base_module_name, context_key,
                )
        else:
            thread_pool = get_context('spawn').Pool(processes=n_threads)
            results = []
            for idx, (base_module_name, module_name, metadata) in enumerate(kernels_to_build):
                args = (
                    idx, len(kernels_to_build), location, metadata, module_name,
                    base_module_name, context_key,
                )
                result = thread_pool.apply_async(build_single_kernel, args=args)
                results.append(result)

            thread_pool.close()
            thread_pool.join()

            # Ensure no errors
            for result in results:
                result.get()
    finally:
        if old_prebuilt_env is None:
            del os.environ["XSUITE_PREBUILT_KERNELS"]
        else:
            os.environ["XSUITE_PREBUILT_KERNELS"] = old_prebuilt_env

    _print(f'Built {len(kernels_to_build)} kernels.')


def build_single_kernel(
        idx, total, location, metadata, module_name, base_module_name, context_key,
):
    _print(f'[{idx + 1}/{total}] Building `{module_name}`...')

    config = metadata['config']
    element_classes = metadata['classes']
    extra_classes = metadata.get('extra_classes', [])
    build_context = xo.ContextCpu() if context_key == SERIAL_CONTEXT else xo.ContextCpu(
        omp_num_threads='auto'
    )

    with warnings.catch_warnings():
        # We still include deprecated elements in the kernels, so silence the warnings
        warnings.filterwarnings('ignore', category=FutureWarning)

        elements = []
        buffer = build_context.new_buffer()
        for cls in element_classes:
            if cls.__name__ in BEAM_ELEMENTS_INIT_DEFAULTS:
                element = cls(**BEAM_ELEMENTS_INIT_DEFAULTS[cls.__name__],
                              _buffer=buffer)
            else:
                element = cls(_buffer=buffer)
            elements.append(element)

    line = xt.Line(elements=elements)
    tracker = xt.Tracker(
        line=line,
        compile=False,
        _context=build_context,
        _prebuilding_kernels=True,
    )
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
        base_module_name=base_module_name,
        context_key=context_key,
        config=tracker.config,
        tracker_element_classes=tracker._tracker_data_base.kernel_element_classes,
        all_classes=all_classes,
        location=location,
    )


def clear_kernels(
        kernels=None,
        verbose=False,
        location=XSK_PREBUILT_KERNELS_LOCATION,
        context=None,
):
    if kernels is not None and (
            isinstance(kernels, str) or not hasattr(kernels, '__iter__')):
        kernels = [kernels]

    location = Path(location)
    context_key = _context_key_from_cli(context)

    for file in location.iterdir():
        if file.name.startswith('_'):
            continue
        if file.suffix not in ('.c', '.so', '.json'):
            continue

        module_name = file.stem.split('.')[0]
        base_module_name, file_context_key = _split_module_name(module_name)

        if kernels is not None and base_module_name not in kernels:
            continue
        if context_key is not None and file_context_key != context_key:
            continue
        file.unlink()

        if verbose:
            print(f'Removed `{file}`.')


if __name__ == '__main__':
    regenerate_kernels()
