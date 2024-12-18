#!/usr/bin/bash
# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2024.                 #
# ######################################### #
set -xe

# Expects the path to tests folder as the first argument
if [ $# -eq 0 ]; then
    echo "No arguments provided. Please provide the path to the tests folder."
    exit 1
fi

# Set the path to the reports folder
REPORTS_DIR="/opt/reports"

# Pytest options
PYTEST_OPTS="--color=yes --verbose"

# Keep track of failures
STATUS=0

# Make nice annotations in the GitHub Actions logs
pip install pytest-github-actions-annotate-failures
export GITHUB_ACTIONS=true

# If xtrack on Pyopencl context, run tests one by one, otherwise run normally
if [[ $XOBJECTS_TEST_CONTEXTS =~ "ContextPyopencl" ]] && [[ $* =~ xsuite/(xtrack|xpart|xfields) ]]; then
  # Run tests one by one
  for test_file in "$@"/test_*; do
      TEST_NAME=$(basename "$test_file" .py)  # strip path and extension
      pytest $PYTEST_OPTS "$test_file"
      PYTEST_STATUS=$?
      # If the tests failed, set the status to 1 (5 is for no tests collected)
      if [ $PYTEST_STATUS -ne 0 ] && [ $PYTEST_STATUS -ne 5 ]; then
        STATUS=1
      fi
  done
else  # Run tests normally if no Pyopencl context
  if [[ $XOBJECTS_TEST_CONTEXTS =~ "ContextCpu" ]]; then
    pip install pytest-xdist
    PYTEST_OPTS="$PYTEST_OPTS -nauto"
  fi

  pytest $PYTEST_OPTS "$@"
  PYTEST_STATUS=$?
  # If the tests failed, set the status to 1 (5 is for no tests collected)
  if [ $PYTEST_STATUS -ne 0 ] && [ $PYTEST_STATUS -ne 5 ]; then
    STATUS=1
  fi
fi

exit $STATUS
