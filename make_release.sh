#! /bin/bash
# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2024.                 #
# ######################################### #

set -e

get_latest_version () {
  pip index versions "$1" \
  | grep 'LATEST' \
  | sed -E -e 's/[ ]*LATEST:[ ]*([0-9.]+)/\1/g'
}

update_version () {
  local package=$1
  local version=$2
  sed -i '' -E -e "s/$package==[0-9.]+/$package==$version/g" "pyproject.toml"
}

for package in xtrack xfields xcoll xobjects; do
  latest_version=$(get_latest_version $package)
  update_version $package $latest_version
done
