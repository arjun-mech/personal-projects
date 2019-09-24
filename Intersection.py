import numpy as np
from stl import mesh
import math
import sys

#Find Intersection of 2 Lines
def Intersection_fun(Vertex_1, Vertex_2, Point, Vector_1):
    Vector = np.subtract(Vertex_2,Vertex_1)
    Vector = Vector/np.linalg.norm(Vector)
    Cross_1 = np.cross(Vector,Vector_1)
    Cross_2 = np.cross(np.subtract(Point,Vertex_1),Vector_1)
    #print(Cross_1)
    #print(Cross_2)
    for i in range(3):
        if (Cross_1[i]!=0):
            Factor =  Cross_2[i]/Cross_1[i]
            break
    #print(Factor)
    #print(Vector)
    Intersection = np.add(Vertex_1, Factor*Vector)
    return Intersection

def Intersection_fun_alt(Point_1,Vector_1,Point_2, Vector_2):
    Cross_1 = np.cross(Vector_1,Vector_2)
    #print(Cross_1)
    Cross_2 = np.cross(np.subtract(Point_2,Point_1),Vector_2)
    #print(Cross_2)
    for i in range(3):
        if (Cross_1[i]!=0  ):
            Factor =  Cross_2[i]/Cross_1[i]
            break
    Intersection = np.add(Point_1, Factor*Vector_1)   
    return Intersection

def Intersection_fun_2d(Point_1,Point_a,Point_2, Point_b):
    Vector_1 = np.subtract(Point_a,Point_1)
    Vector_2 = np.subtract(Point_b,Point_2)
    Cross_1 = np.cross(Vector_1,Vector_2)
    #print(Cross_1)
    Cross_2 = np.cross(np.subtract(Point_2,Point_1),Vector_2)
    #print(Cross_2)   
    Factor =  Cross_2/Cross_1
    Intersection = np.add(Point_1, Factor*Vector_1)   
    return Intersection


#a = np.array([58.867,50,117.735])
#b = np.array([63.805,0,88.4583])
#c = np.array([58.867,0,88.86751])
#v = np.array([-0.951677,0.2243,0.208])

#p = Intersection_fun(a,b,c,v)
#print(p)
#print(np.subtract(a,b))