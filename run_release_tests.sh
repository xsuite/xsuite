set -e # Exit immediately if a command exits with a non-zero status.

WF_BRANCH="feature/thick_cavity" # xsuite branch

XOBJECTS=xsuite:main
   XPART=xsuite:main
   XDEPS=xsuite:main
  XTRACK=xsuite:merge/misalign_optimize
 XFIELDS=xsuite:main
   XMASK=xsuite:main
   XCOLL=xsuite:main
  XWAKES=xsuite:main

# GPU tests
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform alma --ctx cuda \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --xw $XWAKES --branch $WF_BRANCH \
  --pytest-opts "-m context_dependent"

python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform ubuntu --ctx cl \
   --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --xw $XWAKES --branch $WF_BRANCH \
   --pytest-opts "-m context_dependent"

# # CPU tests
# python run_on_gh.py --suites xm --platform alma-cpu-smaller --ctx cpu \
#   --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --xw $XWAKES --branch $WF_BRANCH
# python run_on_gh.py --suites xo,xp,xd,xt,xf,xc,xw --platform  alma-cpu-2 --ctx cpu:auto \
#   --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --xw $XWAKES --branch $WF_BRANCH
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc,xw --platform alma-cpu-1 --ctx cpu \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --xw $XWAKES --branch $WF_BRANCH
