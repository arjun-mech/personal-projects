import numpy as np
from stl import mesh
import math
import sys

def Make_Points(Array_I):
    Array_Length = Array_I.shape[0]
    Array_O = np.zeros((3*Array_Length, 3))
   
    #Make Nx3x3 matrix a 3Nx3 Matrix to keep all points in same vector dimension
    for i in range(Array_Length):
        Array_O[3*i] = (Array_I[i][0][0], Array_I[i][0][1], Array_I[i][0][2])
        Array_O[int(3*i+1)] = (Array_I[i][1][0], Array_I[i][1][1], Array_I[i][1][2])
        Array_O[int(3*i+2)] = (Array_I[i][2][0], Array_I[i][2][1], Array_I[i][2][2])

    return Array_O

def Point_Index_fun(Array,Point):
    All_Index = []
    for j in range(Array.shape[0]):
        if (np.array_equal(Array[j], Point)):
            index = int(j/3)           
            All_Index.append(index)
    return All_Index

#Find Next Index
def find_Index(Point_1,Point_2,Index,Points):
    I_1 = Point_Index_fun(Points, Point_1)
    I_2 = Point_Index_fun(Points, Point_2)
    Common_Index = list(set(I_1) & set(I_2))
    Common_Index.remove(Index)
    return Common_Index[0]

def Third_Vertex_fun(Point_1, Point_2, Index, Vectors):
    Index_2 = Index
    I_2 = Vectors[Index_2]
    Third_Point = np.zeros(3)
    for i in range(3):
        if (np.array_equal(I_2[i],Point_1) or np.array_equal(I_2[i],Point_2)):
            Third_Point = np.zeros(3)
        else:
            Third_Point = I_2[i]
            break
    return Third_Point
        
def Point_Index_fun_alt(Array,Point):
    All_Index = []
    for j in range(Array.shape[0]):
        if (np.array_equal(Array[j], Point)):
            index = int(j)           
            All_Index.append(index)
    return All_Index

def bridging_check(n1,n2,t1,t2):
        surface_normal = np.add(n1,n2)
        surface_normal = surface_normal/np.linalg.norm(surface_normal)
		#print(surface_normal)
        curve_normal = np.add(t1,t2)
        curve_normal = curve_normal/np.linalg.norm(curve_normal)
		#print(curve_normal)
        dot_product = np.dot(curve_normal,-1*surface_normal)
		#print(dot_product)
        if(dot_product>1):
            dot_product = 0.999
        if(dot_product<-1):
            dot_product = -0.999  
        
        return dot_product  