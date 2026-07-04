#!/bin/bash
# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2024.                 #
# ######################################### #
set -xe

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/ci_common.sh"

# Expects the following environment variables:
# - $xsuite_prefix, where to clone the packages
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
  pip uninstall -y xsuite "${repos[@]}"
  pip install --upgrade xsuite xmask xwakes
  pip check
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
