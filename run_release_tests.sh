set -e # Exit immediately if a command exits with a non-zero status.

WF_BRANCH="main"

XOBJECTS=xsuite:main
   XPART=xsuite:main
   XDEPS=xsuite:merge/from_riccardo
  XTRACK=xsuite:merge/from_riccardo
 XFIELDS=xsuite:main
   XMASK=xsuite:adapt/rename_orbit_corretion_name
   XCOLL=xsuite:main

# GPU tests
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform alma --ctx cuda \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform ubuntu --ctx cl \
   --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH

# CPU tests
python run_on_gh.py --suites xm --platform pcbe-abp-gpu001 --ctx cpu \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform  radeon --ctx cpu:auto \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform alma-cpu --ctx cpu \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH
