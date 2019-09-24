import numpy as np
from stl import mesh
import math
import sys
from sklearn import preprocessing
import csv
from Intersection import Intersection_fun
from Intersection import Intersection_fun_alt
from Triangle_Intersection import new_point
from Counter_Clockwise_Check import counter_clockwise_check
from Winding_Direction import Plane_Winding_Direction
from Index import *

class point_path:
    def __init__(self, *args, **kwargs):
        
