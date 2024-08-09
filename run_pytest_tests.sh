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

run_tests(){
    local platform=$1
    local context=$2
    local options=$3

    echo "Running on $platform with $context and options: '$options'"

    python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform "$platform" --ctx "$context" \
        --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH --pytest-opts $options

    python run_on_gh.py --suites xm --platform pcbe-abp-gpu001 --ctx cpu \
        --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK --xc $XCOLL --branch $WF_BRANCH --pytest-opts $options
}

platform="$1"
context="$2"
pytest_opts="$3"

run_tests "$platform" "$context" "$pytest_opts"
