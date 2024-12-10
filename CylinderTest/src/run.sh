#!/bin/sh
# Created: Oct, 29, 2024 19:14:10 by Wataru Fukuda
set -eu

MESH_DIR=MESH.cylinder_test
./gen_cylinder_mesh.py --ni 64 --ne 10 --radius 1.0 --length 5 -o $MESH_DIR
