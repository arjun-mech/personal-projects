import numpy as np
import math
import sys
from Index import *
from Intersection import *

def interpolate(x1,y1,x2,y2):
    x1,y1 = domain_sort(x1,y1)
    x2,y2 = domain_sort(x2,y2)

    all_points = Union(x1,x2)

    f1 = np.interp(all_points, x1, y1)
    #print(f1)
    f2 = np.interp(all_points, x2, y2)
    #print(f2)

    start_bool = bool(f1[0]>f2[0])
    for i in range(len(all_points)):
        c_bool = bool(f1[i]>f2[i])
        if (start_bool != c_bool):
            crossover_point_pre = all_points[i-1]
            #print(crossover_point_pre)
            crossover_point_post = all_points[i]
            #print(crossover_point_post)
            break

    crossover_angle_pre_f1 = np.interp(crossover_point_pre,all_points,f1)
    crossover_angle_pre_f2 = np.interp(crossover_point_pre,all_points,f2)
    crossover_angle_post_f1 = np.interp(crossover_point_post,all_points,f1)
    crossover_angle_post_f2 = np.interp(crossover_point_post,all_points,f2)

    p1 = [crossover_point_pre,crossover_angle_pre_f1]
    p1 = np.asarray(p1)
    #print(p1)
    p2 = [crossover_point_pre,crossover_angle_pre_f2]
    p2 = np.asarray(p2)
    #print(p2)
    p3 = [crossover_point_post,crossover_angle_post_f1]
    p3 = np.asarray(p3)
    #print(p3)
    p4 = [crossover_point_post,crossover_angle_post_f2]
    p4 = np.asarray(p4)
    #print(p4)

    intersection_point = Intersection_fun_2d(p1,p3,p2,p4)
    #print(intersection_point)
    index = func(all_points,intersection_point[0])

    #print(index)
    r1 = f1[:index]
    r2 = f2[index:]
    a = intersection_point[1]
    r1 = np.append(r1,a)
    angles = np.append(r1,r2)
    #print(r1)
    all_points = insert(all_points,intersection_point[0]) 
    return all_points,angles,intersection_point[0]

def Union(lst1, lst2): 
    final_list = sorted(lst1 + lst2) 
    return final_list 

def func(l, x):
    for i in l:
        if i > x: return l.index(i)

def insert(list, n): 
      
    # Searching for the position 
    for i in range(len(list)): 
        if list[i] > n: 
            index = i 
            break
      
    # Inserting n in the list 
    list = list[:i] + [n] + list[i:] 
    return list

def join_list(a,b,x):
    temp = a.extend(x)
    temp = temp+b
    return temp

def domain_sort(x,y):
    #print(x[0],x[len(x)-1])
    if(x[0] <= x[len(x)-1]):
        return x,y
    else:
        x.reverse()
        y.reverse()
        return x,y

def path_rotation(path1,path2,intercept,axis):
    path1_list = np.asarray(path1)
    path2_list = np.asarray(path2)
    path_centre_1 = path1_list[:axis]
    path_centre_2 = path1_list[:axis]
    


def rotate_angle(centre, point_1, point_2):
    vector_1 = np.subtract(point_1,centre)
    vector_2 = np.subtract(point_2,centre)
    rot_angle = math.acos(np.dot(vector_1,vector_2))

    return rot_angle




#x = [10,9,8,7,6,5,4,3,2,1]
#y = [100,90,80,70,0,50,40,30,20,10]

#l = [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5]


#print(domain_sort(x,y))
