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

# A temporary workaround for pyopencl not supporting numpy 2 in wheels
# TODO: Remove once pyopencl gets updated wheels
if [[ $XOBJECTS_TEST_CONTEXTS =~ "ContextPyopencl" ]]; then
  pip install 'numpy<2.0'
fi

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
        "$test_file" || STATUS=1
  done

  echo "Generating report..."
  pytest_html_merger -i "$REPORTS_DIR" -o "$REPORTS_DIR/report.html"
else
   # Run tests normally if no Pyopencl context
  pytest \
    --color=yes \
    --verbose \
    --html="$REPORTS_DIR/report.html" --self-contained-html \
    "$@" || STATUS=1
fi

exit $STATUS
