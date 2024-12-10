#!/bin/sh
# Created: Dec, 10, 2024 18:19:28 by Wataru Fukuda
set -eu

if [ $# -eq 2 ]; then
  ELE_X=$1
  ELE_Y=$2
  ./gen_mesh_FEM.py -o MESH_FEM_2D -e $ELE_X -e $ELE_Y -s 0 $ELE_X -s 0 $ELE_Y -p 1
elif [ $# -eq 3 ]; then
  ELE_X=$1
  ELE_Y=$2
  ELE_Z=$3
  ./gen_mesh_FEM.py -o MESH_FEM_3D -e $ELE_X -e $ELE_Y -e $ELE_Z -s 0 $ELE_X -s 0 $ELE_Y -s 0 $ELE_Z -p 1
else
  echo "the number of input should be 2 or 3"
fi
