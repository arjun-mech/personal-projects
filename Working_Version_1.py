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

# Using an existing stl file:
object_mesh = mesh.Mesh.from_file('cylinder_creo.stl')
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

#Check for Flat Points
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

#Check for flat normal
for i in range(len(Point_Index)):
    First_normal = Cylinder_normals[Point_Index[i][0]]
    for j in range(len(Point_Index[i])-1):
        t = Point_Index[i][j+1]
        if (np.array_equal(Cylinder_normals[t], First_normal)):
            Flatness_check = Flatness_check + 1
    if(Flatness_check == len(Point_Index[i])):
        Flat_Normal = First_normal
        break
    Flatness_check = 1

Flat_points = np.asarray(Flat_points)
Flat_points = np.unique(Flat_points)

#Number for Flatness Check
Flat_Triangles = 0
for i in range(Cylinder_vectors.shape[0]):
    if(np.array_equal(Cylinder_normals[i],Flat_Normal) or np.array_equal(Cylinder_normals[i]*-1,Flat_Normal)):
        Flat_Triangles = Flat_Triangles + 1

#Defining a point on the flat surface of the stl file (Zero_Point)
Zero_Point = Unique_Points[Flat_points[0]]
Edge_Point_Index = Point_Index_fun(Points, Zero_Point)[0]

#Defining Winding Direction
Winding_Direction = -1*Flat_Normal
axis = int(np.nonzero(Winding_Direction)[0])
Start_Point = np.zeros(3)
#print(Winding_Direction)
New_Vectors = []
New_Normals = []

Flat_pointlist = Flat_points
Flat_pointlist.tolist()

#Create new STL file
t=0
for i in range(Triangle_no):
   if(np.array_equal(Flat_Normal,Cylinder_normals[i]) == False and np.array_equal(Flat_Normal*-1,Cylinder_normals[i]) == False):
        New_Vectors.append(Cylinder_vectors[i])
        New_Normals.append(Cylinder_normals[i])
        t = t+1
New_Vectors = np.asarray(New_Vectors)
New_Normals = np.asarray(New_Normals)

#Define Start_Point for Propagation Algorithm
for i in range(New_Vectors.shape[0]):
    for j in range(3):
        if (New_Vectors[i][j][axis] == Zero_Point[axis]):
            Start_Point = New_Vectors[i][j]
            break

Cylinder_mod = mesh.Mesh(np.zeros(New_Vectors.shape[0], dtype=mesh.Mesh.dtype))
Cylinder_mod.vectors = New_Vectors
Cylinder_mod.save('cylinder_mod.stl')

New_Points = Make_Points(New_Vectors)
New_Points_list = New_Points
New_Points_list.tolist()

######################Propogation Algorithm#############################################

#Second Point
Winding_angle = math.pi/8
Path_Points = []
Start_Point_Index = Point_Index_fun(New_Points, Start_Point)[0]
Second_Point = np.zeros(3) 

for i in range(3):
    if (New_Vectors[Start_Point_Index][i][axis] == Start_Point[axis]):
        if (np.array_equal(New_Vectors[Start_Point_Index][i], Start_Point) == False):
            Second_Point = New_Vectors[Start_Point_Index][i]
            break
Second_Point_Index = Start_Point_Index

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

#Find Next Index
def find_Index(Point_1,Point_2,Index):
    I_1 = Point_Index_fun(New_Points, Point_1)
    I_2 = Point_Index_fun(New_Points, Point_2)
    Common_Index = list(set(I_1) & set(I_2))
    Common_Index.remove(Index)
    return Common_Index[0]

#Find Third Vertex on STL Triangle
def Third_Vertex_fun(Point_1, Point_2, Index_1):
    Index_2 = find_Index(Point_1,Point_2,Index_1)
    I_2 = New_Vectors[Index_2]
    Third_Point = np.zeros(3)
    for i in range(3):
        if (np.array_equal(I_2[i],Point_1) or np.array_equal(I_2[i],Point_2)):
            Third_Point = np.zeros(3)
        else:
            Third_Point = I_2[i]
            break
    return Third_Point

def Third_Vertex_fun_2(Point_1, Point_2, Index):
    Index_2 = Index
    I_2 = New_Vectors[Index_2]
    Third_Point = np.zeros(3)
    for i in range(3):
        if (np.array_equal(I_2[i],Point_1) or np.array_equal(I_2[i],Point_2)):
            Third_Point = np.zeros(3)
        else:
            Third_Point = I_2[i]
            break
    return Third_Point

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
Third_Edge_2 = Third_Vertex_fun_2(Third_Edge_1, Second_Point, Third_Point_Index)
Vector_Third_Edge = Plane_Winding_Direction(New_Normals[Third_Point_Index],Winding_Direction, 0.2)
Third_Point = Intersection_fun(Third_Edge_1, Third_Edge_2, Second_Point,Vector_Third_Edge)
#print("I",Third_Edge_1,Third_Edge_2,Third_Point)
Path_Points.append(Third_Point)


def next_point_edge(Point_1, Point_2, Vertex_1, Vertex_2, Index_1, Index_2): 
    e = 0.01 #error
    friction_coefficient = 0.2

    #Defining egde Vector and Normals
    #Normal of Previous Triangle
    N1 = New_Normals[Index_1]
    #print("N1",N1,Index_1)
    
    #Normal of New_Triangle
    N2 = New_Normals[Index_2]
    #print("N2",N2,Index_2)

    T1 = np.subtract(Point_2,Point_1)
    T1 = T1/np.linalg.norm(T1)
    #print("T1",T1)

    #Determining Intersection point(New Point P2, and new vertexes)
    Third_Vertex = Third_Vertex_fun_2(Vertex_1, Vertex_2, Index_2)
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
    #print("GV", Geodesic_Vector)

    #Favored Direction
    Favored_Dir = Plane_Winding_Direction(N2,Winding_Direction,Winding_angle)
    #print("Favored_Dir",Favored_Dir)
    

    #Calculating tangents to curve and normal to plane
    Surface_normal = np.add(N1,N2)
    Surface_normal = Surface_normal/np.linalg.norm(Surface_normal)
    #print("Surface normal mod",np.linalg.norm(Surface_normal))
    #print("Surface Normal",Surface_normal)
    #print("#######")
    #Storage Variable
    Max= Favored_Dir
    Min= Geodesic_Vector
    Mid = np.add(Max,Min)
    Mid = Mid/np.linalg.norm(Mid)
    Curve_vector = np.add(Mid,-1*T1)
    Curve_vector = Curve_vector/np.linalg.norm(Curve_vector)

    #Geodesic Slippage calculation
    #Curve_Geodesic = np.subtract(Geodesic_Vector,T1)
    #Curve_Geodesic = Curve_Geodesic/np.linalg.norm(Curve_Geodesic)
    #print("Curve_Geodesic",Curve_Geodesic)
    #print("Curve geo mod",np.linalg.norm(Curve_Geodesic))
    #print(np.dot(Curve_Geodesic,-1*Surface_normal))
    #print(math.acos(np.dot(Curve_Geodesic,-1*Surface_normal)))
    #Slippage_Geodesic = math.tan(math.acos(np.dot(Curve_Geodesic,-1*Surface_normal)))  
    #print("Slippage Geodesic",Slippage_Geodesic)
    Dot_product = np.dot(Curve_vector,-1*Surface_normal)
    if(Dot_product>1):
        Dot_product =0.999
    Slippage_tendency= math.tan(math.acos(Dot_product))  
    a = 0
    while (((friction_coefficient - Slippage_tendency) > 0 and (friction_coefficient - Slippage_tendency) <e) == False and a <20):
        a = a+1 
        if (friction_coefficient - Slippage_tendency) < 0:
            Max = Mid
        if (friction_coefficient - Slippage_tendency) > 0:
            Min = Mid
        Mid = np.add(Max,Min)
        Mid = Mid/np.linalg.norm(Mid)
        #print(Mid_1)
        Curve_vector = np.add(Mid,-1*T1)
        Curve_vector = Curve_vector/np.linalg.norm(Curve_vector)
        Dot_product = np.dot(Curve_vector,-1*Surface_normal)
        if(Dot_product>1):
            Dot_product =0.999
        Slippage_tendency= math.tan(math.acos(Dot_product)) 
        #print(Slippage_tendency)

    #Define the Propogtion Vector
    Propogation_Vector = Mid
    #print("Propogation_Vector",Propogation_Vector)

    #Determining Intersection point(New Point P2, and new vertexes)
    #print(Vertex_1, Vertex_2, Third_Vertex, Propogation_Vector, N2, Point_2)
    Intersection_Point, New_Vertex_1 = new_point(Vertex_1, Vertex_2, Third_Vertex, Propogation_Vector, N2, Point_2)
    #print(Vertex_1,Vertex_2,Third_Vertex)
    #print(New_Vertex_1)
    #print("Intersection_Point",Intersection_Point)
    New_Vertex_2 = Third_Vertex
    #print(New_Vertex_2)

    New_Index_1 = Index_2
    #print(Index_2)
    if(Intersection_Point[axis]<End_Point[axis]):
        New_Index_2 = find_Index(New_Vertex_1,New_Vertex_2,Index_2)
    else:
        New_Index_2 = 0
    Forward_Array = np.zeros((6,3))
    New_Point_1 = Point_2
    New_Point_2 = Intersection_Point

    Forward_Array[0] = New_Point_1
    Forward_Array[1] = New_Point_2
    Forward_Array[2] = New_Vertex_1
    Forward_Array[3] = New_Vertex_2
    Forward_Array[4][0] = New_Index_1
    Forward_Array[5][0] = New_Index_2
    #print("Forward Array",Forward_Array)
    return Forward_Array

#Start Propogation Tool
Fourth_point_Index = find_Index(Third_Edge_1,Third_Edge_2,Third_Point_Index)
#print("Fourth Point Index",New_Vectors[Fourth_point_Index])
#print("Third point Index", New_Vectors[Third_Point_Index])
Propagation_Array = np.zeros((6,3))
Propagation_Array[0] = Second_Point
Propagation_Array[1] = Third_Point
Propagation_Array[2]= Third_Edge_1
Propagation_Array[3] = Third_Edge_2
Propagation_Array[4][0] = Third_Point_Index
Propagation_Array[5][0] = Fourth_point_Index

#Propagation_Array  = next_point_edge(Propagation_Array[0],Propagation_Array[1],Propagation_Array[2],Propagation_Array[3],int(Propagation_Array[4][0]),int(Propagation_Array[5][0]))
i = 2
#print(float(Winding_Direction[axis]*Path_Points[i][axis]) < float(End_Point[axis]))
while float(Winding_Direction[axis]*Propagation_Array[1][axis]) < float(End_Point[axis]):
    Propagation_Array  = next_point_edge(Propagation_Array[0],Propagation_Array[1],Propagation_Array[2],Propagation_Array[3],int(Propagation_Array[4][0]),int(Propagation_Array[5][0]))
    Path_Points.append(Propagation_Array[1])
    i = i+1
    print (i)
    print(Propagation_Array[1])

with open('file.py', 'w') as f:
  f.write('Path_Points = %s' % Path_Points)