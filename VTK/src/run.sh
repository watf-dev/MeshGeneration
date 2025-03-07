#!/bin/sh
# Created: Mar, 07, 2025 20:20:30 by Wataru Fukuda
set -eu

BASE=$(readlink -f $(dirname $0))

if ls *.vtu 1> /dev/null 2>&1; then
  rm *.vtu
  echo "Removed .vtu files."
else
  echo "No .vtu files found."
fi

$BASE/test_all.py

