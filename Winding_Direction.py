import numpy as np
from stl import mesh
import math
import sys
from sklearn import preprocessing
import csv

#find Winding direction for Plane
def Plane_Winding_Direction(Normal,Vector,Angle):
    Plane_Direction = np.cross(Normal,Vector)
    Plane_Direction = Plane_Direction/np.linalg.norm(Plane_Direction)
    print(Plane_Direction)
    Surface_Tangent = np.cross(Plane_Direction,Normal)
    Surface_Tangent = Surface_Tangent/np.linalg.norm(Surface_Tangent)
    print(Surface_Tangent)
    Direction = np.add(math.sin(Angle)*Surface_Tangent, math.cos(Angle)*Plane_Direction)
    Direction = Direction/np.linalg.norm(Direction)

    return Direction

def Plane_Direction(Normal,Vector):
    Plane_Direction = np.cross(Normal,Vector)
    Plane_Direction = Plane_Direction/np.linalg.norm(Plane_Direction)

    return Plane_Direction

