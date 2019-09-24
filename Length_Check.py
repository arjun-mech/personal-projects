import numpy as np
from stl import mesh
import math
import sys

def length_calc(Point_1, Point_2):
    L = np.linalg.norm(np.subtract(Point_2,Point_1))
    return L

def length_check(Point_1, Point_2 , Reference):
    L1 = length_calc(Reference,Point_1)
    L2 = length_calc(Reference,Point_2)
    if L1>L2:
        return Point_2,2
    else:
        return Point_1,1
