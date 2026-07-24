# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2024.                 #
# ######################################### #

"""Regression test for xsuite/xsuite#884.

RFBucket must auto-centre the bucket interval when zeta0 is not provided,
so that non-zero phi_offset values do not produce zero-width buckets.
"""

import numpy as np
import pytest
from scipy.constants import e, m_p


def test_rfbucket_autocentre_nonzero_phi_offset():
    """RFBucket with non-zero phi_offset and zeta0=None must produce a
    non-zero-width bucket (regression for #884)."""
    from xpart.longitudinal.rf_bucket import RFBucket

    C, h, V = 26658.883, 35640, 6e6

    bucket = RFBucket(
        circumference=C, gamma=479.6, mass_kg=m_p, charge_coulomb=e,
        alpha_array=np.atleast_1d(3.2163e-4),
        harmonic_list=np.atleast_1d(h),
        voltage_list=np.atleast_1d(V),
        phi_offset_list=np.atleast_1d(1.0 + np.pi),  # non-zero RF phase
        p_increment=0,
        # zeta0 not provided -> should auto-centre
    )

    # Bucket must have non-zero width
    assert bucket.z_right > bucket.z_left, (
        f"Bucket has zero or negative width: z_left={bucket.z_left}, "
        f"z_right={bucket.z_right}")

    width = bucket.z_right - bucket.z_left
    zmax = C / (2 * h)
    # Width should be on the order of the bucket length
    assert width > 0.5 * zmax, (
        f"Bucket width {width} is too small compared to zmax {zmax}")


def test_rfbucket_autocentre_matcher():
    """RFBucketMatcher must succeed with auto-centred bucket (#884)."""
    from xpart.longitudinal.rf_bucket import RFBucket
    from xpart.longitudinal.rfbucket_matching import (
        RFBucketMatcher, QGaussianDistribution)

    C, h, V = 26658.883, 35640, 6e6
    zmax = C / (2 * h)

    bucket = RFBucket(
        circumference=C, gamma=479.6, mass_kg=m_p, charge_coulomb=e,
        alpha_array=np.atleast_1d(3.2163e-4),
        harmonic_list=np.atleast_1d(h),
        voltage_list=np.atleast_1d(V),
        phi_offset_list=np.atleast_1d(1.0 + np.pi),
        p_increment=0,
    )

    matcher = RFBucketMatcher(rfbucket=bucket,
                              distribution_type=QGaussianDistribution,
                              sigma_z=zmax / 4)
    # This must not raise ZeroDivisionError
    result = matcher.generate(macroparticlenumber=1000)
    z, dp = result[0], result[1]
    assert len(z) == 1000
    assert len(dp) == 1000


def test_rfbucket_explicit_zeta0_still_works():
    """Providing explicit zeta0 must still work as before."""
    from xpart.longitudinal.rf_bucket import RFBucket

    C, h, V = 26658.883, 35640, 6e6

    bucket = RFBucket(
        circumference=C, gamma=479.6, mass_kg=m_p, charge_coulomb=e,
        alpha_array=np.atleast_1d(3.2163e-4),
        harmonic_list=np.atleast_1d(h),
        voltage_list=np.atleast_1d(V),
        phi_offset_list=np.atleast_1d(np.pi),
        p_increment=0,
        zeta0=0.0,
    )

    assert bucket.z_right > bucket.z_left
    # Symmetric bucket centred at 0
    assert abs(bucket.z_left + bucket.z_right) < 1e-10
