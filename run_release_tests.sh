set -e # Exit immediately if a command exits with a non-zero status.

WF_BRANCH="main"

XOBJECTS=xsuite:main
   XPART=xsuite:fix/repeated_elements
   XDEPS=xsuite:release/0.8.0
  XTRACK=xsuite:release/0.70.0
 XFIELDS=xsuite:main
   XMASK=xsuite:main
   XCOLL=xsuite:main

# GPU tests
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform alma --ctx cuda \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform ubuntu --ctx cl \
   --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH

# CPU tests
python run_on_gh.py --suites xm --platform alma-cpu-smaller --ctx cpu \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform  alma-cpu-2 --ctx cpu:auto \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform alma-cpu-1 --ctx cpu \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH
