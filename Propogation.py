import numpy as np
from stl import mesh
import math
import sys
from sklearn import preprocessing

# Using an existing stl file:
object_mesh = mesh.Mesh.from_file('cylinder.stl')
Cylinder_vectors = object_mesh.vectors
Cylinder_unorm = object_mesh.normals
Triangle_no = Cylinder_vectors.shape[0]

#Initializing Points

Start_Point = 
path_points = []
path_points.append(Start_Point)

i = 0
while path[i][0] < class.max_length('cylinder.stl'):
    path_points[i+1] = next_point(path_points[i],path_points[i-1])
    i += 1

def next_point( x ): 
    e = 0.0001 #error
    theta_max = 90 
    theta_min =-90
    start_angle = 0
    desired_angle = 45
    friction_coefficient = 0.2

    T1 = np.zeroes(3) #
    Edge_Vector = np.zeroes(3)
    N1 = np.zeroes(3) #Normal to Triangle 1
    N2 = np.zeroes(3) #Normal to Triangle 2
    Angle_between_planes = math.acos(np.dot(N1,N2))

    #Input angle - 1.5708 = pi/2
    input_angle = 1.5708 - math.acos(np.dot(T1,Edge_Vector))
    Zero_degree_Vector = np.cross(Edge_Vector, N2)
    Geodesic_Vector = np.add(math.cos(input_angle)*Zero_degree_Vector, math.sin(input_angle)*Edge_Vector)

    #Normalising the vectors
    Geodesic_Vector = preprocessing.normalize(Geodesic_Vector, norm='l2')

    #Calculating tangents to curve and normal to plane
    Surface_normal = preprocessing.normalize(np.add(N1,N2), norm='l2')

    #Storage Variable
    Max_1 = Edge_Vector
    Max_2 = Geodesic_Vector
    Min_1 = Geodesic_Vector
    Min_2 = -1*Edge_Vector
    Mid_1 = preprocessing.normalize(np.add(Max_1,Min_1), norm='l2')
    Mid_2 = preprocessing.normalize(np.add(Max_2,Min_2), norm='l2')
    Curve_max = preprocessing.normalize(np.add(Mid_1,T1), norm='l2')
    Curve_min = preprocessing.normalize(np.add(Mid_2,T1), norm='l2')

    Slippage_tedency_max = math.tan(math.acos(np.dot(Curve_max,-1*Surface_normal)))
    while (((friction_coefficient - Slippage_tedency_max) > 0 & (friction_coefficient - Slippage_tedency_max) <e) == False):           
        if (friction_coefficient - Slippage_tedency_max) < 0:
            Max_1 = Mid_1
        if (friction_coefficient - Slippage_tedency_max) > 0:
            Min_1 = Mid_1
        Mid_1 = preprocessing.normalize(np.add(Max_1,Min_1), norm='l2')
        Curve_max = preprocessing.normalize(np.add(Mid_1,T1), norm='l2')
        Slippage_tedency_max = math.tan(math.acos(np.dot(Curve_max,-1*Surface_normal)))
    
    Slippage_tedency_min = math.tan(math.acos(np.dot(Curve_min,-1*Surface_normal)))
    while (((friction_coefficient - Slippage_tedency_min) > 0 & (friction_coefficient - Slippage_tedency_min) <e) == False):
        if (friction_coefficient - Slippage_tedency_min) < 0:
            Max_2 = Mid_2
        if (friction_coefficient - Slippage_tedency_min) > 0:
            Min_2 = Mid_2
        Mid_2 = preprocessing.normalize(np.add(Max_2,Min_2), norm='l2')
        Curve_min = preprocessing.normalize(np.add(Mid_2,T1), norm='l2')
        Slippage_tedency_min = math.tan(math.acos(np.dot(Curve_min,-1*Surface_normal)))

def next_point_vertex( Point ): 
    Index = class.Triangle_Index(Point)
    section = [] 
    while i < Index.shape[0]:
        section.append
        