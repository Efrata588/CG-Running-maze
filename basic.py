import random
# Defining the maze grid
R, C = 10, 10

northWall = [[1 for _ in range(C)] for _ in range(R)]
eastWall  = [[1 for _ in range(C)] for _ in range(R)]
visited   = [[0 for _ in range(C)] for _ in range(R)]

#Mouse or current position
current_i, current_j = 0, 0

#Stack for backtracking
stack = []


"""function to filter valid neighbours of the current cell."""

def get_neighbors(i, j):
    neighbors = []

    # UP
    if i > 0 and visited[i-1][j] == 0:
        neighbors.append((i-1, j))

    # DOWN
    if i < R-1 and visited[i+1][j] == 0:
        neighbors.append((i+1, j))

    # LEFT
    if j > 0 and visited[i][j-1] == 0:
        neighbors.append((i, j-1))

    # RIGHT
    if j < C-1 and visited[i][j+1] == 0:
        neighbors.append((i, j+1))

    return neighbors

# Function to remove walls between current cell and chosen neighbor


def remove_wall(ci, cj, ni, nj):
    # moving DOWN
    if ni == ci + 1:
        northWall[ni][nj] = 0

    # moving UP
    elif ni == ci - 1:
        northWall[ci][cj] = 0

    # moving RIGHT
    elif nj == cj + 1:
        eastWall[ci][cj] = 0

    # moving LEFT
    elif nj == cj - 1:
        eastWall[ni][nj] = 0


# full generation loop
def generate_maze():
    global current_i, current_j

    visited[current_i][current_j] = 1
    stack.append((current_i, current_j))

    while stack:
        i, j = stack[-1]

        neighbors = get_neighbors(i, j)

        # CASE 1: still have choices
        if neighbors:
            ni, nj = random.choice(neighbors)

            remove_wall(i, j, ni, nj)

            visited[ni][nj] = 1
            stack.append((ni, nj))

        # CASE 2: dead end
        else:
            stack.pop()

