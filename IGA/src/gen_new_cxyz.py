#!/usr/bin/env python3
# Created: Mar, 03, 2025 11:20:01 by Wataru Fukuda

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\

""")
  # parser.add_argument("file", metavar="input-file", help="input file")
  parser.add_argument("-o", "--output", metavar="output-file", default="output", help="output file")
  parser.add_argument("-i", "--input", type=int, default=1, help="input data")
  parser.add_argument("-m", "--multiple", type=float, nargs='*', default=[1,2], help="input data")
  options = parser.parse_args()
  import os
  import numpy

  # cxyz = numpy.array(([0,0],[0.2,-0.2],[0.8,-0.8],[1,-1],
  #                     [0,0.4],[0.3,0.3],[1.2,0],[1.5,-0.1],
  #                     [0,1.6],[0.3,1.7],[1.2,2.0],[1.5,2.1],
  #                     [0,2],[0.2,2.2],[0.8,2.8],[1,3]),dtype=">f8")
  cxyz = numpy.loadtxt("plot.txt",dtype=">f8")
  cxyz.tofile("cxyz_new")


if(__name__ == '__main__'):
  main()

