# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2025.                 #
# ######################################### #
import logging

from xtrack.prebuilt_kernel_definitions import (ONLY_XTRACK_ELEMENTS,
                                    NO_SYNRAD_ELEMENTS, NON_TRACKING_ELEMENTS,
                                    TPSA_SUPPORTED_ELEMENTS)
from xcoll.prebuilt_kernel_definitions import DEFAULT_XCOLL_ELEMENTS, EXTRA_XCOLL_ELEMENTS
from xfields.prebuilt_kernel_definitions import DEFAULT_XFIELDS_ELEMENTS
from xfields.prebuilt_kernel_definitions import NON_TRACKING_ELEMENTS as XFIELDS_NON_TRACKING_ELEMENTS

import xtrack as xt

XTRACK_ELEMENTS = ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS


LOGGER = logging.getLogger(__name__)

BASE_CONFIG = {
    'XTRACK_MULTIPOLE_NO_SYNRAD': True,
    'XFIELDS_BB3D_NO_BEAMSTR': True,
    'XFIELDS_BB3D_NO_BHABHA': True,
    'XTRACK_GLOBAL_XY_LIMIT': 1.0,
}

SCALAR_MONITOR_CLASSES = [xt.ParticlesMonitor, xt.MultiElementMonitor]
TPSA_MONITOR_CLASSES = [xt.MultiElementMonitor]

# These are enumerated in order specified below: the highest priority at the top
kernel_definitions = [
    ('non_tracking_kernels', {
        'config': {},
        # Tracker compilation needs a non-empty ElementRef union even though this
        # kernel only provides auxiliary kernels.
        'classes': [xt.Marker],
        'extra_classes': (
            [xt.Particles] + NON_TRACKING_ELEMENTS + XFIELDS_NON_TRACKING_ELEMENTS
            + SCALAR_MONITOR_CLASSES
        ),
    }),
    ('default_no_config', {
        'config': {},
        'classes': XTRACK_ELEMENTS + DEFAULT_XFIELDS_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
        'extra_classes': [xt.Particles] + EXTRA_XCOLL_ELEMENTS + SCALAR_MONITOR_CLASSES,
    }),
    ('default_base_config', {
        'config': BASE_CONFIG,
        'classes': XTRACK_ELEMENTS + DEFAULT_XFIELDS_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
        'extra_classes': [xt.Particles] + EXTRA_XCOLL_ELEMENTS + SCALAR_MONITOR_CLASSES,
    }),
    ('tpsa_base_config', {
        'config': {**BASE_CONFIG, 'XTRACK_TPSA_TRACK': True},
        'classes': TPSA_SUPPORTED_ELEMENTS,
        'extra_classes': [xt.MultiSetter] + TPSA_MONITOR_CLASSES,
    }),
    ('all_with_synrad', {
        'config': {**BASE_CONFIG, 'XTRACK_MULTIPOLE_NO_SYNRAD': False},
        'classes': ONLY_XTRACK_ELEMENTS + DEFAULT_XFIELDS_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
        'extra_classes': [xt.Particles] + SCALAR_MONITOR_CLASSES,
    }),
    ('all_with_radiative', {
        'config': {**BASE_CONFIG, 'XTRACK_MULTIPOLE_NO_SYNRAD': False,
                   'XFIELDS_BB3D_NO_BEAMSTR': False, 'XFIELDS_BB3D_NO_BHABHA': False},
        'classes': XTRACK_ELEMENTS + DEFAULT_XFIELDS_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
        'extra_classes': [xt.Particles] + SCALAR_MONITOR_CLASSES,
    }),
]

NAME_CLASS_MAP = {}
for _, kernel_def in kernel_definitions:
    for cls in kernel_def.get('classes', []):
        NAME_CLASS_MAP[cls.__name__] = cls
    for cls in kernel_def.get('extra_classes', []):
        NAME_CLASS_MAP[cls.__name__] = cls
