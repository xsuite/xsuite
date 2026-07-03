#!/bin/bash
# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2024.                 #
# ######################################### #
set -xe

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/ci_common.sh"

component_source_prefix="$(mktemp -d)"

for project in "${repos[@]}"; do
  clone_project "$project" "$component_source_prefix"
done

python -m pip install --upgrade pip
python -m pip install packaging
python -m pip install --force-reinstall xsuite xmask xwakes

python - "$component_source_prefix" <<'PY'
import ast
import importlib.metadata
import re
import sys
from pathlib import Path

from packaging.version import Version

component_source_prefix = Path(sys.argv[1])
packages = [
    "xobjects",
    "xdeps",
    "xpart",
    "xtrack",
    "xfields",
    "xmask",
    "xcoll",
    "xwakes",
]


def read_dunder_version(path):
    module = ast.parse(path.read_text())
    for node in module.body:
        if (
            isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "__version__"
                    for target in node.targets)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            return node.value.value
    raise RuntimeError(f"Could not find __version__ assignment in {path}")


def read_pyproject_version(path):
    text = path.read_text()
    match = re.search(r'^version\s*=\s*"([^"]+)"\s*$', text, re.MULTILINE)
    if not match:
        raise RuntimeError(f"Could not find static project version in {path}")
    return match.group(1)


def source_version(package):
    package_path = component_source_prefix / package
    version_file = package_path / package / "_version.py"
    if version_file.exists():
        return read_dunder_version(version_file)

    if package == "xcoll":
        return read_pyproject_version(package_path / "pyproject.toml")

    raise RuntimeError(f"Do not know how to get source version for {package}")


source_versions = {
    package: source_version(package)
    for package in packages
}
pypi_versions = {
    package: importlib.metadata.version(package)
    for package in packages
}

print("Package versions:")
for package in packages:
    print(
        f"  {package}: cloned repo {source_versions[package]} | "
        f"PyPI install {pypi_versions[package]}"
    )

mismatches = [
    package for package in packages
    if Version(source_versions[package]) != Version(pypi_versions[package])
]

if mismatches:
    print("Version mismatch between cloned repos and PyPI packages:")
    for package in mismatches:
        print(
            f"  {package}: cloned repo has {source_versions[package]}, "
            f"PyPI has {pypi_versions[package]}"
        )
    sys.exit(1)
PY
