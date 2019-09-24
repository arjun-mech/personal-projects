import numpy as np
from stl import mesh
import math
import sys
from sklearn import preprocessing
from Index import *

class STL_Formatting:
    def __init__(self, Vectors, Normals):
        self.Normals = Normals
        self.Vectors = Vectors

    def eliminate_flatpoints(self):
        Triangle_no = self.Vectors.shape[0]
        Points = Make_Points(self.Vectors)
        #Find all unique Points for the object
        Unique_Points = np.unique(Points, axis=0)
        Point_Index = []
        all_index = []
        Flat_points = []
        Flatness_check = 1

        #Check for Flat Points
        for i in range(Unique_Points.shape[0]):
            Point_Index.append([])
            Point_Index[i] = Point_Index_fun(Points,Unique_Points[i])

        for i in range(len(Point_Index)):
            First_normal = self.Normals[Point_Index[i][0]]
            for j in range(len(Point_Index[i])-1):
                t = Point_Index[i][j+1]
                if (np.array_equal(self.Normals[t], First_normal)):
                    Flatness_check = Flatness_check + 1
            if(Flatness_check == len(Point_Index[i])):
                Flat_points.extend(Point_Index[i])
            Flatness_check = 1

        #Check for flat normal
        for i in range(len(Point_Index)):
            First_normal = self.Normals[Point_Index[i][0]]
            for j in range(len(Point_Index[i])-1):
                t = Point_Index[i][j+1]
                if (np.array_equal(self.Normals[t], First_normal)):
                    Flatness_check = Flatness_check + 1
            if(Flatness_check == len(Point_Index[i])):
                Flat_Normal = First_normal
                
                break
            Flatness_check = 1

        Flat_points = np.asarray(Flat_points)
        Flat_points = np.unique(Flat_points)

        #Number for Flatness Check
        Flat_Triangles = 0
        for i in range(self.Vectors.shape[0]):
            if(np.array_equal(self.Normals[i],Flat_Normal) or np.array_equal(self.Normals[i]*-1,Flat_Normal)):
                Flat_Triangles = Flat_Triangles + 1

        #Defining a point on the flat surface of the stl file (Zero_Point)
        #Zero_Point = Unique_Points[Flat_points[0]]
        #print("Zero_Point",Zero_Point)
        #Edge_Point_Index = Point_Index_fun(Points, Zero_Point)[0]
        #print("Edge_Point_Index",Edge_Point_Index)
        
        New_Vectors = []
        New_Normals = []

        #Create new STL file
       
        for i in range(Triangle_no):
           if(np.array_equal(Flat_Normal,self.Normals[i]) == False and np.array_equal(Flat_Normal*-1,self.Normals[i]) == False):
                New_Vectors.append(self.Vectors[i])
                New_Normals.append(self.Normals[i])
               

        New_Vectors = np.asarray(New_Vectors)
        New_Normals = np.asarray(New_Normals)

		#Defining Winding Direction
        #print("Flat_Normal",Flat_Normal)
        Edge_Point_Index = Point_Index_fun_alt(self.Normals, Flat_Normal)[0]
        #print(self.Normals[flat_normal_index])
        #print(flat_normal_index)
        Zero_Point = self.Vectors[Edge_Point_Index][0]
        #print("flat_normal_point",flat_normal_point)


        Winding_Direction = -1*Flat_Normal
        axis = int(np.nonzero(Winding_Direction)[0])
        
        return New_Vectors,New_Normals,Winding_Direction,axis,Zero_Point,Edge_Point_Index