#!/usr/bin/bash

# Expects the path to tests folder as the first argument
if [ $# -eq 0 ]; then
    echo "No arguments provided. Please provide the path to the tests folder."
    exit 1
fi

# Set the path to the reports folder
REPORTS_DIR="/opt/reports"

# Keep track of failures
STATUS=0

# If xtrack on Pyopencl context, run tests one by one, otherwise run normally
if [[ $XOBJECTS_TEST_CONTEXTS =~ "ContextPyopencl" ]] && [[ $* =~ xsuite/(xtrack|xpart|xfields) ]]; then
  # Run tests one by one
  pip install pytest-html-merger

  for test_file in "$@"/test_*; do
      TEST_NAME=$(basename "$test_file" .py)  # strip path and extension
      echo "Running test $TEST_NAME..."
      pytest \
        --color=yes \
        --verbose \
        --html="$REPORTS_DIR/report-$TEST_NAME.html" --self-contained-html \
        "$test_file"
      PYTEST_STATUS=$?
      # If the tests failed, set the status to 1 (5 is for no tests collected)
      if [ $PYTEST_STATUS -ne 0 ] && [ $PYTEST_STATUS -ne 5 ]; then
        STATUS=1
      fi
  done

  echo "Generating report..."
  pytest_html_merger -i "$REPORTS_DIR" -o "$REPORTS_DIR/report.html"
else
  # Run tests normally if no Pyopencl context
  pytest \
    --color=yes \
    --verbose \
    --html="$REPORTS_DIR/report.html" --self-contained-html \
    "$@"
  PYTEST_STATUS=$?
  # If the tests failed, set the status to 1 (5 is for no tests collected)
  if [ $PYTEST_STATUS -ne 0 ] && [ $PYTEST_STATUS -ne 5 ]; then
    STATUS=1
  fi
fi

exit $STATUS
