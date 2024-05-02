# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2024.                 #
# ######################################### #
import logging

import xcoll as xc
import xfields as xf

from xtrack.beam_elements import *
from xtrack.monitors import *
from xtrack.random import *
from xtrack.multisetter import MultiSetter

LOGGER = logging.getLogger(__name__)

BASE_CONFIG = {
    'XTRACK_MULTIPOLE_NO_SYNRAD': True,
    'XFIELDS_BB3D_NO_BEAMSTR': True,
    'XFIELDS_BB3D_NO_BHABHA': True,
    'XTRACK_GLOBAL_XY_LIMIT': 1.0,
}

FREEZE_ENERGY = {
    'FREEZE_VAR_delta': True,
    'FREEZE_VAR_ptau': True,
    'FREEZE_VAR_rpp': True,
    'FREEZE_VAR_rvv': True,
}

FREEZE_LONGITUDINAL = {
    **FREEZE_ENERGY,
    'FREEZE_VAR_zeta': True,
}

ONLY_XTRACK_ELEMENTS = [
    Drift,
    Multipole,
    Marker,
    ReferenceEnergyIncrease,
    Cavity,
    Elens,
    Wire,
    Solenoid,
    RFMultipole,
    DipoleEdge,
    SimpleThinBend,
    SimpleThinQuadrupole,
    LineSegmentMap,
    FirstOrderTaylorMap,
    NonLinearLens,
    # Slices
    DriftSlice,
    DriftSliceBend,
    DriftSliceOctupole,
    DriftSliceQuadrupole,
    DriftSliceSextupole,
    ThickSliceBend,
    ThickSliceOctupole,
    ThickSliceQuadrupole,
    ThickSliceSextupole,
    ThickSliceSolenoid,
    ThinSliceBend,
    ThinSliceBendEntry,
    ThinSliceBendExit,
    ThinSliceOctupole,
    ThinSliceQuadrupole,
    ThinSliceSextupole,
    # Transformations
    XYShift,
    ZetaShift,
    XRotation,
    SRotation,
    YRotation,
    # Apertures
    LimitEllipse,
    LimitRectEllipse,
    LimitRect,
    LimitRacetrack,
    LimitPolygon,
    LongitudinalLimitRect,
    # Monitors
    BeamPositionMonitor,
    BeamSizeMonitor,
    BeamProfileMonitor,
    LastTurnsMonitor,
    ParticlesMonitor,
]

NO_SYNRAD_ELEMENTS = [
    Bend,
    Quadrupole,
    Sextupole,
    Octupole,
    SecondOrderTaylorMap,
    Exciter,
]

NON_TRACKING_ELEMENTS = [
    RandomUniform,
    RandomExponential,
    RandomNormal,
    RandomRutherford,
    MultiSetter,
]

# These are enumerated in order specified below: the highest priority at the top
kernel_definitions = [
    # ('default_only_xtrack_no_config', {
    #     'config': {},
    #     'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS,
    # }),
    ('default_only_xtrack', {
        'config': BASE_CONFIG,
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS,
    }),
    ('default_only_xtrack_exact_drifts', {
        'config': {
            **BASE_CONFIG,
            'XTRACK_USE_EXACT_DRIFTS': True,
        },
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS,
    }),
    ('default_only_xtrack_no_limit', {
        'config': {
            **{k: v for k, v in BASE_CONFIG.items()
                if k != 'XTRACK_GLOBAL_XY_LIMIT'}
        },
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS,
    }),
    ('only_xtrack_non_tracking_kernels_no_config', {
        'config': {},
        'classes': [],
        'extra_classes': NON_TRACKING_ELEMENTS
    }),
    ('only_xtrack_non_tracking_kernels', {
        'config': BASE_CONFIG,
        'classes': [],
        'extra_classes': NON_TRACKING_ELEMENTS
    }),
    ('default_only_xtrack_backtrack', {
        'config': {**BASE_CONFIG, 'XSUITE_BACKTRACK': True},
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS,
    }),
    ('default_only_xtrack_backtrack_no_limit', {
        'config': {
            **{k: v for k, v in BASE_CONFIG.items()
                if k != 'XTRACK_GLOBAL_XY_LIMIT'},
            'XSUITE_BACKTRACK': True
        },
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS,
    }),
    ('only_xtrack_frozen_longitudinal', {
        'config': {**BASE_CONFIG, **FREEZE_LONGITUDINAL},
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS,
    }),
    ('only_xtrack_frozen_energy', {
        'config': {**BASE_CONFIG, **FREEZE_ENERGY},
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS,
    }),
    ('only_xtrack_backtrack_frozen_energy', {
        'config': {**BASE_CONFIG, **FREEZE_ENERGY, 'XSUITE_BACKTRACK': True},
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS,
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
]


# Xfields elements
DEFAULT_XF_ELEMENTS = [
    *ONLY_XTRACK_ELEMENTS,
    xf.BeamBeamBiGaussian2D,
    xf.BeamBeamBiGaussian3D,
    xf.SpaceChargeBiGaussian,
]

kernel_definitions += [
    ('default_xfields', {
        'config': BASE_CONFIG,
        'classes': [*DEFAULT_XF_ELEMENTS],
    }),
    ('default_xfields_no_config', {
        'config': {},
        'classes': [*DEFAULT_XF_ELEMENTS],
    }),
    ('default_xfields_frozen_longitudinal', {
        'config': {**BASE_CONFIG, **FREEZE_LONGITUDINAL},
        'classes': DEFAULT_XF_ELEMENTS,
    }),
    ('default_xfields_frozen_energy', {
        'config': {**BASE_CONFIG, **FREEZE_ENERGY},
        'classes': DEFAULT_XF_ELEMENTS,
    }),
]

# Xcoll elements
DEFAULT_XCOLL_ELEMENTS = [
    *ONLY_XTRACK_ELEMENTS,
    *NO_SYNRAD_ELEMENTS,
    ZetaShift,
    xc.BlackAbsorber,
    xc.EverestBlock,
    xc.EverestCollimator,
    xc.EverestCrystal
]

kernel_definitions += [
    ('default_xcoll', {
        'config': BASE_CONFIG,
        'classes': DEFAULT_XCOLL_ELEMENTS,
    }),
    ('default_xcoll_no_config', {
        'config': {},
        'classes': DEFAULT_XCOLL_ELEMENTS,
    }),
    ('default_xcoll_no_limit', {
        'config': {
            **{k: v for k, v in BASE_CONFIG.items()
                if k != 'XTRACK_GLOBAL_XY_LIMIT'}
        },
        'classes': DEFAULT_XCOLL_ELEMENTS,
    }),
    ('default_xcoll_frozen_longitudinal', {
        'config': {**BASE_CONFIG, **FREEZE_LONGITUDINAL},
        'classes': DEFAULT_XCOLL_ELEMENTS,
    }),
    ('default_xcoll_frozen_energy', {
        'config': {**BASE_CONFIG, **FREEZE_ENERGY},
        'classes': DEFAULT_XCOLL_ELEMENTS,
    }),
    ('default_xcoll_backtrack', {
        'config': {**BASE_CONFIG, 'XSUITE_BACKTRACK': True},
        'classes': DEFAULT_XCOLL_ELEMENTS,
    }),
    ('default_xcoll_backtrack_no_limit', {
        'config': {
            **{k: v for k, v in BASE_CONFIG.items()
                if k != 'XTRACK_GLOBAL_XY_LIMIT'},
            'XSUITE_BACKTRACK': True
        },
        'classes': DEFAULT_XCOLL_ELEMENTS,
    }),
    ('default_xcoll_backtrack_frozen_energy', {
        'config': {**BASE_CONFIG, **FREEZE_ENERGY, 'XSUITE_BACKTRACK': True},
        'classes': DEFAULT_XCOLL_ELEMENTS,
    }),
]
