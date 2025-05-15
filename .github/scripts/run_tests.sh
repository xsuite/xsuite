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

# We want the tests to be terminated (quickly!) when this script is terminated
# GitHub gives us 7.5s before sending a SIGKILL to all child processes
_term() {
  echo "Received a SIGINT/SIGKILL signal. Terminating."
  kill -TERM "$PYTEST_PID"
}
trap _term SIGINT SIGTERM

# Pytest options
PYTEST_OPTS="--durations=0 --durations-min=1 --color=yes --verbose $PYTEST_ADDOPTS"

# Keep track of failures
STATUS=0

# Make nice annotations in the GitHub Actions logs
pip install pytest-github-actions-annotate-failures
export GITHUB_ACTIONS=true

run_pytest() {
  pytest $PYTEST_OPTS "$1" &
  PYTEST_PID=$!
  wait $PYTEST_PID || PYTEST_STATUS=$?
}

# If xtrack on Pyopencl context, run tests one by one, otherwise run normally
if [[ $XOBJECTS_TEST_CONTEXTS =~ "ContextPyopencl" ]] && [[ $* =~ xsuite/(xtrack|xpart|xfields) ]]; then
  # Run tests one by one
  for test_file in "$@"/test_*; do
      run_pytest "$test_file"

      # If the tests failed, set the status to 1 (5 is for no tests collected)
      if [ $PYTEST_STATUS -ne 0 ] && [ $PYTEST_STATUS -ne 5 ]; then
        STATUS=1
      fi
  done
else  # Run tests normally if no Pyopencl context
  # Use multithreading if on cpu context and not xmask
  if [[ $XOBJECTS_TEST_CONTEXTS =~ "ContextCpu" ]] && [[ ! $* =~ xsuite/(xmask|xcoll) ]]; then
    pip install pytest-xdist
    PYTEST_OPTS="$PYTEST_OPTS -nauto"
  fi

  run_pytest "$@"

  # If the tests failed, set the status to 1 (5 is for no tests collected)
  if [ $PYTEST_STATUS -ne 0 ] && [ $PYTEST_STATUS -ne 5 ]; then
    STATUS=1
  fi
fi

exit $STATUS
