import numpy as np
from stl import mesh
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import sys
from mpl_toolkits import mplot3d
from matplotlib import pyplot

# Using an existing stl file:
your_mesh = mesh.Mesh.from_file('cylinder_creo.stl')
Cylinder = your_mesh.vectors
Triangle_no = Cylinder.shape[0]


def draw_cylinder():

    for i in range(Triangle_no):
        glBegin(GL_LINE_LOOP)
        glColor(0,1,0)
        for j in range(3):
            glVertex3fv(Cylinder[i][j])
        glEnd()

pygame.init()
(width, height) = (800, 600)
screen = pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
clock = pygame.time.Clock()
rotation = 0.0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    rotation += 0.05
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30, float(width)/height, 1, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslate(0, -100, -400)#move back far enough to see this object 
    glRotate(rotation, 1, 1, 1)#NOTE: this is applied BEFORE the translation due to OpenGL multiply order

    draw_cylinder()
    pygame.display.flip()
    clock.tick(60)

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
    for point in Path_Points:
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
        
    rotation += 0.0
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30, float(width)/height, 1, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslate(0, -100, -500)#move back far enough to see this object 
    glRotate(rotation, 0, 1, 0)#NOTE: this is applied BEFORE the translation due to OpenGL multiply order

    draw_cylinder()
    pygame.display.flip()
    clock.tick(60)