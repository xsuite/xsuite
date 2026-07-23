Lost particle state codes
=========================
Particles lost by the simulation have ``Particles.state <= 0``. Different states
are used to identify different particle loss events.

========= ==================================  ==============================================================================
State C   flag                                Information
========= ==================================  ==============================================================================
0         XT_LOST_ON_APERTURE                 Lost on explicit aperture element (e.g. ``LimitRect``, ``LimitEllipse`` etc.).
-1        XP_LOST_ON_GLOBAL_AP                Lost on global aperture limit set in the tracker.
-2        XT_LOST_ON_LONG_CUT                 Lost due to a longitudinal cut.
-10       XT_LOST_ALL_E_IN_SYNRAD             Lost all energy in synchrotron radiation.
-11       XF_OUTSIDE_INTERPOL                 Found outside interpolation grid.
-12       XF_TOO_MANY_PHOTONS                 Too many photons in beamstrahlung.
-20       RNG_ERR_SEEDS_NOT_SET               Random generator seeds not set.
-21       RNG_ERR_INVALID_TRACK               Invalid tracking inside random generator element.
-22       RNG_ERR_RUTH_NOT_SET                Random Rutherford parameters not set.
-30       XT_FULL_BEND_BACKTR                 Backtracking in full bend is not implemented yet.
-31       XT_MULTIP_IN_BEND_BACKTR            Backtracking in multipolar kick for bend is not implemented yet.
-32       XT_DIP_EDGE_FULL_BACKTR             Backtracking in full dipole edge is not implemented yet.
-33       XT_SPIN_BACKTRACK                   Backtracking with spin on.
-40       XT_INVALID_SLICE_TRANSFORM          Invalid slice transform.
-41       XT_INVALID_CURVED_SLICE_TRANSFORM   Invalid curved slice transform.
-300      XC_LOST_WITHOUT_SPEC                Lost in Xcoll but no specific cause recorded.
-330      XC_LOST_ON_MATERIAL                 Primary loss in an Xcoll material element (block, collimator, crystal).
-331      XC_LOST_ON_MATERIAL_SEC             Secondary loss in an Xcoll material element (block, collimator, crystal).
-350      XC_VIRTUAL_ENERGY                   Primary loss: Not a real particle: Virtual energy deposition.
-351      XC_VIRTUAL_ENERGY_SEC               Secondary loss: Not a real particle: Virtual energy deposition.
-352      XC_MASSLESS_OR_NEUTRAL              Secondary loss: Massless or neutral particle.
-353      XC_EXCITED_ION_STATE                Secondary loss: An excited state of an ion (not supported by BDSIM or FLUKA).
-390      XC_ERR_INVALID_TRACK                Invalid track through Xcoll element.
-391      XC_ERR_NOT_IMPLEMENTED              Not implemented in Xcoll.
-392      XC_ERR_INVALID_XOFIELD              Invalid xofield in Xcoll element.
-399      XC_ERR                              Unknown Xcoll error.
-400      XT_LOST_IN_RF_TRACK                 Lost in RF-Track
-100XXXX                                      Used to handle coasting
========= ==================================  ==============================================================================

Alive particle state codes
==========================
As long as particles are alive in the simulation, they have ``Particles.state > 0``.
Normally, alive particles always have state `1`, but specific studies might need
different alive states (like, to track secondary particles in collimation
simulations as in `this example <https://github.com/xsuite/xcoll/blob/main/examples/lossmap_identify_primary_losses.py>`__).

========= ==================================  ==============================================================================
State C   flag                                Information
========= ==================================  ==============================================================================
 1                                            Default alive state.
 301      XC_SECONDARY_PARTICLE               The particle has scattered off an Xcoll material element before.
 302      XC_HIT_ON_FLUKA                     Temporary variable to register hits (should not be present in final states).
 303      XC_HIT_ON_FLUKA_SEC                 Temporary variable to register hits (should not be present in final states).
 304      XC_HIT_ON_GEANT4                    Temporary variable to register hits (should not be present in final states).
 305      XC_HIT_ON_GEANT4_SEC                Temporary variable to register hits (should not be present in final states).
========= ==================================  ==============================================================================
