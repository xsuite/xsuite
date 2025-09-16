# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2025.                 #
# ######################################### #
import logging

from xtrack.prebuilt_kernel_definitions import (ONLY_XTRACK_ELEMENTS,
                                    NO_SYNRAD_ELEMENTS, NON_TRACKING_ELEMENTS)
from xcoll.prebuilt_kernel_definitions import DEFAULT_XCOLL_ELEMENTS
from xfields.prebuilt_kernel_definitions import DEFAULT_XFIELDS_ELEMENTS


LOGGER = logging.getLogger(__name__)

BASE_CONFIG = {
    'XTRACK_MULTIPOLE_NO_SYNRAD': True,
    'XFIELDS_BB3D_NO_BEAMSTR': True,
    'XFIELDS_BB3D_NO_BHABHA': True,
    'XTRACK_GLOBAL_XY_LIMIT': 1.0,
}

# These are enumerated in order specified below: the highest priority at the top
kernel_definitions = [
    ('non_tracking_kernels', {
        'config': BASE_CONFIG,
        'classes': [],
        'extra_classes': NON_TRACKING_ELEMENTS
    }),
    ('default_no_config', {
        'config': {},
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XFIELDS_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
    ('default_base_config', {
        'config': BASE_CONFIG,
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XFIELDS_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
    ('only_xtrack_with_synrad', {
        'config': {**BASE_CONFIG, 'XTRACK_MULTIPOLE_NO_SYNRAD': False},
        'classes': ONLY_XTRACK_ELEMENTS,
    }),
]
