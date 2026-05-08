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

# Mouse position
mouse_pos = None

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

def generate_maze():
    global mouse_pos

    stack = [(0, 0)]
    visited[0][0] = True

    while stack:
        curr_r, curr_c = stack[-1]

        # Update mouse position
        mouse_pos = (curr_r, curr_c)

        neighbors = []

        # Check neighbors: (dr, dc, wall_type, wall_pos)
        # Directions: Up, Down, Left, Right
        dirs = [
            (1, 0, 'N', (curr_r + 1, curr_c)),
            (-1, 0, 'N', (curr_r, curr_c)),
            (0, -1, 'E', (curr_r, curr_c)),
            (0, 1, 'E', (curr_r, curr_c + 1))
        ]

        for dr, dc, w_type, (wr, wc) in dirs:
            nr, nc = curr_r + dr, curr_c + dc

            if 0 <= nr < R and 0 <= nc < C and not visited[nr][nc]:
                neighbors.append((nr, nc, w_type, (wr, wc)))

        if neighbors:
            nr, nc, w_type, (wr, wc) = random.choice(neighbors)

            # "Eat" the wall
            if w_type == 'N':
                northWall[wr][wc] = 0
            else:
                eastWall[wr][wc] = 0

            visited[nr][nc] = True
            stack.append((nr, nc))

            # Visualization sync
            render_frame()
            time.sleep(0.05)

        else:
            stack.pop()

def render_frame():
    glClear(GL_COLOR_BUFFER_BIT)

    draw_maze()

    # Draw green mouse
    if mouse_pos:
        draw_dot(mouse_pos[0], mouse_pos[1], (0, 1, 0))

    for r, c in path_stack:
        draw_dot(r, c, (1, 0, 0))

    for r, c in dead_ends:
        draw_dot(r, c, (0, 0, 1))

    pygame.display.flip()

def solve_maze(start, end):
    stack = [start]
    visited_solve = {start}

    while stack:
        curr = stack[-1]

        if curr == end:
            return True

        r, c = curr
        neighbors = []

        if northWall[r + 1][c] == 0 and (r + 1, c) not in visited_solve:
            neighbors.append((r + 1, c))

        if northWall[r][c] == 0 and (r - 1, c) not in visited_solve:
            neighbors.append((r - 1, c))

        if eastWall[r][c] == 0 and (r, c - 1) not in visited_solve:
            neighbors.append((r, c - 1))

        if eastWall[r][c + 1] == 0 and (r, c + 1) not in visited_solve:
            neighbors.append((r, c + 1))

        if neighbors:
            next_cell = random.choice(neighbors)
            visited_solve.add(next_cell)
            stack.append(next_cell)

        else:
            dead_ends.add(stack.pop())

        global path_stack
        path_stack = list(stack)

        render_frame()
        time.sleep(0.05)

def main():
    pygame.init()

    pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT),
        DOUBLEBUF | OPENGL
    )

    pygame.display.set_caption("Maze Gen & Solve")

    init_gl()

    generate_maze()

    start = (random.randint(0, R - 1), 0)
    end = (random.randint(0, R - 1), C - 1)

    eastWall[start[0]][0] = 0
    eastWall[end[0]][C] = 0

    solve_maze(start, end)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        render_frame()

    pygame.quit()

if __name__ == "__main__":
    main()