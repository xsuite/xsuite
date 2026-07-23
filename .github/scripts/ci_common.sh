#!/bin/bash
# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2024.                 #
# ######################################### #

repos=(xobjects xdeps xpart xtrack xfields xmask xcoll xwakes)
xsuite_prefix="$(cd "${xsuite_prefix:-.}" && pwd)"

# Clone one Xsuite package into the requested prefix.
# The git ref is read from the matching environment variable, for example
# xtrack_branch=xsuite:main for project=xtrack.
# The cloned repository path is exposed as $cloned_project_path for callers.
clone_project() {
  project="$1"
  target_prefix="$2"
  branch_varname="${project//-/_}_branch"
  project_branch=${!branch_varname}  # get value of the variable [project]_branch

  IFS=':' read -r -a parts <<< "$project_branch"
  user="${parts[0]}"
  branch="${parts[1]}"

  echo "::notice::Cloning ${project} from ${user}:${branch}"
  cd "$target_prefix"
  git clone \
    --recursive \
    --single-branch -b "$branch" \
    "https://github.com/${user}/${project}.git"
  cloned_project_path="${target_prefix}/${project}"
}
