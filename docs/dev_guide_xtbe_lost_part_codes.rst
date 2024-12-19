Lost particles state codes
==========================
Particles lost by the simulation have Particles.state <= 0. Different states
are used to identify different particle loss events.

========= ==========================  ====================================================================
State C   flag                        Information
========= ==========================  ====================================================================
0         XT_LOST_ON_APERTURE         Lost on explicit aperture element (e.g. LimitRect, LimitEllip etc.).
-1        XP_LOST_ON_GLOBAL_AP        Lost on global aperture limit set in the tracker.
-2        XT_LOST_ON_LONG_CUT         Lost due to a longitudinal cut.
-10       XT_LOST_ALL_E_IN_SYNRAD     Lost all energy in synchrotron radiation.
-11       XF_OUTSIDE_INTERPOL         Found outside interpolation grid.
-12       XF_TOO_MANY_PHOTONS         Too many photons in beamstrahlung.
-20       RNG_ERR_SEEDS_NOT_SET       Random generator seeds not set.
-21       RNG_ERR_INVALID_TRACK       Invalid tracking inside random generator element.
-22       RNG_ERR_RUTH_NOT_SET        Random Rutherford parameters not set.
-30       XT_FULL_BEND_BACKTR         Backtracking in full bend non implemented yet.
-31       XT_MULTIP_IN_BEND_BACKTR    Backtracking in multipolar kick for bend non implemented yet.
-32       XT_DIP_EDGE_FULL_BACKTR     Backtracking in full dipole edge non implemented yet.
-330      XC_LOST_ON_EVEREST_BLOCK    Lost in an Everest block.
-331      XC_LOST_ON_EVEREST_COLL     Lost in an Everest collimator.
-332      XC_LOST_ON_EVEREST_CRYSTAL  Lost in an Everest crystal.
-333      XC_LOST_ON_FLUKA_BLOCK      Lost in a FLUKA insertion (not yet implemented).
-334      XC_LOST_ON_FLUKA_COLL       Lost in a FLUKA collimator.
-335      XC_LOST_ON_FLUKA_CRYSTAL    Lost in a FLUKA crystal (not yet implemented).
-336      XC_LOST_ON_GEANT4_BLOCK     Lost in a Geant4 insertion (not yet implemented).
-337      XC_LOST_ON_GEANT4_COLL      Lost in a Geant4 collimator.
-338      XC_LOST_ON_GEANT4_CRYSTAL   Lost in a Geant4 crystal (not yet implemented).
-340      XC_LOST_ON_ABSORBER         Lost in a black absorber.
-390      XC_ERR_INVALID_TRACK        Invalid tracking in collimator (e.g. backtracking, during twiss).
-391      XC_ERR_NOT_IMPLEMENTED      The particle went to a part of the code that is not supported.
-392      XC_ERR_INVALID_XOFIELD      At least one collimator has unsupported values for its parameters.
-399      XC_ERR                      General Xcoll error.
-400      XT_LOST_IN_RF_TRACK         Lost in RF-Track
-100XXXX                              Used to handle coasting
========= ==========================  ====================================================================
