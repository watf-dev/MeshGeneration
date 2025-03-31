#!/usr/bin/env python3
# Created: Oct, 25, 2024 19:04:41 by Wataru Fukuda

import os
import watfio
from watfmesh.MeshGeneration import MeshGeneration

# DEBUG = True
DEBUG = False

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""
  generate FEM mesh
""")
  parser.add_argument("-o","--outdir", default="MESH_FEM", help="output")
  parser.add_argument("-e","--nes", type=int, action="append")
  parser.add_argument("-s","--space", nargs=2, type=float, action="append")
  parser.add_argument("-p","--order", type=int)
  (options, args) = parser.parse_known_args()
  space = options.space
  nes = options.nes
  orders = options.order

  mesh = MeshGeneration(space, nes, orders)
  nn = mesh.genNN()
  ne = mesh.genNE()
  nen = mesh.genNEN()
  nsd = mesh.genNSD()
  npd = mesh.genNPD()
  mxyz = mesh.genMXYZ()
  mien = mesh.genMIEN()
  mrng = mesh.genMRNG()

  data = watfio.ConfigData("FEM2")
  data.setEndian("big")
  data.set("nn", nn)
  data.set("ne", ne)
  data.set("nen", nen)
  data.set("nsd", nsd)
  data.set("npd", npd)
  data.setHeavyData("xyz", mxyz)
  data.setHeavyData("ien", mien)
  data.setHeavyData("rng", mrng)
  filename = os.path.join(options.outdir, "mesh.cfg")
  data.writeAll(filename)


if __name__ == "__main__":
  main()

