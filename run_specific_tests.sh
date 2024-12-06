set -e # Exit immediately if a command exits with a non-zero status.

WF_BRANCH="main"

XOBJECTS=xsuite:main
   XPART=xsuite:main
   XDEPS=xsuite:release/0.8.2
  XTRACK=xsuite:feature/aperture_plot
 XFIELDS=xsuite:release/0.21.3
   XMASK=xsuite:main
   XCOLL=xsuite:main

python run_on_gh.py --suites xt --platform pcbe-abp-gpu001 --ctx cpu \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH \
  --pytest-opts '-k test_madnginterface'
