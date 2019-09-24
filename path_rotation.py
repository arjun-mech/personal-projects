import numpy as np
import math
import sys

class Rotation:

    def __init__(self, path_1, path_2,axis, intercept):
        self.path_1 = path_1
        self.path_2 = path_2
        self.l_1 = path_1[:,0]
        self.l_2 = path_2[:,0]
        self.axis = axis
        self.dir = np.zeroes(3)
        self.dir[self.axis] = 1
        self.angle_path_1 = self.angle_array(self.path_1)



    def angle_array(self,path):
        angle_list = []

        for i in range(self.path.shape[0]-1):
            angle_list.append(self.vertical_angle_calc(path[i],path[i+1]))

    def rotate_angle(self, point_1, point_2):
        vector_1 = np.subtract(point_1,self.centre)
        vector_2 = np.subtract(point_2,self.centre)
        rot_angle = math.acos(np.dot(vector_1,vector_2))

        return rot_angle

    def rotation_intersection(self,Points):
        gvv
