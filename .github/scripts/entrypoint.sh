#!/usr/bin/env bash
set -e

source /opt/miniforge/etc/profile.d/conda.sh
conda activate base

exec "$@"
