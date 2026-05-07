import pygame  #for windowing and event handling
from pygame.locals import *
from OpenGL.GL import *  #graphics library
from OpenGL.GLU import * #utilities for OpenGL
import random
import time

# --- Configuration ---
R, C = 20, 20  # Rows and Columns
CELL_SIZE = 30
WINDOW_WIDTH = C * CELL_SIZE
WINDOW_HEIGHT = R * CELL_SIZE

# --- Data Structures (As per Assignment) ---
# northWall[i][j] = 1 means wall exists above cell (i, j)
# eastWall[i][j] = 1 means wall exists to the right of cell (i, j)
# Row 0 is the bottom boundary; Column 0 (eastWall) handles the left boundary.
northWall = [[1 for _ in range(C)] for _ in range(R + 1)]
eastWall = [[1 for _ in range(C + 1)] for _ in range(R)]

visited = [[False for _ in range(C)] for _ in range(R)]
path_stack = []      # For solving (Red dots)
dead_ends = set()    # For solving (Blue dots)

def init_gl():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
def draw_maze():
    glColor3f(1.0, 1.0, 1.0) # White walls
    glLineWidth(2)
    glBegin(GL_LINES)
    # Draw North Walls
    for r in range(R + 1):
        for c in range(C):
            if northWall[r][c] == 1:
                glVertex2f(c * CELL_SIZE, r * CELL_SIZE)
                glVertex2f((c + 1) * CELL_SIZE, r * CELL_SIZE)
    # Draw East Walls
    for r in range(R):
        for c in range(C + 1):
            if eastWall[r][c] == 1:
                glVertex2f(c * CELL_SIZE, r * CELL_SIZE)
                glVertex2f(c * CELL_SIZE, (r + 1) * CELL_SIZE)
    glEnd()

def draw_dot(r, c, color):
    glColor3f(*color)
    glPointSize(10)
    glBegin(GL_POINTS)
    glVertex2f(c * CELL_SIZE + CELL_SIZE/2, r * CELL_SIZE + CELL_SIZE/2)
    glEnd()