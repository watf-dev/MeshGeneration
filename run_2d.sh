#!/bin/sh
# Created: Oct, 27, 2024 21:07:23 by Wataru Fukuda

ELE_X=$1
ELE_Y=$2

./gen_mesh_FEM.py -o MESH_FEM_2D -e $ELE_X -e $ELE_Y -s 0 $ELE_X -s 0 $ELE_Y -p 1

