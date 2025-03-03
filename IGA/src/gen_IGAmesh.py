#!/usr/bin/env python3
# Created: Mar, 02, 2025 16:47:07 by Wataru Fukuda

import numpy
from scipy.special import comb

class BernsteinPolynomials:
  def __init__(self,p):
    self.p=p
  def getValues(self,xi):
    BP = numpy.zeros(self.p+1,dtype=">f8")
    for i in range(self.p+1):
      BP[i] = comb(self.p,i) * xi**i * (1-xi)**(self.p-i)
    return BP

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\

""")
  parser.add_argument("config", metavar="input-file", help="input config file")
  parser.add_argument("-i", "--input_dir", metavar="input-file", default="input", help="input dir")
  parser.add_argument("-o", "--output", metavar="output-file", default="output", help="output file")
  parser.add_argument("--outdir", default="MESH.FEM")
  parser.add_argument("-d","--divide",default=101,type=int,help="divide number")
  options = parser.parse_args()
  import os

  C = numpy.fromfile(os.path.join(options.input_dir,"C"),dtype=">f8")
  C_offset = numpy.fromfile(os.path.join(options.input_dir,"C_offset"),dtype=">i4")
  orders = numpy.fromfile(os.path.join(options.input_dir,"order"),dtype=">i4")
  cxyz = numpy.fromfile(os.path.join(options.input_dir,"cxyz"),dtype=">f8").reshape(-1,2)
  ien = numpy.fromfile(os.path.join(options.input_dir,"ien"),dtype=">i4")
  ien_offset = numpy.fromfile(os.path.join(options.input_dir,"ien_offset"),dtype=">i4")

  order = orders[0]
  BP = BernsteinPolynomials(orders[0])
  divide = options.divide
  xi = numpy.arange(0,divide,dtype=">f8")/(divide-1)
  xi_edge = numpy.array(([0,1]),dtype=">f8")
  BB = []
  for x2 in xi:
    for x1 in xi:
      if x2 == 0 or x2 == 1:
        BB_ = []
        for j in range(order+1):
          for i in range(order+1):
            BB_.append(BP.getValues(x1)[i]*BP.getValues(x2)[j])
        BB.append(BB_)
  BB = numpy.array(BB,dtype=">f8")

  N = []
  for i in range(len(C_offset)-1):
    C_ele = C[C_offset[i]:C_offset[i+1]]
    C_ele = numpy.array(C_ele,dtype=">f8").reshape((order+1)**2,(order+1)**2)
    N_ = numpy.dot(C_ele, BB.T)
    N.append(N_)
  N = numpy.array(N,dtype=">f8")

  result_xyz = []
  result_ien = []
  ele = divide-1
  for i in range(len(ien_offset)-1):
    ien_ = ien[ien_offset[i]:ien_offset[i+1]]
    xyz_ = cxyz[ien_].reshape(-1,2)
    result_xyz_ = numpy.dot(N[i].T, xyz_)
    result_xyz.append(result_xyz_)
    for k in range(ele):
      for j in range(ele):
        result_ien_ = [divide**2*i+divide*k+j,divide**2*i+divide*k+j+1,divide**2*i+divide*(k+1)+j+1,divide**2*i+divide*(k+1)+j]
        result_ien.append(result_ien_)
  result_xyz = numpy.array(result_xyz,dtype=">f8").reshape(-1,2)
  result_ien = numpy.array(result_ien,dtype=">i4").reshape(-1,4)

  import watfio
  nn = len(result_xyz)
  ne = result_ien.shape[0]
  data = watfio.ConfigData("FEM")
  data.setEndian("big")
  nen = 4
  nsd = 2
  npd = 2
  data.set("nn", nn)
  data.set("ne", ne)
  data.set("nen", nen)
  data.set("nsd", nsd)
  data.set("npd", npd)
  data.setHeavyData("xyz", result_xyz)
  data.setHeavyData("ien", result_ien)
  filename = os.path.join(options.outdir, "mesh.cfg")
  data.writeAll(filename)


if(__name__ == '__main__'):
  main()

