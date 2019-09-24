import numpy as np
from stl import mesh
import math
import sys

Point_1 = np.array([-25,0,0])
Point_2 = np.array([-24.14815,7.07,-6.47])
Point_3 = np.array([-24.373,0,-5.56])
Normal = np.array([-0.99,0,-0.11])

def counter_clockwise_check(P1,P2,P3,N):
    V1 = np.subtract(P2,P1)
    V1 = V1/np.linalg.norm(V1)
    #print(V1)
    V2 = np.subtract(P3,P2)
    V2 = V2/np.linalg.norm(V2)
    #print(V2)
    Normal = np.cross(V1,V2)
    Normal = Normal/np.linalg.norm(Normal)
    #print(Normal)
    Sub = np.subtract(Normal,N)
    #print(Sub)
    a = np.linalg.norm(Sub)
    #print(a)
    if(a < 0.1):
        return P1,P2
    else:
        return P2,P1

#print(counter_clockwise_check(Point_1,Point_2,Point_3,Normal))

    