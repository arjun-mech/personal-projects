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
from Winding_Direction import Plane_Direction
from Index import *
from Bridging import bridging_check

class slippage_v2:
    def __init__(self, Vectors, Normals, End_Point, axis,Winding_Direction,Winding_angle):
        self.Normals = Normals
        self.Vectors = Vectors
        self.End_Point = End_Point
        self.axis = axis
        self.Points = Make_Points(self.Vectors)
        self.Winding_Direction = Winding_Direction
        self.Winding_angle = Winding_angle

    def next_point_edge(self,Point_1, Point_2, Vertex_1, Vertex_2, Index_1, Index_2): 
        e = 0.01 #error
        friction_coefficient = 0.7

        #Defining egde Vector and Normals
        #Normal of Previous Triangle
        N1 = self.Normals[Index_1]
        print("N1",N1,Index_1)
    
        #Normal of New_Triangle
        N2 = self.Normals[Index_2]
        print("N2",N2,Index_2)

        T1 = np.subtract(Point_2,Point_1)
        T1 = T1/np.linalg.norm(T1)
        #print("T1",T1)

        #Determining Intersection point(New Point P2, and new vertexes)
        Third_Vertex = Third_Vertex_fun(Vertex_1, Vertex_2, Index_2,self.Vectors)
        #print("Vertex_1,Vertex_2",Vertex_1,Vertex_2,Third_Vertex)
        #Make the points Counterclockwise
        Vertex_1,Vertex_2 = counter_clockwise_check(Vertex_1,Vertex_2,Third_Vertex, N2)
        #print("Vertex_1,Vertex_2",Vertex_1,Vertex_2,Third_Vertex)
        Edge_Vector = np.subtract(Vertex_2,Vertex_1)
        Edge_Vector = Edge_Vector/np.linalg.norm(Edge_Vector)
        #print("EV",Edge_Vector)

        input_angle = math.acos(np.dot(T1,Edge_Vector))
        Zero_degree_Vector = np.cross(N2, Edge_Vector)
        Zero_degree_Vector = Zero_degree_Vector/np.linalg.norm(Zero_degree_Vector)

        Geodesic_Vector = np.add(math.sin(input_angle)*Zero_degree_Vector, math.cos(input_angle)*Edge_Vector)
    
        #Normalising the vectors
        Geodesic_Vector = Geodesic_Vector/np.linalg.norm(Geodesic_Vector)
        print("Geodesic_vector", Geodesic_Vector)

        #Favored Direction
        Favored_Dir = Plane_Winding_Direction(N2,self.Winding_Direction,self.Winding_angle)
        print("Favored_Dir",Favored_Dir)
    

        #Calculating tangents to curve and normal to plane
        Surface_normal = np.add(N1,N2)
        Surface_normal = Surface_normal/np.linalg.norm(Surface_normal)
        #print("Surface normal mod",np.linalg.norm(Surface_normal))
        #print("Surface Normal",Surface_normal)

        #Storage Variable
        Max= Favored_Dir
        Min= Geodesic_Vector
        Mid = np.add(Max,Min)
        Mid = Mid/np.linalg.norm(Mid)
        Curve_vector = np.add(Max,-1*T1)
        #Curve_vector = Curve_vector/np.linalg.norm(Curve_vector)

        #Geodesic Slippage calculation
        #Curve_Geodesic = np.subtract(Geodesic_Vector,T1)
        #Curve_Geodesic = Curve_Geodesic/np.linalg.norm(Curve_Geodesic)
        #print("Curve_Geodesic",Curve_Geodesic)

        #Slippage_Geodesic = math.tan(math.acos(np.dot(Curve_Geodesic,-1*Surface_normal)))  
        #print("Slippage Geodesic",Slippage_Geodesic)

        Dot_product = np.dot(Curve_vector,-1*Surface_normal)
        if(Dot_product>1):
            Dot_product = 0.999
        if(Dot_product<-1):
            Dot_product = -0.999        
        Slippage_tendency= abs(math.tan(math.acos(Dot_product)))
        #print("Dot product",Dot_product)
        #print(math.tan(math.acos(Dot_product)))

        a = 0
        if (Slippage_tendency < friction_coefficient):
            Propogation_Vector = Max
        else:
            while (abs(friction_coefficient - Slippage_tendency) > e) and a <40:
                if (friction_coefficient < Slippage_tendency):
                    Max = Mid
                if (friction_coefficient > Slippage_tendency):
                    Min = Mid
                Mid = np.add(Max,Min)
                Mid = Mid/np.linalg.norm(Mid)
                #print(Mid_1)
                Curve_vector = np.add(Mid,-1*T1)
                #Curve_vector = Curve_vector/np.linalg.norm(Curve_vector)
                Dot_product = np.dot(Curve_vector,-1*Surface_normal)
                print("Dot_product",Dot_product)
                if(Dot_product>1):
                    Dot_product =0.999
                if(Dot_product<-1):
                    Dot_product =-0.999
                Slippage_tendency= abs(math.tan(math.acos(Dot_product)))
                a = a + 1
                #print("Max",Max)
                #print("Min",Min)
                #print("Mid",Mid)
                #print("Slippage_tendency",abs(Slippage_tendency))
            #Define the Propogtion Vector
            Propogation_Vector = Mid
            

        print("Propogation Vector",Propogation_Vector)

        Intersection_Point, New_Vertex_1 = new_point(Vertex_1, Vertex_2, Third_Vertex, Propogation_Vector, N2, Point_2)
        New_Vertex_2 = Third_Vertex

        angle_axis = Plane_Direction(N2,self.Winding_Direction)
        local_angle = math.acos(math.cos(math.pi/6)*math.cos(math.asin(np.dot(angle_axis,Propogation_Vector))))
        #print("New_Vertex_1",New_Vertex_1)
        #print("New_Vertex_2",New_Vertex_2)
        print("Intersection_Point",Intersection_Point)
        #print(bool(Intersection_Point[self.axis]*self.Winding_Direction[self.axis]<self.End_Point[self.axis]*self.Winding_Direction[self.axis]))
        New_Index_1 = Index_2
        #print(self.Winding_Direction[self.axis])
        #print("End_Point",self.End_Point)
        #print(Index_2)
        if(Intersection_Point[self.axis]*self.Winding_Direction[self.axis]<self.End_Point[self.axis]*self.Winding_Direction[self.axis]):
            New_Index_2 = find_Index(New_Vertex_1,New_Vertex_2,Index_2,self.Points)
        else:
            New_Index_2 = 0
        Forward_Array = np.zeros((6,3))
        New_Point_1 = Point_2
        New_Point_2 = Intersection_Point
        
        #print("New_Index_1",New_Index_1)
        #print(self.Vectors[New_Index_1])
        #print("New_Index_2",New_Index_2)
        #print(self.Vectors[New_Index_2])

        Forward_Array[0] = New_Point_1
        Forward_Array[1] = New_Point_2
        Forward_Array[2] = New_Vertex_1
        Forward_Array[3] = New_Vertex_2
        Forward_Array[4][0] = New_Index_1
        Forward_Array[5][0] = New_Index_2
        #print("Forward Array",Forward_Array)
        #print("####")
        return Forward_Array, local_angle
    
