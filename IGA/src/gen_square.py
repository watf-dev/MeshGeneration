#!/usr/bin/env python3
# Created: Mar, 01, 2025 11:38:04 by Wataru Fukuda

import tafsmio
import numpy
import os
import nurbs.UniformBspline
import nurbs.bezier
from tafsm_nurbs.BezierExtraction import BezierExtraction

class NURBS2Bezier:
  def __init__(self, space, nes, orders, nsd):
    self.space = space
    self.nes = nes
    self.orders = orders
    self.nsd = nsd
  def genKnots(self):
    knots = []
    npd = len(self.nes)
    for i in range(npd):
      xne = self.nes[i]
      order = self.orders[i]
      knot  = nurbs.UniformBspline.UniformBspline.genKnotVector(xne, order)   # range : 0 ~ ne
      knots.append(knot)
    return knots
  def genXYZ(self):
    xyzs = []
    for i in range(len(self.nes)):
      ne_ = self.nes[i]
      order_ = self.orders[i]
      xyz = nurbs.UniformBspline.UniformBspline.genControlPoints(ne_, order_)
      x_range = self.space[i][0], self.space[i][1]
      for i in range(len(xyz)):
        xyz[i] = xyz[i]*(x_range[1]-x_range[0])+x_range[0]
      xyzs.append(xyz)
    return xyzs
  def genBezierOperator(self):
    knots = self.genKnots()
    Cs = []
    for i in range(len(self.orders)):
      kk = knots[i]
      order = self.orders[i]
      C = nurbs.bezier.extraction(order,kk)
      Cs.append(numpy.array(C))
    return Cs
  def toElementPosition(self, index, total):   # each element position from left bottom
    a = []
    for t in total:
      a.append(index % t)
      index //= t
    return a
  def toIEN(self, point_position, total):
    s = 0
    point_position_ = point_position[::-1]
    t_ = total[::-1]
    for point_position,t in zip(point_position_,t_):
      s *= t
      s += point_position
    return s
  def genMesh(self):
    # set data
    xyz = self.genXYZ()
    Cs = self.genBezierOperator()
    ne = 1
    for i in range(len(self.nes)):
      ne *= self.nes[i]
    nn = 1
    nns = []
    for i in range(len(self.nes)):
      nn *= len(xyz[i])
      nns.append(len(xyz[i]))

    # set data
    nns.append(len(self.nes))
    npd = len(self.nes)

    # set cxyz
    cxyz=numpy.zeros(nns, dtype=">f8")
    if(npd==2):
      for i in range(len(xyz[0])):
        cxyz[:,i,0] = xyz[0][i]
      for i in range(len(xyz[1])):
        cxyz[i,:,1] = xyz[1][i]
    else:
      print("error: npd 1,3 are not supported.")
      exit(1)
    cxyz = cxyz.reshape(nn,npd)

    nens = []
    nen = 1
    for i in range(npd):
      nens.append(self.orders[i]+1)
      nen *= nens[-1]

    ### set ien ###
    ien = []
    for i in range(ne):
      ele_position = numpy.array(self.toElementPosition(i, self.nes))
      for j in range(nen):
        ele_point_position = numpy.array(self.toElementPosition(j, nens))
        point_position = ele_position + ele_point_position
        ien_ = self.toIEN(point_position, nns)
        ien.append(ien_)

    ### set C_offset and ien_offset ###
    ien_offset = numpy.zeros((ne+1), dtype=">i4")
    C_offset = numpy.zeros((ne+1), dtype=">i4")
    size = ((self.orders[0]+1)**2)**2
    for i in range(ne):
      ien_offset[i+1] = ien_offset[i] + nen
      C_offset[i+1] = C_offset[i] + size

    ### set C ###
    knots = self.genKnots()
    BE = []
    for i in range(npd):
      BE_ = BezierExtraction(knots[i], self.orders[i])
      BE_.evaluate()
      BE_ = numpy.array(BE_.C,dtype=">f8")
      BE.append(BE_)

    C = []
    for j,ne_ in enumerate(self.nes):
      C_tmp = []
      for i in range(ne_):
        C_tmp.append(BE[j][i:i+self.orders[j]+1,self.orders[j]*i:self.orders[j]*i+self.orders[j]+1])
      C.append(C_tmp)
    C = numpy.array(C,dtype=">f8")

    Cout = []
    for j in range(self.nes[1]):
      for i in range(self.nes[0]):
        Cout_ = numpy.kron(C[1,j],C[0,i])
        Cout.append(Cout_)
    Cout = numpy.array(Cout, dtype=">f8")

    ### set order ##J#
    order_output = numpy.zeros((ne, npd), dtype=">i4")
    for i in range(npd):
      order_output[:,i] += self.orders[i]

    # prepare data for output
    data = tafsmio.ConfigData("bezier1")
    data.setEndian("small")
    data.set("nn", nn)
    data.set("ne", ne)
    data.set("nsd", self.nsd)
    data.set("max_npd", npd)
    data.setHeavyData("cxyz", cxyz.reshape((-1,self.nsd)))
    data.setHeavyData("order", order_output)
    data.setHeavyData("ien", numpy.array(ien))
    data.setHeavyData("ien_offset", ien_offset)
    data.setHeavyData("extraction-operator", Cout)
    data.setHeavyData("extraction-operator_offset", C_offset)
    return data

def main():
  import tafsm.argparse as argparse
  usage = "usage: %prog [options]"
  parser = argparse.ArgumentParser(usage,description=__doc__)
  parser.add_argument("-o","--outdir", default="MESH", help="output")
  parser.add_argument("-e","--ne",    type=int, action="append")
  parser.add_argument("-p","--order", type=int, action="append")
  parser.add_argument("-s","--space", nargs=2, type=float, action="append")
  parser.add_argument("-n","--nsd",  type=int)
  (options, args) = parser.parse_known_args()
  space = options.space
  ne = options.ne
  nsd = options.nsd
  orders = options.order

  mesh = NURBS2Bezier(space, ne, orders, nsd)
  data = mesh.genMesh()

  filename = os.path.join(options.outdir, "patch.cfg")
  data.writeAll(filename)

if __name__ == "__main__":
  main()

