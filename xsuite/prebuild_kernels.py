# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2024.                 #
# ######################################### #
import json
import os
from multiprocessing import Pool
from pathlib import Path
from pprint import pformat
from typing import Iterator, Optional, Tuple

import numpy as np

import xsuite as xs
import xcoll as xc
import xfields as xf
import xobjects as xo
import xtrack as xt
from xsuite.kernel_definitions import kernel_definitions
from xtrack.general import _print

XSK_PREBUILT_KERNELS_LOCATION = Path(xs.__file__).parent / 'lib'

BEAM_ELEMENTS_INIT_DEFAULTS = {
    'Bend': {
        'length': 1.,
    },
    'Quadrupole': {
        'length': 1.,
    },
    'Solenoid': {
        'length': 1.,
    },
    'BeamBeamBiGaussian2D': {
        'other_beam_Sigma_11': 1.,
        'other_beam_Sigma_33': 1.,
        'other_beam_num_particles': 0.,
        'other_beam_q0': 1.,
        'other_beam_beta0': 1.,
    },
    'BeamBeamBiGaussian3D': {
        'slices_other_beam_zeta_center': np.array([0]),
        'slices_other_beam_num_particles': np.array([0]),
        'phi': 0.,
        'alpha': 0,
        'other_beam_q0': 1.,
        'slices_other_beam_Sigma_11': np.array([1]),
        'slices_other_beam_Sigma_12': np.array([0]),
        'slices_other_beam_Sigma_22': np.array([0]),
        'slices_other_beam_Sigma_33': np.array([1]),
        'slices_other_beam_Sigma_34': np.array([0]),
        'slices_other_beam_Sigma_44': np.array([0]),
    },
    'LimitPolygon': {
        'x_vertices': np.array([0, 1, 1, 0]),
        'y_vertices': np.array([0, 0, 1, 1]),
    },
    'BeamProfileMonitor': {
        'range': 1,
    },
    'LastTurnsMonitor': {
        'n_last_turns': 1,
        'num_particles': 1,
    },
    'ParticlesMonitor': {
        'num_particles': 1,
        'start_at_turn': 0,
        'stop_at_turn': 1,
    },
    'Exciter': {
        'samples': [0],
    },
    'SpaceChargeBiGaussian': {
        'longitudinal_profile': {
            '__class__': 'LongitudinalProfileQGaussian',
            'number_of_particles': 1,
            'sigma_z': 0,
        }
    },
    'EverestBlock': {
        'material': xc.materials.Silicon,
    },
    'EverestCollimator': {
        'material': xc.materials.Silicon,
    },
    'EverestCrystal': {
        'material': xc.materials.SiliconCrystal,
    }
}

# SpaceChargeBiGaussian is not included for now (different issues -
# circular import, incompatible compilation flags)


def get_element_class_by_name(name: str) -> type:
    extra_classes = (xt.MultiSetter, )

    element_classes = (xt.element_classes + xt.rng_classes + xt.monitor_classes
                       + xf.element_classes + xc.element_classes
                       + extra_classes)

    for cls in element_classes:
        if cls.__name__ == name:
            return cls

    raise ValueError(f'No element class with name {name} available.')


def save_kernel_metadata(
        module_name: str,
        config: dict,
        kernel_element_classes,
        location,
):
    location = Path(location)
    out_file = location / f'{module_name}.json'

    kernel_metadata = {
        'config': config.data,
        'classes': [cls._DressingClass.__name__ for cls in kernel_element_classes],
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
        line_element_classes,
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
            _print('Skipping the search for a suitable kernel, as the '
                   'environment variable XSUITE_PREBUILT_KERNELS == "0".')
        return

    if os.environ.get("XSUITE_VERBOSE", None) is not None:
        verbose = True

    requested_class_names = [
        cls._DressingClass.__name__ for cls in line_element_classes
    ]

    for module_name, kernel_metadata in enumerate_kernels(verbose=verbose):
        if verbose:
            _print(f"==> Considering the precompiled kernel `{module_name}`...")

        available_classes_names = kernel_metadata['classes']
        if kernel_metadata['config'] != config:
            if verbose:
                lhs = kernel_metadata['config']
                rhs = config
                config_diff = {kk: (lhs.get(kk), rhs.get(kk))
                               for kk in set(lhs.keys()) | set(rhs.keys())
                               if lhs.get(kk) != rhs.get(kk)}
                _print(f'The kernel `{module_name}` is unsuitable. Its config '
                      f'(left) and the requested one (right) differ at the '
                      f'following keys:\n'
                      f'{pformat(config_diff)}')
                _print(f'Skipping class compatibility check for `{module_name}`.')

            continue

        if verbose:
            _print(f'The kernel `{module_name}` has the right config.')

        if set(requested_class_names) <= set(available_classes_names):
            available_classes = [
                get_element_class_by_name(class_name)
                for class_name in available_classes_names
            ]
            if verbose:
                _print(f'Found suitable prebuilt kernel `{module_name}`.')
            return module_name, available_classes
        elif verbose:
            class_diff = set(requested_class_names) - set(available_classes_names)
            _print(f'The kernel `{module_name}` is unsuitable. It does not '
                  f'provide the following requested classes: '
                  f'{", ".join(class_diff)}.')

    if verbose:
        _print('==> No suitable precompiled kernel found.')


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

    elements = []
    for cls in element_classes:
        if cls.__name__ in BEAM_ELEMENTS_INIT_DEFAULTS:
            element = cls(**BEAM_ELEMENTS_INIT_DEFAULTS[cls.__name__])
        else:
            element = cls()
        elements.append(element)

    line = xt.Line(elements=elements)
    tracker = xt.Tracker(line=line, compile=False, _prebuilding_kernels=True)
    tracker.config.clear()
    tracker.config.update(config)

    # Get all kernels in the elements
    extra_kernels = {}
    extra_classes.append(xt.Particles)
    extra_classes = [getattr(el, '_XoStruct', el) for el in extra_classes]

    all_classes = tracker._tracker_data_base.kernel_element_classes + extra_classes

    for el in all_classes:
        extra_kernels.update(el._kernels)

    tracker._build_kernel(
        module_name=module_name,
        containing_dir=location,
        compile='force',
        extra_classes=extra_classes,
        extra_kernels=extra_kernels,
    )

    all_classes = [cls for cls in all_classes if cls.__name__ != 'ParticlesData']

    save_kernel_metadata(
        module_name=module_name,
        config=tracker.config,
        kernel_element_classes=all_classes,
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

