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

ONLY_XTRACK_ELEMENTS = [
    Drift,
    Multipole,
    Bend,
    RBend,
    Quadrupole,
    Sextupole,
    Octupole,
    Magnet,
    SecondOrderTaylorMap,
    Marker,
    ReferenceEnergyIncrease,
    Cavity,
    CrabCavity,
    Elens,
    Wire,
    Solenoid,
    VariableSolenoid,
    UniformSolenoid,
    RFMultipole,
    DipoleEdge,
    MultipoleEdge,
    SimpleThinBend,
    SimpleThinQuadrupole,
    LineSegmentMap,
    FirstOrderTaylorMap,
    NonLinearLens,
    # Drift Slices
    DriftSlice,
    DriftSliceBend,
    DriftSliceRBend,
    DriftSliceOctupole,
    DriftSliceQuadrupole,
    DriftSliceSextupole,
    DriftSliceCavity,
    DriftSliceCrabCavity,
    DriftSliceMultipole,
    # Thick slices
    ThickSliceBend,
    ThickSliceRBend,
    ThickSliceOctupole,
    ThickSliceQuadrupole,
    ThickSliceSextupole,
    ThickSliceUniformSolenoid,
    ThickSliceCavity,
    ThickSliceCrabCavity,
    ThickSliceMultipole,
    # Thin slices
    ThinSliceBend,
    ThinSliceRBend,
    ThinSliceOctupole,
    ThinSliceQuadrupole,
    ThinSliceSextupole,
    ThinSliceCavity,
    ThinSliceCrabCavity,
    ThinSliceMultipole,
    # Edge slices
    ThinSliceBendEntry,
    ThinSliceBendExit,
    ThinSliceRBendEntry,
    ThinSliceRBendExit,
    ThinSliceQuadrupoleEntry,
    ThinSliceQuadrupoleExit,
    ThinSliceSextupoleEntry,
    ThinSliceSextupoleExit,
    ThinSliceUniformSolenoidEntry,
    ThinSliceUniformSolenoidExit,
    ThinSliceOctupoleEntry,
    ThinSliceOctupoleExit,

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
    Exciter,
]

# Xfields elements
DEFAULT_XF_ELEMENTS = [
    xf.BeamBeamBiGaussian2D,
    xf.BeamBeamBiGaussian3D,
    xf.SpaceChargeBiGaussian,
]

# Xcoll elements
DEFAULT_XCOLL_ELEMENTS = [
    ZetaShift,
    xc.BlackAbsorber,
    xc.EverestBlock,
    xc.EverestCollimator,
    xc.EverestCrystal,
    xc.BlowUp,
    xc.EmittanceMonitor
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
    ('non_tracking_kernels', {
        'config': BASE_CONFIG,
        'classes': [],
        'extra_classes': NON_TRACKING_ELEMENTS
    }),
    ('default_no_config', {
        'config': {},
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XF_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
    ('default_base_config', {
        'config': BASE_CONFIG,
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XF_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
    ('exact_drifts', {
        'config': {
            **BASE_CONFIG,
            'XTRACK_USE_EXACT_DRIFTS': True,
        },
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XF_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
    ('default_no_limit', {
        'config': {
            **{k: v for k, v in BASE_CONFIG.items()
                if k != 'XTRACK_GLOBAL_XY_LIMIT'}
        },
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XF_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
    ('default_backtrack', {
        'config': {**BASE_CONFIG, 'XSUITE_BACKTRACK': True},
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XF_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
    ('only_xtrack_backtrack_no_limit', {
        'config': {
            **BASE_CONFIG,
            'XSUITE_BACKTRACK': True,
            'XTRACK_GLOBAL_XY_LIMIT': False,
        },
        'classes': ONLY_XTRACK_ELEMENTS + NO_SYNRAD_ELEMENTS + DEFAULT_XF_ELEMENTS + DEFAULT_XCOLL_ELEMENTS,
    }),
    ('only_xtrack_with_synrad', {
        'config': {**BASE_CONFIG, 'XTRACK_MULTIPOLE_NO_SYNRAD': False},
        'classes': ONLY_XTRACK_ELEMENTS,
    }),
]
