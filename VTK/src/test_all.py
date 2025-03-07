#!/usr/bin/env python3
# Created: Mar, 07, 2025 14:51:42 by Wataru Fukuda

import vtk
import math

def exportBezier(ugrid, filename):
  writer = vtk.vtkXMLUnstructuredGridWriter()
  writer.SetInputData(ugrid)
  writer.SetFileName(filename + ".vtu")
  writer.SetDataModeToAscii()
  writer.Write()
  print(f"Exported: {filename}.vtu")

def test_VTK_BEZIER_CURVE_quadratic_quarter_circle():
  cp = vtk.vtkPoints()
  w = vtk.vtkDoubleArray()
  w.SetName("RationalWeights")
  w.SetNumberOfComponents(1)
  w.SetNumberOfTuples(3)
  cp.InsertNextPoint(0.0, 1.0, 0.0)
  cp.InsertNextPoint(1.0, 0.0, 0.0)
  cp.InsertNextPoint(1.0, 1.0, 0.0)
  w.SetValue(0, 1.0)
  w.SetValue(1, 1.0)
  w.SetValue(2, 2**0.5/2)
  ugrid = vtk.vtkUnstructuredGrid()
  ugrid.SetPoints(cp)
  ugrid.InsertNextCell(vtk.VTK_BEZIER_CURVE, 3, [0, 1, 2])
  ugrid.GetPointData().SetRationalWeights(w)
  exportBezier(ugrid, "VTK_BEZIER_CURVE_quadratic_quarter_circle")

def test_VTK_BEZIER_QUADRILATERAL_linearquadratic_quarter_disk():
  cp = vtk.vtkPoints()
  w = vtk.vtkDoubleArray()
  w.SetName("RationalWeights")
  w.SetNumberOfComponents(1)
  cp.InsertNextPoint(0.0, 1.0, 0.0)
  cp.InsertNextPoint(1.0, 0.0, 0.0)
  cp.InsertNextPoint(2.0, 0.0, 0.0)
  cp.InsertNextPoint(0.0, 2.0, 0.0)
  cp.InsertNextPoint(1.0, 1.0, 0.0)
  cp.InsertNextPoint(2.0, 2.0, 0.0)
  w.SetNumberOfTuples(6)
  w.SetValue(0, 1.0)
  w.SetValue(1, 1.0)
  w.SetValue(2, 1.0)
  w.SetValue(3, 1.0)
  w.SetValue(4, 2**0.5/2)
  w.SetValue(5, 2**0.5/2)
  p = vtk.vtkIntArray()
  p.SetName("HigherOrderDegrees")
  p.SetNumberOfComponents(3)
  p.InsertNextTuple3(2, 1, 0)
  ugrid = vtk.vtkUnstructuredGrid()
  ugrid.SetPoints(cp)
  ugrid.InsertNextCell(vtk.VTK_BEZIER_QUADRILATERAL, 6, [0, 1, 2, 3, 4, 5])
  ugrid.GetPointData().SetRationalWeights(w)
  ugrid.GetCellData().SetHigherOrderDegrees(p)
  exportBezier(ugrid, "VTK_BEZIER_QUADRILATERAL_linearquadratic_quarter_disk")

def test_VTK_BEZIER_TRIANGLE_quartic_sphereOctant():
  cp = vtk.vtkPoints()
  w = vtk.vtkDoubleArray()
  w.SetName("RationalWeights")
  w.SetNumberOfComponents(1)
  nPoints = 15
  pointIds = list(range(nPoints))
  c1 = (3**0.5 - 1) / (3**0.5)
  c2 = (3**0.5 + 1) / (2 * 3**0.5)
  c3 = 1 - (5 - 2**0.5) * (7 - 3**0.5) / 46
  points_list = [
    (1, 0, 0), (0, 1, 0), (0, 0, 1),
    (1, c1, 0), (c2, c2, 0), (c1, 1, 0),
    (0, 1, c1), (0, c2, c2), (0, c1, 1),
    (c1, 0, 1), (c2, 0, c2), (1, 0, c1),
    (1, c3, c3), (c3, 1, c3), (c3, c3, 1)
  ]
  for pt in points_list:
    cp.InsertNextPoint(pt)
  w.SetNumberOfTuples(nPoints)
  w1 = 4 * (3**0.5) * ((3**0.5) - 1)
  w2 = 3 * (2**0.5)
  w3 = (2 / 3)**0.5 * (3 + 2 * (2**0.5) - (3**0.5))
  rationalWeightsTps2 = [
    w1, w1, w1, w2, 4, w2, w2, 4, w2, w2, 4, w2, w3, w3, w3
  ]
  for i in range(nPoints):
    w.SetValue(i, rationalWeightsTps2[i])
  ugrid = vtk.vtkUnstructuredGrid()
  ugrid.SetPoints(cp)
  ugrid.InsertNextCell(vtk.VTK_BEZIER_TRIANGLE, nPoints, pointIds)
  ugrid.GetPointData().SetRationalWeights(w)
  exportBezier(ugrid, "VTK_BEZIER_TRIANGLE_quartic_sphereOctant")

def test_VTK_BEZIER_TRIANGLE_quadratic_full_disk():
  cp = vtk.vtkPoints()
  w = vtk.vtkDoubleArray()
  w.SetName("RationalWeights")
  w.SetNumberOfComponents(1)
  w.SetNumberOfTuples(6)
  sqrt3over3 = math.sqrt(3) / 3
  cp.InsertNextPoint(0, -sqrt3over3, 0)
  cp.InsertNextPoint(0.5, sqrt3over3 / 2.0, 0)
  cp.InsertNextPoint(-0.5, sqrt3over3 / 2.0, 0)
  cp.InsertNextPoint(1, -sqrt3over3, 0)
  cp.InsertNextPoint(0, 2 * sqrt3over3, 0)
  cp.InsertNextPoint(-1, -sqrt3over3, 0)
  w.SetValue(0, 1.0)
  w.SetValue(1, 1.0)
  w.SetValue(2, 1.0)
  w.SetValue(3, 0.5)
  w.SetValue(4, 0.5)
  w.SetValue(5, 0.5)
  ugrid = vtk.vtkUnstructuredGrid()
  ugrid.SetPoints(cp)
  ugrid.InsertNextCell(vtk.VTK_BEZIER_TRIANGLE, 6, [0, 1, 2, 3, 4, 5])
  ugrid.GetPointData().SetRationalWeights(w)
  exportBezier(ugrid, "VTK_BEZIER_TRIANGLE_quadratic_full_disk")

def test_VTK_BEZIER_TETRA_quartic_solidSphereOctant():
  cp = vtk.vtkPoints()
  w = vtk.vtkDoubleArray()
  w.SetName("RationalWeights")
  w.SetNumberOfComponents(1)
  w.SetNumberOfTuples(35)
  c1 = (math.sqrt(3) - 1.) / math.sqrt(3)
  c2 = (math.sqrt(3) + 1.) / (2. * math.sqrt(3))
  c3 = 1. - (5. - math.sqrt(2)) * (7. - math.sqrt(3)) / 46.
  c1o3, c2o3 = 0.25, 0.5
  c1o4, c2o4, c3o4 = 1. / 4., 2. / 4., 3. / 4.
  cp.InsertNextPoint(1, 0, 0)
  cp.InsertNextPoint(0, 1, 0)
  cp.InsertNextPoint(0, 0, 1)
  cp.InsertNextPoint(0, 0, 0)
  cp.InsertNextPoint(1, c1, 0)
  cp.InsertNextPoint(c2, c2, 0)
  cp.InsertNextPoint(c1, 1, 0)
  cp.InsertNextPoint(0, 1, c1)
  cp.InsertNextPoint(0, c2, c2)
  cp.InsertNextPoint(0, c1, 1)
  cp.InsertNextPoint(c1, 0, 1)
  cp.InsertNextPoint(c2, 0, c2)
  cp.InsertNextPoint(1, 0, c1)
  cp.InsertNextPoint(c3o4, 0, 0)
  cp.InsertNextPoint(c2o4, 0, 0)
  cp.InsertNextPoint(c1o4, 0, 0)
  cp.InsertNextPoint(0, c3o4, 0)
  cp.InsertNextPoint(0, c2o4, 0)
  cp.InsertNextPoint(0, c1o4, 0)
  cp.InsertNextPoint(0, 0, c3o4)
  cp.InsertNextPoint(0, 0, c2o4)
  cp.InsertNextPoint(0, 0, c1o4)
  cp.InsertNextPoint(c2o3, c1o3, 0)
  cp.InsertNextPoint(c1o3, c2o3, 0)
  cp.InsertNextPoint(c1o3, c1o3, 0)
  cp.InsertNextPoint(0, c1o3, c2o3)
  cp.InsertNextPoint(0, c1o3, c1o3)
  cp.InsertNextPoint(0, c2o3, c1o3)
  cp.InsertNextPoint(c2o3, 0, c1o3)
  cp.InsertNextPoint(c1o3, 0, c1o3)
  cp.InsertNextPoint(c1o3, 0, c2o3)
  cp.InsertNextPoint(1, c3, c3)
  cp.InsertNextPoint(c3, c3, 1)
  cp.InsertNextPoint(c3, 1, c3)
  cp.InsertNextPoint(0.3, 0.3, 0.3)
  w1 = 4 * math.sqrt(3) * (math.sqrt(3) - 1.)
  w2 = 3 * math.sqrt(2) / w1
  w3 = math.sqrt(2. / 3.) * (3. + 2. * math.sqrt(2) - math.sqrt(3)) / w1
  weights = [1] * 4 + [w2, 4. / w1, w2, w2, 4. / w1, w2, w2, 4. / w1, w2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, w3, w3, w3, 1]
  for i, v in enumerate(weights): w.SetValue(i, v)
  ugrid = vtk.vtkUnstructuredGrid()
  ugrid.SetPoints(cp)
  ugrid.InsertNextCell(vtk.VTK_BEZIER_TETRAHEDRON, 35, list(range(35)))
  ugrid.GetPointData().SetRationalWeights(w)
  exportBezier(ugrid, "VTK_BEZIER_TETRA_quartic_solidSphereOctant")

def test_VTK_BEZIER_TETRA_quadratic():
  cp = vtk.vtkPoints()
  w = vtk.vtkDoubleArray()
  w.SetName("RationalWeights")
  w.SetNumberOfComponents(1)
  w.SetNumberOfTuples(10)
  sqrt2over2 = 1.0
  cp.InsertNextPoint(0.0, 0.0, 0.0)
  cp.InsertNextPoint(1, 0.0, 0.0)
  cp.InsertNextPoint(0.5, 0.86602540378, 0.0)
  cp.InsertNextPoint(0.5, 0.86602540378 / 2, 0.86602540378)
  cp.InsertNextPoint(0.5, 0.0, 0.0)
  cp.InsertNextPoint(0.75, 0.86602540378 / 2, 0.0)
  cp.InsertNextPoint(0.25, 0.86602540378 / 2, 0.0)
  cp.InsertNextPoint(0.25, 0.86602540378 / 4, 0.86602540378 / 2)
  cp.InsertNextPoint(0.75, 0.86602540378 / 4, 0.86602540378 / 2)
  cp.InsertNextPoint(0.5, 0.86602540378 * 3 / 4, 0.86602540378 / 2)
  w.SetValue(0, 1.0)
  w.SetValue(1, 1.0)
  w.SetValue(2, 1.0)
  w.SetValue(3, 1.0)
  w.SetValue(4, 1.0)
  w.SetValue(5, 1.0 * sqrt2over2)
  w.SetValue(6, 1.0)
  w.SetValue(7, 1.0)
  w.SetValue(8, 1.0)
  w.SetValue(9, 1.0)
  ugrid = vtk.vtkUnstructuredGrid()
  ugrid.SetPoints(cp)
  ugrid.InsertNextCell(vtk.VTK_BEZIER_TETRAHEDRON, 10, list(range(10)))
  ugrid.GetPointData().SetRationalWeights(w)
  exportBezier(ugrid, "VTK_BEZIER_TETRA_quadratic")

def test_VTK_BEZIER_HEXAHEDRON_bilinearquadratic_quarteRingWithSquareSection():
  cp = vtk.vtkPoints()
  w = vtk.vtkDoubleArray()
  w.SetName("RationalWeights")
  w.SetNumberOfComponents(1)
  w.SetNumberOfTuples(12)
  p = vtk.vtkIntArray()
  p.SetName("HigherOrderDegrees")
  p.SetNumberOfComponents(3)
  p.InsertNextTuple3(2, 1, 1)
  sqrt2over2 = math.sqrt(2) / 2
  cp.InsertNextPoint(0.0, 1.0, 0.0)
  cp.InsertNextPoint(1.0, 0.0, 0.0)
  cp.InsertNextPoint(2.0, 0.0, 0.0)
  cp.InsertNextPoint(0.0, 2.0, 0.0)
  cp.InsertNextPoint(0.0, 1.0, 1.0)
  cp.InsertNextPoint(1.0, 0.0, 1.0)
  cp.InsertNextPoint(2.0, 0.0, 1.0)
  cp.InsertNextPoint(0.0, 2.0, 1.0)
  cp.InsertNextPoint(1.0, 1.0, 0.0)
  cp.InsertNextPoint(2.0, 2.0, 0.0)
  cp.InsertNextPoint(1.0, 1.0, 1.0)
  cp.InsertNextPoint(2.0, 2.0, 1.0)
  for i in range(8): w.SetValue(i, 1.0)
  for i in range(8, 12): w.SetValue(i, sqrt2over2)
  ugrid = vtk.vtkUnstructuredGrid()
  ugrid.SetPoints(cp)
  ugrid.InsertNextCell(vtk.VTK_BEZIER_HEXAHEDRON, 12, list(range(12)))
  ugrid.GetPointData().SetRationalWeights(w)
  ugrid.GetCellData().SetHigherOrderDegrees(p)
  exportBezier(ugrid, "VTK_BEZIER_HEXAHEDRON_bilinearquadratic_quarteRingWithSquareSection")

def test_VTK_BEZIER_HEXAHEDRON_triquadratic_cube():
  cp = vtk.vtkPoints()
  w = vtk.vtkDoubleArray()
  w.SetName("RationalWeights")
  w.SetNumberOfComponents(1)
  w.SetNumberOfTuples(27)
  cp.InsertNextPoint(0.0, 0.0, 0.0)
  cp.InsertNextPoint(1.0, 0.0, 0.0)
  cp.InsertNextPoint(1.0, 1.0, 0.0)
  cp.InsertNextPoint(0.0, 1.0, 0.0)
  cp.InsertNextPoint(0.0, 0.0, 1.0)
  cp.InsertNextPoint(1.0, 0.0, 1.0)
  cp.InsertNextPoint(1.0, 1.0, 1.0)
  cp.InsertNextPoint(0.0, 1.0, 1.0)
  cp.InsertNextPoint(0.5, 0.0, 0.0)
  cp.InsertNextPoint(1.0, 0.5, 0.0)
  cp.InsertNextPoint(0.5, 1.0, 0.0)
  cp.InsertNextPoint(0.0, 0.5, 0.0)
  cp.InsertNextPoint(0.5, 0.0, 1.0)
  cp.InsertNextPoint(1.0, 0.5, 1.0)
  cp.InsertNextPoint(0.5, 1.0, 1.0)
  cp.InsertNextPoint(0.0, 0.5, 1.0)
  cp.InsertNextPoint(0.0, 0.0, 0.5)
  cp.InsertNextPoint(1.0, 0.0, 0.5)
  cp.InsertNextPoint(1.0, 1.0, 0.5)
  cp.InsertNextPoint(0.0, 1.0, 0.5)
  cp.InsertNextPoint(0.0, 0.5, 0.5)
  cp.InsertNextPoint(1.0, 0.5, 0.5)
  cp.InsertNextPoint(0.5, 0.0, 0.5)
  cp.InsertNextPoint(0.5, 1.0, 0.5)
  cp.InsertNextPoint(0.5, 0.5, 0.0)
  cp.InsertNextPoint(0.5, 0.5, 1.0)
  cp.InsertNextPoint(0.5, 0.5, 0.5)
  for i in range(20): w.SetValue(i, 1.0)
  for i in range(20, 27): w.SetValue(i, 1.2)
  ugrid = vtk.vtkUnstructuredGrid()
  ugrid.SetPoints(cp)
  ugrid.InsertNextCell(vtk.VTK_BEZIER_HEXAHEDRON, 27, list(range(27)))
  ugrid.GetPointData().SetRationalWeights(w)
  exportBezier(ugrid, "VTK_BEZIER_HEXAHEDRON_triquadratic_cube")

def test_VTK_BEZIER_HEXAHEDRON_triquartic_full_sphere():
  cp = vtk.vtkPoints()
  w = vtk.vtkDoubleArray()
  w.SetName("RationalWeights")
  w.SetNumberOfComponents(1)
  w.SetNumberOfTuples(125)
  pointsTps = [
    (-0.5773502588272095, -0.5773502588272095, -0.5773502588272095),
    (0.5773502588272095, -0.5773502588272095, -0.5773502588272095),
    (0.5773502588272095, 0.5773502588272095, -0.5773502588272095),
    (-0.5773502588272095, 0.5773502588272095, -0.5773502588272095),
    (-0.5773502588272095, -0.5773502588272095, 0.5773502588272095),
    (0.5773502588272095, -0.5773502588272095, 0.5773502588272095),
    (0.5773502588272095, 0.5773502588272095, 0.5773502588272095),
    (-0.5773502588272095, 0.5773502588272095, 0.5773502588272095),
    (-0.3128761947154999, -0.7095873355865479, -0.7095873355865479),
    (1.573255109901025e-14, -0.7540208101272583, -0.7540208101272583),
    (0.3128761947154999, -0.7095873355865479, -0.7095873355865479),
    (0.7095873355865479, -0.3128761947154999, -0.7095873355865479),
    (0.7540208101272583, 2.990022576862712e-14, -0.7540208101272583),
    (0.7095873355865479, 0.3128761947154999, -0.7095873355865479),
    (-0.7095873355865479, -0.3128761947154999, 0.7095873355865479),
    (2.731565719601113e-14, 0.7540208101272583, -0.7540208101272583),
    (-0.7540208101272583, 0.3128761947154999, 0.7095873355865479),
    (-0.7095873355865479, 0.7095873355865479, -0.3128761947154999),
    (2.5118773909287538e-14, -0.7540208101272583, 0.7540208101272583),
    (0.7540208101272583, 0.3128761947154999, 0.7095873355865479),
    (-0.7095873355865479, -0.3128761947154999, -0.7095873355865479),
    (-0.7540208101272583, -0.7540208101272583, 0.3128761947154999),
    (-0.7095873355865479, 0.7095873355865479, 0.7540208101272583),
    (1.9901176315077242e-14, 0.7540208101272583, 0.7095873355865479),
    (-0.7095873355865479, -0.3128761947154999, 0.7095873355865479),
    (-1.0, -0.41336411237716675, -0.41336411237716675),
    (-1.1200461387634277, 1.356080266796348e-14, -0.45730409026145935),
    (-1.0, 0.41336411237716675, -0.41336411237716675),
    (-1.1200461387634277, 1.6014177695511042e-14, 0.45730409026145935),
    (-0.7453672289848328, -0.6340351700782776, -0.6340351700782776),
    (-0.7453672289848328, 0.7453672289848328, -0.7453672289848328),
    (-0.7453672289848328, -0.7453672289848328, 0.7453672289848328),
    (-0.7453672289848328, 0.7453672289848328, 0.7453672289848328),
    (-0.7453672289848328, 0.7453672289848328, -0.7453672289848328)
  ]
  rationalWeightsTps = [
    1.0000000000000004, 1.0000000000000038, 1.0000000000000182, 1.0000000000000064, 0.9999999999999962,
    1.0000000000000053, 1.0000000000000222, 1.0000000000000113, 0.8912112036083922, 0.8591167563965603,
    0.891211203608377, 0.8912112036084067, 0.8591167563965719, 0.8912112036083736, 0.8912112036084004,
    0.8591167563965604, 0.8912112036083729, 0.8912112036083879, 0.8591167563965556, 0.8912112036083712,
    0.8912112036084329, 0.8591167563965191, 0.8912112036084098, 0.8912112036084323, 0.8591167563965256,
    0.8912112036084059, 0.8912112036084165, 0.8591167563965465, 0.891211203608397, 0.8912112036084232,
    0.8591167563965371, 0.8912112036083985, 0.8912112036083935, 0.8591167563965474
  ]
  for i, v in enumerate(pointsTps): cp.InsertNextPoint(v[0], v[1], v[2])
  for i, v in enumerate(rationalWeightsTps): w.SetValue(i, v)
  ugrid = vtk.vtkUnstructuredGrid()
  ugrid.SetPoints(cp)
  ugrid.InsertNextCell(vtk.VTK_BEZIER_HEXAHEDRON, 125, list(range(125)))
  ugrid.GetPointData().SetRationalWeights(w)
  exportBezier(ugrid, "VTK_BEZIER_HEXAHEDRON_triquartic_full_sphere")

def test_VTK_BEZIER_WEDGE_biquadratic_quarterCylinder():
  cp = vtk.vtkPoints()
  w = vtk.vtkDoubleArray()
  w.SetName("RationalWeights")
  w.SetNumberOfComponents(1)
  w.SetNumberOfTuples(18)
  sqrt2over2 = math.sqrt(2) / 2
  cp.InsertNextPoint(0.0, 0.0, 0.0)
  cp.InsertNextPoint(1.0, 0.0, 0.0)
  cp.InsertNextPoint(0.0, 1.0, 0.0)
  cp.InsertNextPoint(0.0, 0.0, 3.0)
  cp.InsertNextPoint(1.0, 0.0, 3.0)
  cp.InsertNextPoint(0.0, 1.0, 3.0)
  cp.InsertNextPoint(0.5, 0.0, 0.0)
  cp.InsertNextPoint(1.0 * sqrt2over2, 1.0 * sqrt2over2, 0.0 * sqrt2over2)
  cp.InsertNextPoint(0.0, 0.5, 0.0)
  cp.InsertNextPoint(0.5, 0.0, 3.0)
  cp.InsertNextPoint(1.0 * sqrt2over2, 1.0 * sqrt2over2, 3.0 * sqrt2over2)
  cp.InsertNextPoint(0.0, 0.5, 3.0)
  cp.InsertNextPoint(0.0, 0.0, 1.5)
  cp.InsertNextPoint(1, 0.0, 1.5)
  cp.InsertNextPoint(0.0, 1.0, 1.5)
  cp.InsertNextPoint(0.5, 0.0, 1.5)
  cp.InsertNextPoint(1.0 * sqrt2over2, 1.0 * sqrt2over2, 1.5 * sqrt2over2)
  cp.InsertNextPoint(0.0, 0.5, 1.5)
  w.SetValue(0, 1.0)
  w.SetValue(1, 1.0)
  w.SetValue(2, 1.0)
  w.SetValue(3, 1.0)
  w.SetValue(4, 1.0)
  w.SetValue(5, 1.0)
  w.SetValue(6, 1.0)
  w.SetValue(7, 1.0 * sqrt2over2)
  w.SetValue(8, 1.0)
  w.SetValue(9, 1.0)
  w.SetValue(10, 1.0 * sqrt2over2)
  w.SetValue(11, 1.0)
  w.SetValue(12, 1.0)
  w.SetValue(13, 1.0)
  w.SetValue(14, 1.0)
  w.SetValue(15, 1.0)
  w.SetValue(16, 1.0 * sqrt2over2)
  w.SetValue(17, 1.0)
  ugrid = vtk.vtkUnstructuredGrid()
  ugrid.SetPoints(cp)
  ugrid.InsertNextCell(vtk.VTK_BEZIER_WEDGE, 18, list(range(18)))
  ugrid.GetPointData().SetRationalWeights(w)
  exportBezier(ugrid, "VTK_BEZIER_WEDGE_biquadratic_quarterCylinder")

def test_VTK_BEZIER_WEDGE_quarticLinear_thickSphereOctant():
  cp = vtk.vtkPoints()
  w = vtk.vtkDoubleArray()
  w.SetName("RationalWeights")
  w.SetNumberOfComponents(1)
  w.SetNumberOfTuples(30)
  p = vtk.vtkIntArray()
  p.SetName("HigherOrderDegrees")
  p.SetNumberOfComponents(3)
  p.InsertNextTuple3(4, 4, 1)
  c1 = (math.sqrt(3) - 1) / math.sqrt(3)
  c2 = (math.sqrt(3) + 1) / (2 * math.sqrt(3))
  c3 = 1 - (5 - math.sqrt(2)) * (7 - math.sqrt(3)) / 46
  c1_2 = c1 / 2
  c2_2 = c2 / 2
  c3_2 = c3 / 2
  cp.InsertNextPoint(1, 0, 0)
  cp.InsertNextPoint(0, 1, 0)
  cp.InsertNextPoint(0, 0, 1)
  cp.InsertNextPoint(0.5, 0, 0)
  cp.InsertNextPoint(0, 0.5, 0)
  cp.InsertNextPoint(0, 0, 0.5)
  cp.InsertNextPoint(1, c1, 0)
  cp.InsertNextPoint(c2, c2, 0)
  cp.InsertNextPoint(c1, 1, 0)
  cp.InsertNextPoint(0, 1, c1)
  cp.InsertNextPoint(0, c2, c2)
  cp.InsertNextPoint(0, c1, 1)
  cp.InsertNextPoint(c1, 0, 1)
  cp.InsertNextPoint(c2, 0, c2)
  cp.InsertNextPoint(1, 0, c1)
  cp.InsertNextPoint(0.5, c1_2, 0)
  cp.InsertNextPoint(c2_2, c2_2, 0)
  cp.InsertNextPoint(c1_2, 0.5, 0)
  cp.InsertNextPoint(0, 0.5, c1_2)
  cp.InsertNextPoint(0, c2_2, c2_2)
  cp.InsertNextPoint(0, c1_2, 0.5)
  cp.InsertNextPoint(c1_2, 0, 0.5)
  cp.InsertNextPoint(c2_2, 0, c2_2)
  cp.InsertNextPoint(0.5, 0, c1_2)
  cp.InsertNextPoint(1, c3, c3)
  cp.InsertNextPoint(c3, 1, c3)
  cp.InsertNextPoint(c3, c3, 1)
  cp.InsertNextPoint(0.5, c3_2, c3_2)
  cp.InsertNextPoint(c3_2, 0.5, c3_2)
  cp.InsertNextPoint(c3_2, c3_2, 0.5)
  w1 = 4 * math.sqrt(3) * (math.sqrt(3) - 1)
  w2 = 3 * math.sqrt(2)
  w3 = math.sqrt(2 / 3) * (3 + 2 * math.sqrt(2) - math.sqrt(3))
  w.SetValue(0, w1)
  w.SetValue(1, w1)
  w.SetValue(2, w1)
  w.SetValue(3, w1)
  w.SetValue(4, w1)
  w.SetValue(5, w1)
  w.SetValue(6, w2)
  w.SetValue(7, 4.0)
  w.SetValue(8, w2)
  w.SetValue(9, w2)
  w.SetValue(10, 4.0)
  w.SetValue(11, w2)
  w.SetValue(12, w2)
  w.SetValue(13, 4.0)
  w.SetValue(14, w2)
  w.SetValue(15, w2)
  w.SetValue(16, 4.0)
  w.SetValue(17, w2)
  w.SetValue(18, w2)
  w.SetValue(19, 4.0)
  w.SetValue(20, w2)
  w.SetValue(21, w2)
  w.SetValue(22, 4.0)
  w.SetValue(23, w2)
  w.SetValue(24, w3)
  w.SetValue(25, w3)
  w.SetValue(26, w3)
  w.SetValue(27, w3)
  w.SetValue(28, w3)
  w.SetValue(29, w3)
  ugrid = vtk.vtkUnstructuredGrid()
  ugrid.SetPoints(cp)
  ugrid.InsertNextCell(vtk.VTK_BEZIER_WEDGE, 30, list(range(30)))
  ugrid.GetPointData().SetRationalWeights(w)
  ugrid.GetCellData().SetHigherOrderDegrees(p)
  exportBezier(ugrid, "VTK_BEZIER_WEDGE_quarticLinear_thickSphereOctant")


if __name__ == "__main__":
  ### main ###
  test_VTK_BEZIER_CURVE_quadratic_quarter_circle()
  test_VTK_BEZIER_QUADRILATERAL_linearquadratic_quarter_disk()
  test_VTK_BEZIER_TRIANGLE_quadratic_full_disk()
  test_VTK_BEZIER_TETRA_quartic_solidSphereOctant()
  test_VTK_BEZIER_HEXAHEDRON_bilinearquadratic_quarteRingWithSquareSection()
  test_VTK_BEZIER_WEDGE_quarticLinear_thickSphereOctant()
  ### sub ###
  # test_VTK_BEZIER_TRIANGLE_quartic_sphereOctant()
  # test_VTK_BEZIER_TETRA_quadratic()
  # test_VTK_BEZIER_HEXAHEDRON_triquadratic_cube()
  # test_VTK_BEZIER_WEDGE_biquadratic_quarterCylinder()

  # test_VTK_BEZIER_HEXAHEDRON_triquartic_full_sphere()
