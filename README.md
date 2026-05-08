# Maze Generation and Solving using PyOpenGL

## Overview

This project generates and solves a 2D maze using Python, Pygame, and PyOpenGL.

- White lines → maze walls
- Red dots → current solving path
- Blue dots → dead ends

---

## How It Works

### Maze Generation

The maze is generated using the Recursive Backtracking (DFS) algorithm.

Steps:

1. Start from a cell
2. Mark it as visited
3. Randomly choose an unvisited neighbor
4. Remove the wall between cells
5. Continue until all cells are visited

The maze is stored using:

- `northWall` → horizontal walls
- `eastWall` → vertical walls

---

### Maze Solving

The maze is solved using stack-based backtracking.

Steps:

1. Start from entrance
2. Move through available paths
3. Backtrack when reaching dead ends
4. Continue until the exit is found

---

# loom record

https://www.loom.com/share/4f237fb14869439296f62658dfc3a97a
