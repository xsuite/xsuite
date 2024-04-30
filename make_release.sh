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

verify_input() {
  read -p "Are you sure you want to continue? [y/N] " prompt
  if [[ $prompt != "y" && $prompt != "Y" ]]
  then
    exit 0
  fi
}

echo "=== THE CURRENT TAGGED VERSION ==="
git tag --sort=authordate | tail -n 1

echo "=== BUMPING VERSIONS: VERIFY I DID IT CORRECTLY ==="
for package in xtrack xfields xcoll xobjects; do
  latest_version=$(get_latest_version $package)
  update_version $package $latest_version
done

git diff -- pyproject.toml
verify_input

echo "=== WHAT SHOULD BE THE NEXT VERSION? ==="
read -p "Next version: " next_version
read -p "Retype the version: " retype_version

if [[ $next_version != $retype_version ]]
then
  echo "Versions do not match. Exiting."
  exit 1
fi

echo "=== WILL PROCEED TO TAG AND COMMIT NOW ==="
git add pyproject.toml
git commit -m "Bump versions"
git tag -a $next_version -m "Release $next_version"

echo "=== RUN THE FOLLOWING TO PUBLISH RELEASE: ==="
echo "git push --follow-tags"