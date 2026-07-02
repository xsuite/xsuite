#!/bin/bash
# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2024.                 #
# ######################################### #
set -xe

repos=(xobjects xdeps xpart xtrack xfields xmask xcoll xwakes)
xsuite_prefix="${xsuite_prefix:-.}"

# Expects the following environment variables:
# - $prefix, where to clone the packages
# - ${repo}_branch, where $repo is one of the repos above (replace - with _)
# - $precompile_kernels set to "true" or "false"
# - $install_mpi set to "true" or "false"
# - $install_from_pypi set to "true" or "false"

# Expect Xsuite already cloned by the main workflow
if [ "${precompile_kernels:-false}" == "false" ]; then
  export SKIP_KERNEL_BUILD=1
fi

if [ "${install_mpi:-false}" == "true" ]; then
  echo "::group::Installing MPI"
  mamba install -y openmpi
  pip install mpi4py
  echo "::endgroup::"
fi

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

if [ "${install_from_pypi:-false}" == "true" ]; then
  echo "::group::Installing test dependencies from source repos"
  test_source_prefix=$(mktemp -d)
  for project in "${repos[@]}"; do
    clone_project "$project" "$test_source_prefix"
    pip install "${cloned_project_path}[tests]"

    mkdir -p "${xsuite_prefix}/${project}"
    cp -a "${cloned_project_path}/." "${xsuite_prefix}/${project}/"
    rm -rf "${xsuite_prefix:?}/${project}/.git" "${xsuite_prefix:?}/${project}/${project}"
  done
  echo "::endgroup::"

  echo "::group::Installing xsuite from PyPI"
  pip install --force-reinstall xsuite xmask xwakes
  echo "::endgroup::"

  exit 0
fi

# Clone the repos and install them in the correct branch
for project in "${repos[@]}"; do
  echo "::group::Installing ${project}"
  clone_project "$project" "$xsuite_prefix"
  pip install -e "${cloned_project_path}[tests]"
  echo "::endgroup::"
done

echo "::group::Installing xsuite"
pip install --no-deps -v -e "${xsuite_prefix}/xsuite"
echo "::endgroup::"
