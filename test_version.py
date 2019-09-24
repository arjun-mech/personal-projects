import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
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
from slippage_v2 import *
from STL_Formatting import *
import matplotlib.pyplot as plt
from join_path import *

# Using an existing stl file:
object_mesh = mesh.Mesh.from_file('cone_solidworks.stl')
Cylinder_vectors = object_mesh.vectors
Cylinder_unorm = object_mesh.normals
Triangle_no = Cylinder_vectors.shape[0]
Cylinder_normals = preprocessing.normalize(Cylinder_unorm, norm='l2')

Format_STL = STL_Formatting(Cylinder_vectors,Cylinder_normals)
New_Vectors,New_Normals,Winding_Direction,axis,Zero_Point,Edge_Point_Index = Format_STL.eliminate_flatpoints()

print("Zero_Point",Zero_Point)
#Define Start_Point for Propagation Algorithm
for i in range(New_Vectors.shape[0]):
    for j in range(3):
        if (New_Vectors[i][j][axis] == Zero_Point[axis]):
            Start_Point = New_Vectors[i][j]
            break

New_Points = Make_Points(New_Vectors)


#Second Point
Winding_angle = (math.pi/18)*6
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

print("First Point", Start_Point)
print("Second Point",Second_Point)
#Check for Direction Sanity
Dir_1 = np.cross(New_Normals[Start_Point_Index],Winding_Direction)
Dir_1 = Dir_1/np.linalg.norm(Dir_1)
print("D_1",Dir_1)
Dir_2 = np.subtract(Second_Point,Start_Point)
Dir_2 = Dir_2/np.linalg.norm(Dir_2)
print("D_2",Dir_2)

# setting the absolute and relative tolerance 
rtol = 1e-05
atol = 1e-08
#print(np.allclose(Dir_1, Dir_2, rtol, atol))

if(np.allclose(Dir_1, Dir_2, rtol, atol) == False):
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
Vector_Third_Edge = Plane_Winding_Direction(New_Normals[Third_Point_Index],Winding_Direction, 0.3)
print("Vector_Third_Edge",Vector_Third_Edge)
print("Third_Edge_1",Third_Edge_1)
print("Third_Edge_2",Third_Edge_2)
Third_Point = Intersection_fun(Third_Edge_1, Third_Edge_2, Second_Point,Vector_Third_Edge)
#print("I",Third_Edge_1,Third_Edge_2,Third_Point)
Path_Points.append(Third_Point)

#Start Propogation Tool
Fourth_point_Index = find_Index(Third_Edge_1,Third_Edge_2,Third_Point_Index,New_Points)

Propagation_Array = np.zeros((6,3))
Propagation_Array[0] = Second_Point
Propagation_Array[1] = Third_Point
Propagation_Array[2]= Third_Edge_1
Propagation_Array[3] = Third_Edge_2
Propagation_Array[4][0] = Third_Point_Index
Propagation_Array[5][0] = Fourth_point_Index

S1 = slippage_v2(New_Vectors,New_Normals,End_Point,axis,Winding_Direction,Winding_angle)
path_angle_local = [90,90,90]

print("Winding_Direction",Winding_Direction)
print("First Point", Start_Point)
print("Second Point",Second_Point)
print("Third_Point", Third_Point)
print("End Point", End_Point)

while float(Winding_Direction[axis]*Propagation_Array[1][axis]) < float(End_Point[axis]*Winding_Direction[axis]):
    Propagation_Array,angle  = S1.next_point_edge(Propagation_Array[0],Propagation_Array[1],Propagation_Array[2],Propagation_Array[3],int(Propagation_Array[4][0]),int(Propagation_Array[5][0]))
    Path_Points.append(Propagation_Array[1])
    path_angle_local.append(angle*180/3.14)

##############################Return Path##############################################
print("#######################Starting Reverse Path############################")
#Define Start_Point for Propagation Algorithm
for i in range(New_Vectors.shape[0]):
    for j in range(3):
        if (New_Vectors[i][j][axis] == End_Point[axis]):
            Start_Point_b = New_Vectors[i][j]
            break

Winding_Direction_b = Winding_Direction*-1

#Second Point

Path_Points_b = []
Start_Point_Index_b = Point_Index_fun(New_Points, Start_Point_b)[0]
Second_Point_b = np.zeros(3) 

for i in range(3):
    if (New_Vectors[Start_Point_Index_b][i][axis] == Start_Point_b[axis]):
        if (np.array_equal(New_Vectors[Start_Point_Index_b][i], Start_Point_b) == False):
            Second_Point_b = New_Vectors[Start_Point_Index_b][i]
            break
Second_Point_Index_b = Start_Point_Index_b


#Check for Direction Sanity
Dir_1_b = np.cross(New_Normals[Start_Point_Index_b],Winding_Direction_b)
Dir_1_b = Dir_1_b/np.linalg.norm(Dir_1_b)
Dir_2_b = np.subtract(Second_Point_b,Start_Point_b)
Dir_2_b = Dir_2_b/np.linalg.norm(Dir_2_b)

if(np.allclose(Dir_1_b, Dir_2_b, rtol, atol)== False):
    Temp_b = Second_Point_b
    Second_Point_b = Start_Point_b
    Start_Point_b = Temp_b

Path_Points_b.append(Start_Point_b)
Path_Points_b.append(Second_Point_b)

#Third Point
Third_Point_b = np.zeros(3)
Third_Edge_1_b = np.zeros(3)
Third_Point_Index_list_b = Point_Index_fun(New_Points,Second_Point_b)
Third_Point_Index_list_b.remove(Second_Point_Index_b)
for i in range(len(Third_Point_Index_list_b)):
    for j in range(3):
        if(np.array_equal(New_Vectors[Third_Point_Index_list_b[i]][j],Second_Point_b) == False):
            if(New_Vectors[Third_Point_Index_list_b[i]][j][axis] == Second_Point_b[axis]):
                Third_Edge_1_b = New_Vectors[Third_Point_Index_list_b[i]][j]
                Third_Point_Index_b = Third_Point_Index_list_b[i]
                break
Third_Edge_2_b = Third_Vertex_fun(Third_Edge_1_b, Second_Point_b, Third_Point_Index_b,New_Vectors)
Vector_Third_Edge_b = Plane_Winding_Direction(New_Normals[Third_Point_Index_b],Winding_Direction_b, 0.6)
print("Vector_Third_Edge_b",Vector_Third_Edge_b)
print("Third_Edge_1_b",Third_Edge_1_b)
print("Third_Edge_2_b",Third_Edge_2_b)

Third_Point_b = Intersection_fun(Third_Edge_2_b, Third_Edge_1_b, Second_Point_b,Vector_Third_Edge_b)

#print("I",Third_Edge_1,Third_Edge_2,Third_Point)
Path_Points_b.append(Third_Point_b)

#Start Propogation Tool
Fourth_point_Index_b = find_Index(Third_Edge_1_b,Third_Edge_2_b,Third_Point_Index_b,New_Points)

Propagation_Array_b = np.zeros((6,3))
Propagation_Array_b[0] = Second_Point_b
Propagation_Array_b[1] = Third_Point_b
Propagation_Array_b[2]= Third_Edge_1_b
Propagation_Array_b[3] = Third_Edge_2_b
Propagation_Array_b[4][0] = Third_Point_Index_b
Propagation_Array_b[5][0] = Fourth_point_Index_b

S1_b = slippage_v2(New_Vectors,New_Normals,Start_Point,axis,Winding_Direction_b,Winding_angle)

path_angle_local_b = [90,90,90]

print("Start_Point_b",Start_Point_b)
print("Second_Point_b",Second_Point_b)
print("Third_Point_b",Third_Point_b)
print("End_Point",Start_Point)
print("Winding_Direction_b",Winding_Direction_b)

while (float(Winding_Direction_b[axis]*Propagation_Array_b[1][axis]) < float(Start_Point[axis]*Winding_Direction_b[axis])):
    Propagation_Array_b,angle_b  = S1_b.next_point_edge(Propagation_Array_b[0],Propagation_Array_b[1],Propagation_Array_b[2],Propagation_Array_b[3],int(Propagation_Array_b[4][0]),int(Propagation_Array_b[5][0]))
    Path_Points_b.append(Propagation_Array_b[1])
    path_angle_local_b.append(angle_b*180/3.14)

#print(Path_Points)
#print(Path_Points_b)

#########################################################################################

def vertical_angle_calc(point,next_point,Winding_Direction):
    centre = np.zeros(3)
    centre[axis] = point[axis]

    path_vector = np.subtract(next_point,point)
    path_vector = path_vector/np.linalg.norm(path_vector)
    Dot_product = np.dot(path_vector,Winding_Direction)
    #print("Dot_product",Dot_product)
    if(Dot_product>1):
        Dot_product = 0.999
    if(Dot_product<-1):
        Dot_product = -0.999   
    angle = 180*(math.acos(Dot_product)/(math.pi))

    return angle,centre[axis]

path_angle = []
path_centre = []
for i in range(len(Path_Points)-1):
    angle,centre = vertical_angle_calc(Path_Points[i],Path_Points[i+1],Winding_Direction)
    print(angle,centre)
    path_angle.append(angle)
    path_centre.append(centre)

path_angle_b = []
path_centre_b = []
for i in range(len(Path_Points_b)-1):
    angle,centre = vertical_angle_calc(Path_Points_b[i],Path_Points_b[i+1],Winding_Direction_b)
    print(angle,centre)
    path_angle_b.append(angle)
    path_centre_b.append(centre)

#Write CSV File

import csv
with open('some.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(map(lambda x: [x], path_centre))
with open('some_1.csv', 'w', newline='') as f_1:
    writer = csv.writer(f_1)
    writer.writerows(map(lambda x: [x], path_angle))

plt.plot(path_centre,path_angle,color = 'green')
plt.plot(path_centre_b,path_angle_b,color = 'blue')
plt.axis([-10, 60, 0, 90])
plt.show()

print("###")
print("p",path_angle_local)


def draw_cylinder():

    for i in range(Triangle_no):
        glBegin(GL_LINE_LOOP)
        glColor(0,1,0)
        for j in range(3):
            glVertex3fv(Cylinder_vectors[i][j])
        glEnd()
    
    glLineWidth(1.0)
    glBegin(GL_LINE_STRIP)
    glColor(1, 0, 0)
    for point in Path_Points_b:
        glVertex3fv(point)
    glEnd()

pygame.init()
(width, height) = (1200, 900)
screen = pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
clock = pygame.time.Clock()
rotation = 0.0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    rotation += 1
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30, float(width)/height, 1, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslate(0, 0, -500)#move back far enough to see this object 
    glRotate(rotation, 0, 1, 0)#NOTE: this is applied BEFORE the translation due to OpenGL multiply order

    draw_cylinder()
    pygame.display.flip()
    clock.tick(60)

