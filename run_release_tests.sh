set -e # Exit immediately if a command exits with a non-zero status.

WF_BRANCH="main"

XOBJECTS=xsuite:merge/compact_json
   XPART=xsuite:refactor/adapt_to_xtrack_replicas
   XDEPS=xsuite:feature/check_limits
  XTRACK=xsuite:refactor/replicas
 XFIELDS=xsuite:refactor/nocompounds
   XMASK=xsuite:main
   XCOLL=xsuite:main

# GPU tests
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform alma --ctx cuda \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --branch $WF_BRANCH
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform ubuntu --ctx cl \
   --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK

# CPU tests
python run_on_gh.py --suites xm --platform pcbe-abp-gpu001 --ctx cpu \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --branch $WF_BRANCH
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform  radeon --ctx cpu:auto \
   --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --branch $WF_BRANCH
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform alma-cpu --ctx cpu \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --branch $WF_BRANCH