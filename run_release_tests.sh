set -e # Exit immediately if a command exits with a non-zero status.

WF_BRANCH="no_compile" # xsuite branch

XOBJECTS=xsuite:no_compile
   XPART=xsuite:main
   XDEPS=xsuite:main
  XTRACK=xsuite:no_compile
 XFIELDS=xsuite:main
   XMASK=xsuite:main
   XCOLL=xsuite:main
  XWAKES=xsuite:main

# CPU tests
python run_on_gh.py --suites xo,xd,xp,xt,xf,xc,xw --platform alma-cpu-1 --ctx cpu \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --xw $XWAKES --branch $WF_BRANCH \
  --allow-no-prebuilt-kernels

python run_on_gh.py --suites xo,xd,xp,xt,xf,xc,xw --platform alma-cpu-2 --ctx cpu:auto \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --xw $XWAKES --branch $WF_BRANCH \
  --allow-no-prebuilt-kernels

python run_on_gh.py --suites xp,xt,xf,xc,xw --platform alma-cpu-3 --ctx cpu \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --xw $XWAKES --branch $WF_BRANCH \
  --forbid-compile --precompile-kernels

python run_on_gh.py --suites xm --platform alma-cpu-smaller --ctx cpu,cpu:auto \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --xw $XWAKES --branch $WF_BRANCH \
  --forbid-compile --precompile-kernels

# GPU tests
python run_on_gh.py --suites xo,xd,xp,xt,xf,xc --platform alma2 --ctx cuda \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --xw $XWAKES --branch $WF_BRANCH \
  --pytest-opts "-m context_dependent" --forbid-compile --precompile-kernels

python run_on_gh.py --suites xo,xd,xp,xt,xf,xc --platform alma --ctx cl \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --xw $XWAKES --branch $WF_BRANCH \
  --pytest-opts "-m context_dependent" --timeout-minutes 2880 --forbid-compile --precompile-kernels

# MPI tests
python run_on_gh.py --suites xw --platform alma-cpu-small-1 --ctx cpu \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --xw $XWAKES --branch $WF_BRANCH \
  --with-mpi --forbid-compile --precompile-kernels
