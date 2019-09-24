from Index import *
import numpy as np
from stl import mesh
import math
import sys

class point_geodesic:
    def __init__(self, Vectors, Normals):
        self.Normals = Normals
        self.Vectors = Vectors
        self.Points = Make_Points(self.Vectors)

    def geodesic(common_vertex,vector,start_index,start_vertex):

        angle = []
        edges = []
        temp_vector = np.subtract(start_vertex,common_vertex)
        temp_vector = temp_vector/np.linalg.norm(temp_vector)
        edges.append(vector)
        edges.append(temp_vector)

        interior_angle = 180*math.acos(np.dot(temp_vector,vector))/math.pi
        angle.append(interior_angle)

        indexes = Point_Index_fun(vertex,self.Points)
        temp_vertex = start_vertex
        temp_index = start_index

        for i in range(len(indexes)-1):
            interior_angle,temp_vertex,temp_index, edge = angle_return(common_vertex, temp_vertex, temp_index)
            angle.append(interior_angle)
            edges.append(edge)

        temp_vector = np.subtract(temp_vertex,common_vertex)
        temp_vector = temp_vector/np.linalg.norm(temp_vector)

        interior_angle = 180*math.acos(np.dot(temp_vector,vector))/math.pi
        angle.append(interior_angle)

        total_angle = sum(angle)
        bisecting_angle = total_angle/2

        sector = 0
        for i in range(len(indexes)):
            bisecting_angle = bisecting_angle - angle[i]
            sector = sector + 1
            if bisecting_angle < 0:
                bisecting_angle = bisecting_angle + angle[i]
                break
        
        geodesic_vector = vector_angle(egdes[sector],edges[sector+1],angle[i],bisecting_angle)
        curve_normal = np.add(geodesic_vector,vector)
        curve_normal = curve_normal/np.linalg.norm(curve_normal)

        indexes_mod = indexes
        indexes_mod.append(indexes[0])

		#Calculating Surface Normal
        surface_normal = np.zeros(3)
        for i in range(len(indexes_mod)):
            surface_normal = np.add(surface_normal,angle[i]/total_angle*self.Normals[indexes_mod[i]])

        return geodesic_vector, curve_normal, surface_normal

    def angle_return(common_vertex, vertex_2, index):

        next_index = find_Index(common_vertex, vertex_2, index, self.Points)
        next_vertex = Third_Vertex_fun(common_vertex, vertex_2, next_index,self.Vectors)
		#Start vector
        temp_vector_start = np.subtract(vertex_2,common_vertex)
        temp_vector_start = temp_vector_start/np.linalg.norm(temp_vector_start)
		#Next Vector
        temp_vector_next = np.subtract(next_vertex,common_vertex)
        temp_vector_next = temp_vector_next/np.linalg.norm(temp_vector_next)

        interior_angle = 180*math.acos(np.dot(temp_vector_start,temp_vector_next))/math.pi
        
        return interior_angle, next_vertex, next_index, temp_vector_next
        
    def vector_angle(vector_1,vector_2, angle, bisecting_angle):

        vector_1_projection = math.cos(bisecting_angle*math.pi/180)*vector_1
        vector_2_projection = math.cos((angle-bisecting_angle)*math.pi/180)*vector_2
        output_vector = np.add(vector_1_projection,vector_2_projection)

        output_vector = output_vector/np.linalg.norm(output_vector)

        return output_vector

