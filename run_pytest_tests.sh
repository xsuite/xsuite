#!/bin/bash
set -e 

WF_BRANCH="pytest-csv"

XOBJECTS="xsuite:main"
XPART="xsuite:main"
XDEPS="xsuite:main"
XTRACK="xsuite:feature/twiss_ergonomics"
XFIELDS="xsuite:main"
XMASK="xsuite:main"
XCOLL="xsuite:main"

pytest_opts="-k test_buffer.py"

# GPU tests
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform alma-tests --ctx cuda \
    --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH --pytest-opts "$pytest_opts"
# python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform ubuntu --ctx cl \
#     --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH --pytest-opts "$pytest_opts"

# CPU tests
python run_on_gh.py --suites xm --platform test1 --ctx cpu \
    --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH --pytest-opts "$pytest_opts"
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform  test3 --ctx cpu:auto \
    --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH --pytest-opts "$pytest_opts"
# python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform alma-cpu-1 --ctx cpu \
#     --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH --pytest-opts "$pytest_opts"

