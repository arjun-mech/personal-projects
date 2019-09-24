import numpy as np
from stl import mesh
import math
import sys
from sklearn import preprocessing
from Index import *

class Bridging:
    def __init__(self, Vectors, Normals):
        self.Normals = Normals
        self.Vectors = Vectors
        self.Points = Make_Points(self.Vectors)   

    def bridging_check_point(surface_normal, curve_normal):
        if np.dot(-1*surface_normal,curve_normal) > 0:
            return 1
        else:
            return 0

    def bridging_iteration(index, common_vertex, start_vertex):
        start_vector = np.subtract(start_vertex, common_vertex)
        start_vector = start_vector/np.linalg.norm(start_vector)
        allowed_angles = []
        #Brute Force Span
        total_span = 90
        #Find Vertex On the start Triangle
        third_vertex = Third_Vertex_fun(common_vertex, vertex_2, index ,self.Vectors)
        third_vertex_vector = np.subtract(third_vertex,common_vertex)
        
        end_vector = 