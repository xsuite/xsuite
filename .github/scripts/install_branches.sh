#!/bin/bash
# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2024.                 #
# ######################################### #
set -xe

repos=(xobjects xdeps xpart xtrack xfields xmask xcoll xsuite-kernels)
xsuite_prefix="${xsuite_prefix:-.}"

# Expects the following environment variables:
# - $prefix, where to clone the packages
# - ${repo}_branch, where $repo is one of the repos above (replace - with _)
# - $precompile_kernels set to "true" or "false"

for project in "${repos[@]}"; do
  branch_varname="${project//-/_}_branch"
  project_branch=${!branch_varname}  # get value of the variable [project]_branch

  IFS=':' read -r -a parts <<< "$project_branch"
  user="${parts[0]}"
  branch="${parts[1]}"

  cd "$xsuite_prefix"
  git clone \
    --recursive \
    --single-branch -b "$branch" \
    "https://github.com/${user}/${project}.git"

   if [ "$project" == "xsuite" ]; then
      if [ "${precompile_kernels:-false}" == "false" ]; then
          echo export SKIP_KERNEL_BUILD=1
      fi
      pip install --no-deps -e -v "${xsuite_prefix}/${project}"
  else
      pip install -e "${xsuite_prefix}/${project}[tests]"
  fi
done
