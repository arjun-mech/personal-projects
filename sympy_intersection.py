import sympy
from sympy import Point3D
from sympy.abc import L
from sympy.geometry import Line3D, Segment3D

l1 = Line3D(Point3D(58.867,50,117.735), Point3D(63.805,0,88.4583))
l2 = Line3D(Point3D(58.867,0,88.86751), direction_ratio=[-0.951677,0.2243,0.208])
print(l1.intersection(l2))

a = l1.intersection(l2)