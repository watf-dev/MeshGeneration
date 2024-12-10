#!/usr/bin/env python3
# Created: Oct, 30, 2024 20:20:23 by Wataru Fukuda

import math
import numpy
import os
import watfio

def gen_xyz_square(ni,ne,r,l):
  xyz = numpy.zeros(ni*2,dtype="f8").reshape(-1,2)
  np = 4
  nes = int(ni/np)
  for i in range(np):
    for e in range(nes):
      deg = 2*math.pi/(nes*np)*(i*nes+e)
      if( e <= nes / 2 ):
        r_tmp = (r/2+l/2)/math.cos(2*math.pi/(np*nes)*e)
      else:
        e_symmetry = nes - e
        r_tmp = (r/2+l/2)/math.cos(2*math.pi/(np*nes)*e_symmetry)
      xyz[(nes*i+e)][0] = r_tmp*math.cos(deg)
      xyz[(nes*i+e)][1] = r_tmp*math.sin(deg)
  return xyz

def gen_xyz(xyz_square,ni,ne,r,l):
  xyz = numpy.zeros(ni*(ne+1)*2, dtype="f8").reshape(-1,2)
  deg_ = 2*math.pi/ni
  for i in range(ni):
    xyz_outer = xyz_square[i]
    deg = deg_ * i
    x = (xyz_outer[0] - r*math.cos(deg))/ne
    y = (xyz_outer[1] - r*math.sin(deg))/ne
    for j in range(ne+1):
      xyz[(ne+1)*i+j][0] = r * math.cos(deg) + x * j
      xyz[(ne+1)*i+j][1] = r * math.sin(deg) + y * j
  return xyz

def gen_ien(ni,ne):
  ien = numpy.zeros(ni*ne*4,dtype="i4").reshape(-1,4)
  for i in range(ni):
    for j in range(ne):
      ien[(ne)*i+j][0] = (ne+1)*i + j
      ien[(ne)*i+j][1] = (ne+1)*i + j + 1
      ien[(ne)*i+j][2] = (ne+1)*(i+1) + j + 1
      ien[(ne)*i+j][3] = (ne+1)*(i+1) + j
  i = ne * (ni-1)
  for j in range(ne):
    ien[i + j][2] = j + 1
    ien[i + j][3] = j
  return ien

def get_ele_ave(xyz_square,ni):
  ele_l = []
  for i in range(int(ni/4)):
    xyz_top = xyz_square[int((ni/8)*3)+i]
    xyz_bottom = xyz_square[int((ni/8)*3)+i+1]
    ele_l.append(xyz_top[1] - xyz_bottom[1])
  ele_ave = sum(ele_l)/len(ele_l)
  return ele_ave

def gen_xyz_left(xyz_square,ni,ne):
  xyz = numpy.zeros(int((ni/4+1)*(ni/4)*2),dtype="f8").reshape(-1,2)
  ele_ave = get_ele_ave(xyz_square,ni)
  for i in range(int(ni/4+1)):
    xyz_top = xyz_square[int((ni/8)*3)+i]
    for j in range(int(ni/4)):
      xyz[int((ni/4)*i+j)][0] = xyz_top[0] - ele_ave*(j+1)
      xyz[int((ni/4)*i+j)][1] = xyz_top[1] 
  return xyz

def gen_ien_left(ni,ne):
  ien = numpy.zeros(int((ni/4)*(ni/4)*4),dtype="i4").reshape(-1,4)
  last = ni*(ne+1) - 1
  for i in range(int(ni/4)):
    for j in range(int(ni/4)):
      ien[int((ni/4)*i+j)][0] = last+(ni/4)*i+j
      ien[int((ni/4)*i+j)][1] = last+(ni/4)*i+j+1
      ien[int((ni/4)*i+j)][2] = last+(ni/4)*(i+1)+j+1
      ien[int((ni/4)*i+j)][3] = last+(ni/4)*(i+1)+j
  for i in range(int(ni/4)):
    ien[int((ni/4)*i)][0] = ni/8*(ne+1)*3 + (ne+1)*(i+1) - 1
    ien[int((ni/4)*i)][3] = ni/8*(ne+1)*3 + (ne+1)*(i+2) - 1
  return ien

def gen_xyz_right(xyz_square,ni,ne):
  xyz = numpy.zeros(int((ni/4+1)*(ni/4)*2),dtype="f8").reshape(-1,2)
  ele_ave = get_ele_ave(xyz_square,ni)
  for i in range(int(ni/4+1)):
    xyz_top = xyz_square[int((ni/8)*1)-i]
    for j in range(int(ni/4)):
      xyz[int((ni/4)*i+j)][0] = xyz_top[0] + ele_ave*(j+1)
      xyz[int((ni/4)*i+j)][1] = xyz_top[1] 
  return xyz

def gen_ien_right(ni,ne):
  ien = numpy.zeros(int((ni/4)*(ni/4)*4),dtype="i4").reshape(-1,4)
  last = ni*(ne+1) + (ni/4)*(ni/4+1) - 1
  for i in range(int(ni/4)):
    for j in range(int(ni/4)):
      ien[int((ni/4)*i+j)][0] = last+(ni/4)*i+j
      ien[int((ni/4)*i+j)][1] = last+(ni/4)*i+j+1
      ien[int((ni/4)*i+j)][2] = last+(ni/4)*(i+1)+j+1
      ien[int((ni/4)*i+j)][3] = last+(ni/4)*(i+1)+j
  for i in range(int(ni/4)):
    ien0 = ni/8*(ne+1)*1 - (ne+1)*(i-1) - 1
    ien3 = ni/8*(ne+1)*1 - (ne+1)*i - 1
    if ien0 < 0:
      ien0 += ni*(ne+1)
    if ien3 < 0:
      ien3 += ni*(ne+1)
    ien[int((ni/4)*i)][0] = ien0
    ien[int((ni/4)*i)][3] = ien3
  return ien

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
generate a cylinder mesh as FEM format
""")
  parser.add_argument("-o", "--output", metavar="output-file", default="output", help="output file")
  parser.add_argument("--ni",type=int,default=100,help="number of inner nodes")
  parser.add_argument("--ne",type=int,default=5,help="number of elements in the radius direction")
  parser.add_argument("--radius",type=float,default=1.0,help="radius")
  parser.add_argument("--length",type=float,default=5,help="length to outer edge")
  options = parser.parse_args()
  ni = options.ni
  ne = options.ne
  r = options.radius
  l = options.length

  ### make data
  xyz_square = gen_xyz_square(ni,ne,r,l)
  xyz = gen_xyz(xyz_square,ni,ne,r,l)
  ien = gen_ien(ni,ne)
  xyz_left = gen_xyz_left(xyz_square,ni,ne)
  ien_left = gen_ien_left(ni,ne)
  xyz_right = gen_xyz_right(xyz_square,ni,ne)
  ien_right = gen_ien_right(ni,ne)
  xyz = numpy.concatenate((xyz,xyz_left,xyz_right),axis=0)
  ien = numpy.concatenate((ien,ien_left,ien_right),axis=0)

  ### output
  nn = len(xyz)
  ne = len(ien)
  nsd = 2
  npd = 2
  nen = 4
  data = watfio.ConfigData("FEM")
  data.setEndian("big")
  data.set("nn",nn)
  data.set("ne",ne)
  data.set("nsd",nsd)
  data.set("npd",npd)
  data.set("nen",nen)
  data.setHeavyData("xyz",xyz)
  data.setHeavyData("ien",ien)
  output_dir = options.output
  data.writeAll(os.path.join(output_dir, "mesh.cfg"))


if(__name__ == '__main__'):
  main()

