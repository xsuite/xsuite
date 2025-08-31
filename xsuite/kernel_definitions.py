# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2025.                 #
# ######################################### #
import logging

from xtrack.prebuild_kernels import BASE_CONFIG, FREEZE_ENERGY, FREEZE_LONGITUDINAL, \
                                    ONLY_XTRACK_ELEMENTS, NO_SYNRAD_ELEMENTS, \
                                    NON_TRACKING_ELEMENTS
from xcoll.prebuild_kernels import DEFAULT_XCOLL_ELEMENTS
from xfields.prebuild_kernels import DEFAULT_XFIELDS_ELEMENTS


LOGGER = logging.getLogger(__name__)


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
    ('exact_drifts', {
        'config': {
            **BASE_CONFIG,
            'XTRACK_USE_EXACT_DRIFTS': True,
        },
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XFIELDS_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
    ('default_no_limit', {
        'config': {
            **{k: v for k, v in BASE_CONFIG.items()
                if k != 'XTRACK_GLOBAL_XY_LIMIT'}
        },
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XFIELDS_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
    ('default_backtrack', {
        'config': {**BASE_CONFIG, 'XSUITE_BACKTRACK': True},
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XFIELDS_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
    ('only_xtrack_backtrack_no_limit', {
        'config': {
            **BASE_CONFIG,
            'XSUITE_BACKTRACK': True,
            'XTRACK_GLOBAL_XY_LIMIT': False,
        },
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XFIELDS_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
    ('frozen_longitudinal', {
        'config': {**BASE_CONFIG, **FREEZE_LONGITUDINAL},
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XFIELDS_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
    ('frozen_energy', {
        'config': {**BASE_CONFIG, **FREEZE_ENERGY},
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XFIELDS_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
    ('backtrack_frozen_energy', {
        'config': {**BASE_CONFIG, **FREEZE_ENERGY, 'XSUITE_BACKTRACK': True},
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XFIELDS_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
    ('mirror_frozen_energy', {
        'config': {**BASE_CONFIG, **FREEZE_ENERGY, 'XSUITE_MIRROR': True},
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XFIELDS_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
    ('only_xtrack_taper', {
        'config': {
            **BASE_CONFIG,
            'XTRACK_MULTIPOLE_NO_SYNRAD': False,
            'XTRACK_MULTIPOLE_TAPER': True,
            'XTRACK_DIPOLEEDGE_TAPER': True,
        },
        'classes': ONLY_XTRACK_ELEMENTS,
    }),
    ('only_xtrack_with_synrad', {
        'config': {**BASE_CONFIG, 'XTRACK_MULTIPOLE_NO_SYNRAD': False},
        'classes': ONLY_XTRACK_ELEMENTS,
    }),
    ('only_xtrack_with_synrad_kick_as_co', {
        'config': {
            **BASE_CONFIG, 'XTRACK_MULTIPOLE_NO_SYNRAD': False,
            'XTRACK_SYNRAD_KICK_SAME_AS_FIRST': True
        },
        'classes': ONLY_XTRACK_ELEMENTS,
    }),
    ('only_xtrack_with_synrad_frozen_energy', { # for spin twiss
        'config': {**BASE_CONFIG, **FREEZE_ENERGY, 'XTRACK_MULTIPOLE_NO_SYNRAD': False,},
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XFIELDS_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
]
