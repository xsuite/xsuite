set -e # Exit immediately if a command exits with a non-zero status.

XOBJECTS=xsuite:release/0.2.10
   XPART=xsuite:main
   XDEPS=xsuite:release/v0.5.0
  XTRACK=xsuite:release/0.46.2
 XFIELDS=xsuite:release/0.14.1
   XMASK=xsuite:main
   XCOLL=xsuite:main

python run_on_gh.py --suites xm --platform pcbe-abp-gpu001-1 --ctx cpu \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform alma --ctx cpu:auto \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform alma-cpu --ctx cpu \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform pcbe-abp-gpu001-2 --ctx cuda:3 \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK
python run_on_gh.py --suites xo,xp,xd,xt,xf,xc --platform ubuntu --ctx cl \
  --xo $XOBJECTS --xp $XPART --xd $XDEPS --xt $XTRACK --xf $XFIELDS --xm $XMASK