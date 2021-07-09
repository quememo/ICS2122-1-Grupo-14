"""

Python implementation of the maximum coverage location problem.

The program randomly generates a set of candidate sites, among 
which the K optimal candidates are selected. The optimization 
problem is solved by integer programming. 


"""


import numpy as np
from scipy.spatial import distance_matrix
from gurobipy import *
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon, Point
from numpy import random

def generate_candidate_sites(points, M=100):
    '''
    Generate M candidate sites with the convex hull of a point set
    Input:
        points: a Numpy array with shape of (N,2)
        M: the number of candidate sites to generate
    Return:
        sites: a Numpy array with shape of (M,2)
    '''
    hull = ConvexHull(points)
    polygon_points = points[hull.vertices]
    poly = Polygon(polygon_points)
    min_x, min_y, max_x, max_y = poly.bounds
    sites = []
    while len(sites) < M:
        random_point = Point([random.uniform(min_x, max_x),
                             random.uniform(min_y, max_y)])
        if (random_point.within(poly)):
            sites.append(random_point)
    return np.array([(p.x,p.y) for p in sites])

def mclp(points,K,radius,M,bases):
    """
    Solve maximum covering location problem
    Input:
        points: input points, Numpy array in shape of [N,2]
        K: the number of sites to select # 20
        radius: the radius of circle
        M: the number of candidate sites, which will randomly generated inside # 26
        the ConvexHull wrapped by the polygon

        Xj: 1 si se ocupa la base j, 0 e.o.c
        Yi: Denota si un nodo de demanda i es cubierto por una base en un radio 
        d(i,j): distancia euclidiana del nodo i a la base j
        radius: radio con la distancia maxima que cubre una base

        I: Conjunto de nodos de demanda (22000)
        J: Conjunto de nodos que podrían ser una base (26)
        K: Número de bases a seleccionar (20)
        ai = Cantidad de personas por nodo (=1)
        Ni = Bases que cumplen el radio a un nodo de llamada

    FO: Maximizar la cantidad de nodos de llamada atendidos (Yi)

    Restricciones
    1. Si un nodo de llamada (Yi) es cubierto, debe haber al menos una base seleccionada cercana a él
    2. La cantidad de bases asignadas debe ser igual a la establecida (K, P en paper)  

    Return:
        opt_sites: locations K optimal sites, Numpy array in shape of [K,2]
        f: the optimal value of the objective function
    """
    print('----- Configurations * -----')
    print('  Number of points %g' % points.shape[0])
    print('  K %g' % K)
    print('  Radio %g' % radius)
    print('  M %g' % bases.shape[0]) # M
    import time
    start = time.time()
    #sites = generate_candidate_sites(bases,M)
    J = bases.shape[0]
    #J = sites.shape[0]
    I = points.shape[0]
    D = distance_matrix(points,bases)
    #D = distance_matrix(points,sites)
    mask1 = D<=radius
    D[mask1]=1
    D[~mask1]=0
    # Build model
    m = Model()
    # Add variables
    x = {}
    y = {}
    for i in range(I):
      y[i] = m.addVar(vtype=GRB.BINARY, name="y%d" % i)
    for j in range(J):
      x[j] = m.addVar(vtype=GRB.BINARY, name="x%d" % j)

    m.update()
    # Add constraints
    m.addConstr(quicksum(x[j] for j in range(J)) == K)

    for i in range(I):
        m.addConstr(quicksum(x[j] for j in np.where(D[i]==1)[0]) >= y[i])

    m.setObjective(quicksum(y[i]for i in range(I)),GRB.MAXIMIZE)
    m.setParam('OutputFlag', 0)
    m.optimize()
    end = time.time()
    print('----- Output -----')
    print('  Running time : %s seconds' % float(end-start))
    print('  Optimal coverage points: %g' % m.objVal)
    percentage_coverage = (m.objVal/I)*100
    print(f'  Percentage coverage: {percentage_coverage}% ')
    
    solution = []
    if m.status == GRB.Status.OPTIMAL:
        for v in m.getVars():
            # print v.varName,v.x
            if v.x==1 and v.varName[0]=="x":
               solution.append(int(v.varName[1:]))
    opt_sites = bases[solution]
    #opt_sites = sites[solution]
    return opt_sites,m.objVal

def plot_input(points):
    '''
    Plot the result
    Input:
        points: input points, Numpy array in shape of [N,2]
        opt_sites: locations K optimal sites, Numpy array in shape of [K,2]
        radius: the radius of circle
    '''
    from matplotlib import pyplot as plt
    fig = plt.figure(figsize=(12,8))
    plt.scatter(points[:,0],points[:,1], s=2, c='C0')
    ax = plt.gca()
    ax.axis('equal')
    ax.tick_params(axis='both',left=False, top=False, right=False,
                       bottom=False, labelleft=False, labeltop=False,
                       labelright=False, labelbottom=False)

def plot_result(points,opt_sites,radius):
    '''
    Plot the result
    Input:
        points: input points, Numpy array in shape of [N,2]
        opt_sites: locations K optimal sites, Numpy array in shape of [K,2]
        radius: the radius of circle
    '''
    from matplotlib import pyplot as plt
    fig = plt.figure(figsize=(12,8))
    plt.scatter(points[:,0],points[:,1],s=2, c='C0') # C0
    ax = plt.gca()
    plt.scatter(opt_sites[:,0],opt_sites[:,1],s=45,c='C1',marker='*')
    for site in opt_sites:
        circle = plt.Circle(site, radius, color='C1',fill=False,lw=2) # C1
        ax.add_artist(circle)
    ax.axis('equal')
    ax.tick_params(axis='both',left=False, top=False, right=False,
                       bottom=False, labelleft=False, labeltop=False,
                       labelright=False, labelbottom=False)


def plot_result2(points,opt_sites,radius):
    '''
    Plot the result
    Input:
        points: input points, Numpy array in shape of [N,2]
        opt_sites: locations K optimal sites, Numpy array in shape of [K,2]
        radius: the radius of circle
    '''
    from matplotlib import pyplot as plt
    fig = plt.figure(figsize=(12,8))
    plt.scatter(points[:,0],points[:,1],s=2, c='C0') # C0
    ax = plt.gca()
    plt.scatter(opt_sites[:,0],opt_sites[:,1],s=48 ,c='C3') # marker='*' # C3
    ax.axis('equal')
    ax.tick_params(axis='both',left=False, top=False, right=False,
                       bottom=False, labelleft=False, labeltop=False,
                       labelright=False, labelbottom=False)
