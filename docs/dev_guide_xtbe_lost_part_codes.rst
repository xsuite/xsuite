Lost particles state codes
==========================
Particles lost by the simulation have Particles.state <= 0. Different states
are used to identify different particle loss events.

=====  ==================================================================
State  Information
=====  ==================================================================
0      Lost on explicit aperture element (e.g. LimitRect, LimitEllip etc.).
-1     Lost on global aperture limit set in the tracker.
-10    Lost all energy in synchrotron radiation.
-11    Found outside interpolation grid.
-333   Lost in collimator.
=====  ==================================================================
