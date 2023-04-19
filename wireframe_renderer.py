import pygame as game
import numpy as np

game.init()

WIDTH = 500
HEIGHT = 500

screen = game.display.set_mode((WIDTH, HEIGHT))
game.display.set_caption("Wireframe Renderer")

S = 100

PHI = ((1+np.sqrt(5))/2) * S
RPHI = S/PHI

vertices = []
lines = []

def init():
    global vertices, lines
    # ============================ SQUARE ============================
    #vertices = [
    #        [S,0,S],
    #        [-S,0,S],
    #        [S,0,-S],
    #        [-S,0,-S] ]
    #lines = [[0, 1], [0, 2], [2, 3], [1, 3]]

    # ============================= CUBE ============================= 
    vertices = [
        [-S, S, -S], 
        [-S, S, S], 
        [-S, -S, -S], 
        [-S, -S, S],
        [S, S, -S], 
        [S, S, S], 
        [S, -S, -S], 
        [S, -S, S],]
    lines = [[0, 1], [0, 2], [1, 3], [2, 3], [4, 5], [4, 6], [5, 7], [6, 7], [2, 6], [1, 5], [3, 7], [0, 4]]

    # ============================= PYRAMID =============================
    #vertices = [
    #    [-S, -S, -S], 
    #    [-S, -S, S],
    #    [S, -S, -S],
    #    [S, -S, S],
    #    [0, S, 0]
    #]
    #lines = [[0, 1], [0, 2], [1, 3], [2, 3], [0, 4], [1, 4], [2, 4], [3, 4]]

    # ============================= TETRAHEDRON =============================
    #vertices = [
    #    [200, -200, -100 * np.sqrt(3)],
    #    [-200, -200, -100 * np.sqrt(3)],
    #    [0, -200, 100 * np.sqrt(3)],
    #    [0, 200, (-100 * np.sqrt(3))/3]
    #]
    #lines = [[0, 1], [0, 2], [1, 2], [0, 3], [1, 3], [2, 3]]

    # ============================= DODECAHEDRON ============================
    #vertices = [
    #    [S, S, S],
    #    [S, S, -S],
    #    [S, -S, S],
    #    [S, -S, -S],
    #    [-S, S, S],
    #    [-S, S, -S],
    #    [-S, -S, S],
    #    [-S, -S, -S],
    #    [0, PHI, RPHI],
    #    [0, PHI, -RPHI],
    #    [0, -PHI, RPHI],
    #    [0, -PHI, -RPHI],
    #    [RPHI, 0, PHI],
    #    [RPHI, 0, -PHI],
    #    [-RPHI, 0, PHI],
    #    [-RPHI, 0, -PHI],
    #    [PHI, RPHI, 0],
    #    [PHI, -RPHI, 0],
    #    [-PHI, RPHI, 0],
    #  [-PHI, -RPHI, 0]]
    #lines = [[0,8], [0,12], [0,16],  
    #        [1, 9], [1, 13], [1, 16], 
    #        [2, 10], [2, 12], [2, 17], 
    #        [3, 11], [3, 13], [3, 17],
    #        [4, 8], [4, 14], [4, 18],
    #        [5, 9], [5, 15], [5, 18],
    #        [6, 10], [6, 14], [6, 19],
    #        [7, 11], [7, 15], [7, 19],
    #        [8, 9], [12, 14], [16, 17],
    #        [10, 11], [13, 15], [18, 19]
    #    ]

init()

p_vertices = []

focal_len = 1000

def project(x, y, z, f):
    xr = (x * f) / (f + z)
    yr = (y * f) / (f + z)
    return [(WIDTH/2) + xr, (HEIGHT/2) - yr]

def rotate(vertex, _t1, _t2, _t3):
    new_vertex = vertex[:]
    if _t1:
        rot_matrix = [
            [1, 0, 0],
            [0, np.cos(_t1), -np.sin(_t1)],
            [0, np.sin(_t1), np.cos(_t1)]
        ]
        new_vertex = np.matmul(new_vertex, rot_matrix)
    if _t2:
        rot_matrix = [
            [np.cos(_t2), 0, np.sin(_t2)],
            [0, 1, 0],
            [-np.sin(_t2), 0, np.cos(_t2)]
        ]
        new_vertex = np.matmul(new_vertex, rot_matrix)
    if _t3:
        rot_matrix = [
            [np.cos(_t3), -np.sin(_t3), 0],
            [np.sin(_t3), np.cos(_t3), 0],
            [0, 0, 1]
        ]
        new_vertex = np.matmul(new_vertex, rot_matrix)
    
    return new_vertex

def draw_line(xy1, xy2):
    game.draw.line(screen, (255, 255, 255), xy1, xy2)

running = True
t1 = 0
t2 = 0
t3 = 0
dt1 = 0
dt2 = 0
dt3 = 0
dt1 = np.pi / 500
dt2 = np.pi / 500
dt3 = np.pi / 500

v1x = []
v1y = []

bounce = False
bounce_step = 0
max_bounce_step = 100

while running:
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False

        if event.type == game.KEYDOWN:
            if event.key == game.K_SPACE:
                bounce = True

    
    screen.fill((0, 0, 0))

    if bounce:
        bounce_step += 1
        scale = 4 * abs((max_bounce_step/2) - bounce_step)

        if bounce_step < max_bounce_step / 2:
            S += scale/max_bounce_step
        else:
            S -= scale/max_bounce_step

        if bounce_step == max_bounce_step-1:
            bounce = False
            bounce_step = 0

        init()

    for vertex in range(len(vertices)):
        rotated = rotate(vertices[vertex], t1, t2, t3)
        v = rotated
        
        p = project(v[0], v[1], v[2], focal_len)
        p_vertices.append(p)

    for line in lines:
        draw_line(p_vertices[line[0]], p_vertices[line[1]])

    t1 += dt1
    t2 += dt2
    t3 += dt3

    p_vertices = []
    game.display.update()
