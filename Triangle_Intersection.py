import numpy as np
from stl import mesh
import math
import sys
from Intersection import Intersection_fun
from Intersection import Intersection_fun_alt
from Length_Check import length_check


def new_point(Vertex_1, Vertex_2, Vertex_3, Propogation_Vector, Normal, Point):

    Intersection_Point = np.zeros(3)
    Intersection_1 = Intersection_fun(Vertex_1, Vertex_3, Point, Propogation_Vector)
    Intersection_2 = Intersection_fun(Vertex_2, Vertex_3, Point, Propogation_Vector)

    Circumcentre = np.zeros(3)
    Edge_1 = np.subtract(Vertex_1,Vertex_2)
    #print("Edge_1",Edge_1)
    Edge_2 = np.subtract(Vertex_1, Vertex_3)
    #print("Edge_2",Edge_2)
    Midpoint_1 = np.add(.5*Vertex_1,0.5*Vertex_2)
    #print("Midpoint_1",Midpoint_1)
    Midpoint_2 = np.add(.5*Vertex_1,0.5*Vertex_3)
    #print("Midpoint_2",Midpoint_2)
    Perpendicular_1 = np.cross(Normal,Edge_1)
    #print("Perpendicular_1",Perpendicular_1)
    Perpendicular_2 = np.cross(Normal,Edge_2)
    #print("Perpendicular_2",Perpendicular_2)
    Circumcentre = Intersection_fun_alt(Midpoint_1, Perpendicular_1, Midpoint_2, Perpendicular_2)

    Intersection_Point, I = length_check(Intersection_1,Intersection_2, Circumcentre)
    if I == 1:
        New_Vertex = Vertex_1
    else:
        New_Vertex = Vertex_2

    return Intersection_Point, New_Vertex






