def Object_rotation(Vector_x,Vector_y,Vector_z, Object):
    Rotation_matrix = np.zeros((3,3))
    Rotation_matrix[0] = Vector_x
    Rotation_matrix[1] = Vector_y
    Rotation_matrix[2] = Vector_z
    Rotation_matrix = preprocessing.normalize(Rotation_matrix, norm='l2')
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
    Rotation_matrix = preprocessing.normalize(Rotation_matrix, norm='l2')
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

New_Vectors = Object_rotation(Flat_Normal_x, Flat_Normal_y, Flat_Normal_z,New_Vectors)
New_Vectors = Object_translation(New_Vectors, Zero_Point)
#print(New_Vectors)




i = 0
while path[i][0] < class.max_length('cylinder.stl'):
    path_points[i+1] = next_point(path_points[i],path_points[i-1])
    i += 1

def next_point_edge( x ): 
    e = 0.01 #error
    theta_max = 90 
    theta_min =-90
    start_angle = 0
    desired_angle = 45
    friction_coefficient = 0.2

    T1 = np.zeroes(3) #
    Edge_Vector = np.zeroes(3)
    N1 = np.zeroes(3) #Normal to Triangle 1
    N2 = np.zeroes(3) #Normal to Triangle 2
    Angle_between_planes = math.acos(np.dot(N1,N2))

    #Input angle - 1.5708 = pi/2
    input_angle = 1.5708 - math.acos(np.dot(T1,Edge_Vector))
    Zero_degree_Vector = np.cross(Edge_Vector, N2)
    Geodesic_Vector = np.add(math.cos(input_angle)*Zero_degree_Vector, math.sin(input_angle)*Edge_Vector)

    #Normalising the vectors
    Geodesic_Vector = preprocessing.normalize(Geodesic_Vector, norm='l2')

    #Calculating tangents to curve and normal to plane
    Surface_normal = preprocessing.normalize(np.add(N1,N2), norm='l2')

    #Storage Variable
    Max_1 = Edge_Vector
    Max_2 = Geodesic_Vector
    Min_1 = Geodesic_Vector
    Min_2 = -1*Edge_Vector
    Mid_1 = preprocessing.normalize(np.add(Max_1,Min_1), norm='l2')
    Mid_2 = preprocessing.normalize(np.add(Max_2,Min_2), norm='l2')
    Curve_max = preprocessing.normalize(np.add(Mid_1,T1), norm='l2')
    Curve_min = preprocessing.normalize(np.add(Mid_2,T1), norm='l2')

    Slippage_tedency_max = math.tan(math.acos(np.dot(Curve_max,-1*Surface_normal)))
    while (((friction_coefficient - Slippage_tedency_max) > 0 & (friction_coefficient - Slippage_tedency_max) <e) == False):           
        if (friction_coefficient - Slippage_tedency_max) < 0:
            Max_1 = Mid_1
        if (friction_coefficient - Slippage_tedency_max) > 0:
            Min_1 = Mid_1
        Mid_1 = preprocessing.normalize(np.add(Max_1,Min_1), norm='l2')
        Curve_max = preprocessing.normalize(np.add(Mid_1,T1), norm='l2')
        Slippage_tedency_max = math.tan(math.acos(np.dot(Curve_max,-1*Surface_normal)))
    
    Slippage_tedency_min = math.tan(math.acos(np.dot(Curve_min,-1*Surface_normal)))
    while (((friction_coefficient - Slippage_tedency_min) > 0 & (friction_coefficient - Slippage_tedency_min) <e) == False):
        if (friction_coefficient - Slippage_tedency_min) < 0:
            Max_2 = Mid_2
        if (friction_coefficient - Slippage_tedency_min) > 0:
            Min_2 = Mid_2
        Mid_2 = preprocessing.normalize(np.add(Max_2,Min_2), norm='l2')
        Curve_min = preprocessing.normalize(np.add(Mid_2,T1), norm='l2')
        Slippage_tedency_min = math.tan(math.acos(np.dot(Curve_min,-1*Surface_normal)))

def next_point_vertex( Point ): 
    Index = class.Triangle_Index(Point)
    section = [] 
    while i < Index.shape[0]:
        section.append


###########################

def next_point_vertex(Point_1, Point_2, Index_1 ): 
    Index = 
    section = [] 
    while i < Index.shape[0]:
        section.append


Flat_points = np.asarray(Flat_points)
Flat_points = np.unique(Flat_points)

#Defining a point on the flat surface of the stl file (Zero_Point)
Zero_Point = Unique_Points[Flat_points[0]]
Edge_Point_Index = Point_Index_fun(Points, Zero_Point)[0]

#Defining Winding Direction
Winding_Direction = -1*Cylinder_normals[Edge_Point_Index]
axis = int(np.nonzero(Winding_Direction)[0])
Start_Point = np.zeros(3)

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
New_Points_list = New_Points
New_Points_list.tolist()

#Define Start_Point for Propagation Algorithm
for i in range(Cylinder_vectors.shape[0]):
    for j in range(3):
        if (Cylinder_vectors[i][j][axis] == Zero_Point[axis]):
            Start_Point = Cylinder_vectors[i][j]
            break

print(Start_Point)

Cylinder_mod = mesh.Mesh(np.zeros(New_Vectors.shape[0], dtype=mesh.Mesh.dtype))
Cylinder_mod.vectors = New_Vectors
Cylinder_mod.save('cylinder_mod.stl')



    for i in range(len(Path_Points)-1):
        glBegin(GL_LINES)
        glColor(0, 0, 1)
        glVertex(Path_Points[i][0],Path_Points[i][1], Path_Points[i][2])
        glVertex(Path_Points[i+1][0],Path_Points[i+1][1], Path_Points[i+1][2])
        glEnd()

    for i in range(Triangle_no):
        glBegin(GL_LINE_LOOP)
        glColor(0, 1, 0)
        glVertex(Cylinder[i][0][0], Cylinder[i][0][1], Cylinder[i][0][2])
        glVertex(Cylinder[i][1][0], Cylinder[i][1][1], Cylinder[i][1][2])
        glVertex(Cylinder[i][2][0], Cylinder[i][2][1], Cylinder[i][2][2])
        glEnd()