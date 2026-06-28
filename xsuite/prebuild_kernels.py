# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2025.                 #
# ######################################### #
import json
import os
import sysconfig
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
OPENMP_CONTEXT = 'openmp'
CONTEXT_SUFFIXES = {
    SERIAL_CONTEXT: '_cpu_serial',
    OPENMP_CONTEXT: '_cpu_openmp',
}


class PrebuiltKernelNotFoundError(RuntimeError):
    pass


def _current_package_versions():
    return {
        'xtrack': xt.__version__,
        'xfields': xf.__version__,
        'xcoll': xc.__version__,
        'xobjects': xo.__version__,
    }


def _context_key_from_cli(context: Optional[str]) -> Optional[str]:
    if context is None:
        return None
    if context not in (SERIAL_CONTEXT, OPENMP_CONTEXT):
        raise ValueError(f'Unsupported prebuild context `{context}`.')
    return context


def _context_keys_from_cli(context) -> Optional[Tuple[str, ...]]:
    if context is None:
        return None

    if isinstance(context, str):
        raw_contexts = context.split(',')
    elif hasattr(context, '__iter__'):
        raw_contexts = context
    else:
        raw_contexts = [context]

    context_keys = []
    for raw_context in raw_contexts:
        if raw_context is None:
            continue
        context_key = _context_key_from_cli(raw_context.strip())
        if context_key not in context_keys:
            context_keys.append(context_key)

    if not context_keys:
        raise ValueError('At least one prebuild context must be provided.')

    return tuple(context_keys)


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


def _kernel_binary_file(module_name, location=None):
    if location is None:
        location = XSK_PREBUILT_KERNELS_LOCATION
    suffix = sysconfig.get_config_var('EXT_SUFFIX')
    if suffix is None:
        suffix = '.so'
    return Path(location) / f'{module_name}{suffix}'


def _kernel_binary_exists(module_name, location=None):
    return _kernel_binary_file(module_name, location=location).exists()


def _read_kernel_metadata(metadata_file):
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

    return module_name, kernel_metadata, explicit_context


def _format_list(items, limit=5):
    items = list(items)
    formatted = [f'- {item}' for item in items[:limit]]
    if len(items) > limit:
        formatted.append(f'- ... and {len(items) - limit} more')
    return '\n'.join(formatted)


def _format_update_or_regenerate_message():
    return (
        'Suggested fixes: update xsuite with `pip install --upgrade xsuite` '
        '(usually faster), or regenerate the kernels with '
        '`xsuite-prebuild regenerate` (can take some time).'
    )


def _build_no_suitable_kernel_message(requested_context, closest_rejection_reason):
    metadata_files = list(_iter_kernel_metadata_files())
    if not metadata_files:
        return (
            'Could not find a suitable Xsuite prebuilt kernel.\n'
            f'Reason: xsuite is installed, but no cached kernels were found in '
            f'`{XSK_PREBUILT_KERNELS_LOCATION}`.\n'
            f'{_format_update_or_regenerate_message()}\n'
            f'{xo.context_cpu.no_prebuilt_kernel_jit_message()}'
        )

    kernel_order = {name: idx for idx, (name, _) in enumerate(kernel_definitions)}
    have_versions = _current_package_versions()
    known_metadata_count = 0
    version_mismatches = set()
    compatible_metadata_count = 0
    unknown_metadata = []
    missing_binary_details = []

    for metadata_file in metadata_files:
        try:
            module_name, kernel_metadata, _ = _read_kernel_metadata(metadata_file)
        except Exception as err:
            unknown_metadata.append(
                f'`{metadata_file.name}` could not be read ({err}).'
            )
            continue

        base_module_name = kernel_metadata['base_module_name']
        if base_module_name not in kernel_order:
            unknown_metadata.append(
                f'`{module_name}` is not a known kernel for this xsuite version.'
            )
            continue

        if not _kernel_binary_exists(module_name):
            missing_binary_details.append(
                f'`{module_name}` metadata exists, but '
                f'`{_kernel_binary_file(module_name).name}` was not found.'
            )
            continue

        known_metadata_count += 1
        kernel_has_version_mismatch = False
        for package, need in kernel_metadata.get('versions', {}).items():
            have = have_versions.get(package, 'not installed')
            if need == have:
                continue
            kernel_has_version_mismatch = True
            version_mismatches.add((package, need, have))

        if not kernel_has_version_mismatch:
            compatible_metadata_count += 1

    if missing_binary_details and known_metadata_count == 0:
        return (
            'Could not find a suitable Xsuite prebuilt kernel.\n'
            'Reason: xsuite is installed, but no compiled cached kernels were '
            'found for this Python/platform.\n'
            f'{_format_list(missing_binary_details)}\n'
            f'{_format_update_or_regenerate_message()}\n'
            f'{xo.context_cpu.no_prebuilt_kernel_jit_message()}'
        )

    if known_metadata_count and compatible_metadata_count == 0:
        version_mismatch_details = [
            f'cached kernels need {package}=={need}, but the current '
            f'environment has {package}=={have}.'
            for package, need, have in sorted(version_mismatches)
        ]
        return (
            'Could not find a suitable Xsuite prebuilt kernel.\n'
            'Reason: cached kernels were found, but their package versions do '
            'not match the installed packages.\n'
            f'{_format_list(version_mismatch_details)}\n'
            f'{_format_update_or_regenerate_message()}\n'
            f'{xo.context_cpu.no_prebuilt_kernel_jit_message()}'
        )

    reason = (
        'Reason: no cached kernel matches the requested configuration, '
        'context, or element classes.'
    )
    details = []
    if requested_context is not None:
        details.append(f'Requested context: `{requested_context}`.')
    if closest_rejection_reason:
        details.append(f'Closest cached kernel: {closest_rejection_reason}')
    elif unknown_metadata:
        details.append(_format_list(unknown_metadata))

    details_text = '\n'.join(details)
    if details_text:
        details_text = f'\n{details_text}'

    return (
        'Could not find a suitable Xsuite prebuilt kernel.\n'
        f'{reason}{details_text}\n'
        'This can happen with a wrong or unsupported configuration. If this is '
        'not expected, please contact the developers.\n'
        f'{xo.context_cpu.no_prebuilt_kernel_jit_message()}'
    )


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
        'versions': _current_package_versions()
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
        module_name, kernel_metadata, explicit_context = _read_kernel_metadata(
            metadata_file
        )
        base_module_name = kernel_metadata['base_module_name']

        if base_module_name not in kernel_order:
            continue

        if not _kernel_binary_exists(module_name):
            if verbose:
                _print(
                    f'Compiled kernel `{_kernel_binary_file(module_name).name}` '
                    f'not found for metadata `{metadata_file.name}`.'
                )
            continue

        needed_versions = kernel_metadata['versions']
        have_versions = _current_package_versions()

        version_mismatch = False
        for package in needed_versions.keys():
            need = needed_versions[package]
            have = have_versions.get(package, 'not installed')
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
    rejection_reasons = []

    for module_name, kernel_metadata in enumerate_kernels(verbose=verbose):
        if verbose:
            print(f"==> Considering the precompiled kernel `{module_name}`...")

        kernel_context = _context_key_from_metadata(kernel_metadata)
        if requested_context is not None and kernel_context != requested_context:
            rejection_reasons.append(
                (
                    (1000, module_name),
                    f'`{module_name}` was built for context `{kernel_context}`, '
                    f'but context `{requested_context}` was requested.'
                )
            )
            if verbose:
                print(f'The kernel `{module_name}` is unsuitable. Its context '
                      f'is `{kernel_context}`, but the requested one is '
                      f'`{requested_context}`.')
            continue

        if kernel_metadata['config'] != config:
            lhs = kernel_metadata['config']
            rhs = config
            config_diff = {kk: (lhs.get(kk), rhs.get(kk))
                           for kk in set(lhs.keys()) | set(rhs.keys())
                           if lhs.get(kk) != rhs.get(kk)}
            rejection_reasons.append(
                (
                    (len(config_diff), module_name),
                    f'`{module_name}` has a different configuration '
                    f'({len(config_diff)} differing key(s): '
                    f'{", ".join(sorted(config_diff.keys())) or "none"}).'
                )
            )
            if verbose:
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
            class_diff = set(requested_tracker_class_names) - set(module_tracker_element_names)
            rejection_reasons.append(
                (
                    (100 + len(class_diff), module_name),
                    f'`{module_name}` is missing requested tracker element '
                    f'class(es): {", ".join(sorted(class_diff))}.'
                )
            )
            if verbose:
                print(f'The kernel `{module_name}` is unsuitable. It does not '
                      f'provide the following requested classes: '
                      f'{", ".join(class_diff)}.')
            continue

        all_class_names = set(module_tracker_element_names) | set(module_class_names)
        if not set(requested_class_names) <= all_class_names:
            class_diff = set(requested_class_names) - all_class_names
            rejection_reasons.append(
                (
                    (100 + len(class_diff), module_name),
                    f'`{module_name}` is missing requested class(es): '
                    f'{", ".join(sorted(class_diff))}.'
                )
            )
            if verbose:
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

    if not xo.context_cpu.require_prebuilt_kernel(context=context):
        return None

    raise PrebuiltKernelNotFoundError(
        _build_no_suitable_kernel_message(
            requested_context=requested_context,
            closest_rejection_reason=(
                min(rejection_reasons)[1] if rejection_reasons else None
            ),
        )
    )


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
    context_keys = _context_keys_from_cli(context)

    # Delete existing kernels to avoid accidentally loading in existing C code
    clear_kernels(kernels=kernels, location=location, context=context)

    old_prebuilt_env = os.environ.get("XSUITE_PREBUILT_KERNELS")
    os.environ["XSUITE_PREBUILT_KERNELS"] = "0"
    try:
        kernels_to_build = []
        for base_module_name, metadata in kernel_definitions:
            if kernels is not None and base_module_name not in kernels:
                continue
            for context_key in context_keys:
                module_name = _module_name_for_context(base_module_name, context_key)
                kernels_to_build.append((base_module_name, module_name, metadata, context_key))

        if n_threads == 0:
            for idx, (base_module_name, module_name, metadata, context_key) in enumerate(kernels_to_build):
                build_single_kernel(
                    idx, len(kernels_to_build), location, metadata, module_name,
                    base_module_name, context_key,
                )
        else:
            thread_pool = get_context('spawn').Pool(processes=n_threads)
            results = []
            for idx, (base_module_name, module_name, metadata, context_key) in enumerate(kernels_to_build):
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
    context_keys = _context_keys_from_cli(context)

    for file in location.iterdir():
        if file.name.startswith('_'):
            continue
        if file.suffix not in ('.c', '.so', '.json'):
            continue

        module_name = file.stem.split('.')[0]
        base_module_name, file_context_key = _split_module_name(module_name)

        if kernels is not None and base_module_name not in kernels:
            continue
        if context_keys is not None and file_context_key not in context_keys:
            continue
        file.unlink()

        if verbose:
            print(f'Removed `{file}`.')


if __name__ == '__main__':
    regenerate_kernels()
