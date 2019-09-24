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

Cylinder_normals = preprocessing.normalize(Cylinder_unorm, norm='l2')

#Find all points from cylinder_vectors
def Make_Points(Array_I):
    Array_Length = Array_I.shape[0]
    Array_O = np.zeros((3*Array_Length, 3))
   
    #Make Nx3x3 matrix a 3Nx3 Matrix to keep all points in same vector dimension
    for i in range(Array_Length):
        Array_O[3*i] = (Array_I[i][0][0], Array_I[i][0][1], Array_I[i][0][2])
        Array_O[int(3*i+1)] = (Array_I[i][1][0], Array_I[i][1][1], Array_I[i][1][2])
        Array_O[int(3*i+2)] = (Array_I[i][2][0], Array_I[i][2][1], Array_I[i][2][2])

    return Array_O

Points = Make_Points(Cylinder_vectors)
#Find all unique Points for the object
Unique_Points = np.unique(Points, axis=0)
Point_Index = []
all_index = []
Flat_points = []
Flatness_check = 1

#Calculate Index of Point 
def Point_Index_fun(Array,Point):
    All_Index = []
    for j in range(Array.shape[0]):
        if (np.array_equal(Array[j], Point)):
            index = int(j/3)           
            All_Index.append(index)
    return All_Index

for i in range(Unique_Points.shape[0]):
    Point_Index.append([])
    Point_Index[i] = Point_Index_fun(Points,Unique_Points[i])

for i in range(len(Point_Index)):
    First_normal = Cylinder_normals[Point_Index[i][0]]
    for j in range(len(Point_Index[i])-1):
        t = Point_Index[i][j+1]
        if (np.array_equal(Cylinder_normals[t], First_normal)):
            Flatness_check = Flatness_check + 1
    if(Flatness_check == len(Point_Index[i])):
        Flat_points.extend(Point_Index[i])
    Flatness_check = 1

Flat_points = np.asarray(Flat_points)
Flat_points = np.unique(Flat_points)

Zero_Point = Unique_Points[Flat_points[0]]
Edge_Point_Index = Point_Index_fun(Points, Zero_Point)[0]
Flat_Normal_x = Cylinder_normals[Edge_Point_Index]
Edge_Point = np.zeros(3)

for i in range(3):
    if (np.array_equal(Cylinder_vectors[Edge_Point_Index][i], Zero_Point) == False):
        Edge_Point = Cylinder_vectors[Edge_Point_Index][i]
        break

Flat_Normal_y = np.subtract(Zero_Point, Edge_Point)
Flat_Normal_z = np.cross(Flat_Normal_x , Flat_Normal_y)

print(Flat_Normal_x)
print(Flat_Normal_y)
print(Flat_Normal_z)
New_Vectors = np.zeros((Triangle_no - Flat_points.size, 3, 3))
New_Normals = np.zeros((Triangle_no - Flat_points.size, 3))

Flat_pointlist = Flat_points
Flat_pointlist.tolist()

#Create new STL file
t=0
for i in range(Triangle_no):
   if((i in Flat_pointlist)== False):
        New_Vectors[t] = Cylinder_vectors[i]
        New_Normals[t] = Cylinder_normals[i]
        t = t+1

New_Points = Make_Points(New_Vectors)

def Object_rotation(Vector_x,Vector_y,Vector_z, Object):
    Rotation_matrix = np.zeros((3,3))
    Rotation_matrix[0] = Vector_x
    Rotation_matrix[1] = Vector_y
    Rotation_matrix[2] = Vector_z
    Inverse_Matrix = np.linalg.inv(Rotation_matrix)
    print(Rotation_matrix)
    print(Inverse_Matrix)
    
    for i in range(Object.shape[0]):
        for j in range(3):
            Object[i][j] = np.matmul(Inverse_Matrix, Object[i][j])
    return Object

def Point_rotation(Vector_x,Vector_y,Vector_z, Point):
    Rotation_matrix = np.zeros((3,3))
    Rotation_matrix[0] = Vector_x
    Rotation_matrix[1] = Vector_y
    Rotation_matrix[2] = Vector_z
    Inverse_Matrix = np.linalg.inv(Rotation_matrix)

    Point = np.matmul(Inverse_Matrix, Point)
    return Point

print(Zero_Point)
Zero_Point = Point_rotation(Flat_Normal_x, Flat_Normal_y, Flat_Normal_z,Zero_Point)
print(Zero_Point)

def Object_translation(Object, Point):
    for i in range(Object.shape[0]):
        for j in range(3):
            Object[i][j] = np.subtract(Object[i][j], Point)
    return Object

print(New_Vectors)
New_Vectors = Object_translation(New_Vectors, Zero_Point)
New_Vectors = Object_rotation(Flat_Normal_x, Flat_Normal_y, Flat_Normal_z,New_Vectors)

Cylinder_mod = mesh.Mesh(np.zeros(New_Vectors.shape[0], dtype=mesh.Mesh.dtype))
Cylinder_mod.vectors = New_Vectors
Cylinder_mod.save('cylinder_mod.stl')












