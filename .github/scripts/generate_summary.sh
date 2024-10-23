#!/bin/bash
# copyright ############################### #
# This file is part of the Xsuite project.  #
# Copyright (c) CERN, 2024.                 #
# ######################################### #
set -xe

echo "## Test Summary $1"

results_file="reports/$1/results.txt"

if [ -f "$results_file" ]; then
  # Results file found, processing...
  sed -i -e 's/\x1b\[[0-9;]*m//g' -e 's/^> /\\> /g' $results_file

  passed=$(grep -c PASSED $results_file || true)
  failed=$(grep "FAILED.*xsuite" $results_file | grep -P 'FAILED.* - ' | sed -E 's/.*\] (.*::[^ ]+).* - .*/\1/' | sort | uniq | wc -l)
  skipped=$(grep -c SKIPPED $results_file || true)

  echo "| Result     | Number   |"
  echo "|------------|----------|"
  echo "| Passed ✅  | $passed  |"
  echo "| Failed ❌  | $failed  |"
  echo "| Skipped ⏭️ | $skipped |"

  if [ $failed -ne 0 ]; then
    echo "### 🔴 Failed Tests"
    grep "FAILED.*xsuite" $results_file | grep -P 'FAILED.* - ' | sed -E 's/.*\] (.*::[^ ]+).* - (.*)/\1 - \2/' | sort | uniq | while read -r failure; do
      echo "- $failure"

      echo "<details><summary>Click here to view the error details</summary><code>"
      # Extract the failure name
      test_name=$(echo "$failure" | sed -E 's/.*::([^\-]+).* - .*/\1/' | sed -E 's/\x1b\[[0-9;]*m//g' )
      test_name=$(echo "$test_name" | sed 's/[][]/\\&/g')
      # Find the start of the error block
      error_start_line=$(grep -n "____________________ ${test_name} ____________________" $results_file | cut -d: -f1)
      # Debug: Start line found at $error_start_line
      error_end_line=$(tail -n +$((error_start_line + 1)) $results_file | grep -nm 1 "^-.*Captured stdout call.*-$" | cut -d: -f1)
      if [[ ! -z "$error_start_line" ]]; then
        error_end_line=$(tail -n +$((error_start_line + 1)) $results_file | grep -nm 1 "^-.*Captured stdout call.*-$" | cut -d: -f1)
        if [[ ! -z "$error_end_line" ]]; then
            # Find the end of the error block
            absolute_error_end_line=$((error_start_line + error_end_line - 1))
            sed -n "${error_start_line},${absolute_error_end_line}p" $results_file | sed 's/^>/\\>/'
        fi
      fi
      echo "</code></details>"
    done
  fi
else
  echo "No test results found."
fi
