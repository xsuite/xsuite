set -e # Exit immediately if a command exits with a non-zero status.

WF_BRANCH="main"

XOBJECTS=xsuite:release/v0.4.4
   XPART=xsuite:main
   XDEPS=xsuite:release/v0.6.3
  XTRACK=xsuite:release/v0.65.5
 XFIELDS=xsuite:release/v0.20.3
   XMASK=xsuite:main
   XCOLL=xsuite:main

# GPU tests
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform alma --ctx cuda \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform ubuntu --ctx cl \
   --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH

# CPU tests
python run_on_gh.py --suites xm --platform alma-cpu-2 --ctx cpu \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform  radeon --ctx cpu:auto \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform alma-cpu-1 --ctx cpu \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH
