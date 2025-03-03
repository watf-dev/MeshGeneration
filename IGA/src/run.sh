#!/bin/sh
# Created: Mar, 01, 2025 16:07:43 by Wataru Fukuda
set -eu

# ./gen_square.py -o MESH_2D -e 3 -e 3 -s 0 6 -s 0 6 -p 3 -p 3 -n 2
./gen_square.py -o MESH_2D -e 2 -e 2 -s 0 6 -s 0 6 -p 2 -p 2 -n 2
gen_bien.py MESH_2D/patch.cfg
gen_xdmf_wataf.py MESH_2D/patch-b.cfg -o mesh.xmf2

./gen_new_cxyz.py
cp -r MESH_2D MESH_2D_new
cd MESH_2D_new
ln -sf ../cxyz_new cxyz
cd ..
gen_bien.py MESH_2D_new/patch.cfg
gen_xdmf_wataf.py MESH_2D_new/patch-b.cfg -o mesh_new.xmf2

mkdir -p EDGE_DATA
# ./b2e.py MESH_2D/patch.cfg -i MESH_2D -d 11 --outdir MESH.FEM
# gen_xdmf_wataf.py MESH.FEM/mesh.cfg -o mesh_FEM.xmf2
./b2e.py MESH_2D_new/patch.cfg -i MESH_2D_new -d 3 --outdir MESH.FEM_d3
gen_xdmf_wataf.py MESH.FEM_d3/mesh.cfg -o mesh_FEM_d3.xmf2
./b2e.py MESH_2D_new/patch.cfg -i MESH_2D_new -d 5 --outdir MESH.FEM_d5
gen_xdmf_wataf.py MESH.FEM_d5/mesh.cfg -o mesh_FEM_d5.xmf2
./b2e.py MESH_2D_new/patch.cfg -i MESH_2D_new -d 7 --outdir MESH.FEM_d7
gen_xdmf_wataf.py MESH.FEM_d7/mesh.cfg -o mesh_FEM_d7.xmf2
# ./b2e.py MESH_2D_new/patch.cfg -i MESH_2D_new -d 101 --outdir MESH.FEM_d101
# gen_xdmf_wataf.py MESH.FEM_d101/mesh.cfg -o mesh_FEM_d101.xmf2
./b2e.py MESH_2D_new/patch.cfg -i MESH_2D_new -d 21 --outdir MESH.FEM_d21
gen_xdmf_wataf.py MESH.FEM_d21/mesh.cfg -o mesh_FEM_d21.xmf2
./b2e.py MESH_2D_new/patch.cfg -i MESH_2D_new -d 11 --outdir MESH.FEM_d11 --make_data
gen_xdmf_wataf.py MESH.FEM_d11/mesh.cfg -o mesh_FEM_d11.xmf2
