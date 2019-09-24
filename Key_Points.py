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

class Key_Points:
    def __init__(self, Vectors, Normals):
        self.Normals = Normals
        self.Vectors = Vectors

        
    def start_points(self,axis):

        #Define Start_Point for Propagation Algorithm
        for i in range(self.Vectors.shape[0]):
            for j in range(3):
                if (New_Vectors[i][j][axis] == Zero_Point[axis]):
                    Start_Point = New_Vectors[i][j]
                    break


        #End Point
        End_Point = np.zeros(3)
        for i in range(Cylinder_normals.shape[0]):
            if (np.array_equal(Cylinder_normals[i],Winding_Direction)):
                End_Point = Cylinder_vectors[i][0]
                break

        #Check for Direction Sanity
        Dir_1 = np.cross(New_Normals[Start_Point_Index],Winding_Direction)
        Dir_1 = Dir_1/np.linalg.norm(Dir_1)
        Dir_2 = np.subtract(Second_Point,Start_Point)
        Dir_2 = Dir_2/np.linalg.norm(Dir_2)

        if(np.array_equal(Dir_1, Dir_2) == False):
            Temp = Second_Point
            Second_Point = Start_Point
            Start_Point = Temp

        Path_Points.append(Start_Point)
        Path_Points.append(Second_Point)

        #Third Point
        Third_Point = np.zeros(3)
        Third_Edge_1 = np.zeros(3)
        Third_Point_Index_list = Point_Index_fun(New_Points,Second_Point)
        Third_Point_Index_list.remove(Second_Point_Index)
        for i in range(len(Third_Point_Index_list)):
            for j in range(3):
                if(np.array_equal(New_Vectors[Third_Point_Index_list[i]][j],Second_Point) == False):
                    if(New_Vectors[Third_Point_Index_list[i]][j][axis] == Second_Point[axis]):
                        Third_Edge_1 = New_Vectors[Third_Point_Index_list[i]][j]
                        Third_Point_Index = Third_Point_Index_list[i]
                        break
        Third_Edge_2 = Third_Vertex_fun(Third_Edge_1, Second_Point, Third_Point_Index,New_Vectors)
        Vector_Third_Edge = Plane_Winding_Direction(New_Normals[Third_Point_Index],Winding_Direction, 0.2)
        Third_Point = Intersection_fun(Third_Edge_1, Third_Edge_2, Second_Point,Vector_Third_Edge)
        #print("I",Third_Edge_1,Third_Edge_2,Third_Point)
        Path_Points.append(Third_Point)
