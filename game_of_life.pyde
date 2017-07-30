import time
import copy

CANVAS_SIZE = 800
GRID_DENSITY = 80
CELL_WIDTH = CANVAS_SIZE / GRID_DENSITY

cells = [[0 for i in range(GRID_DENSITY)] for j in range(GRID_DENSITY)]
game_is_running = False

def setup():
    size(CANVAS_SIZE, CANVAS_SIZE)
    stroke(0)

def drawGridLines(density, gridSize):
    for i in range(1, density):
        separator = (gridSize /density) * i
        line(separator, 0, separator, gridSize)
        line(0, separator, gridSize, separator)
    
def drawCells():
    for i in range(0, GRID_DENSITY):
        for j in range(0, GRID_DENSITY):
            if cells[i][j] == 1:
                fill(50, 50, 50)
                rect(i * CELL_WIDTH, j * CELL_WIDTH, CELL_WIDTH, CELL_WIDTH)

def calcNeighbors(row, col):
    num_neighbors = 0
    for m in range(-1, 2):
        for n in range(-1, 2):
            if m == 0 and n == 0:
                continue
            if row + m < 0 or col + n < 0:
                continue
            if row + m >= GRID_DENSITY or col + n >= GRID_DENSITY:
                continue
            if cells[row+m][col+n] == 1:
                num_neighbors += 1
    return num_neighbors

def willLive(cell, num_neighbors):
    if num_neighbors == 3 or (cell == 1 and num_neighbors == 2):
        return 1
    return 0

def processGame():
    buffer_grid = copy.deepcopy(cells)
    for i in range(0, GRID_DENSITY):
        for j in range(0, GRID_DENSITY):
            buffer_grid[i][j] = willLive(cells[i][j], calcNeighbors(i, j))

    return buffer_grid
    
def draw():
    global cells
    global game_is_running
    background(255, 255, 255)
    drawGridLines(GRID_DENSITY, CANVAS_SIZE)
    drawCells()
    if game_is_running:
        buffer_grid = copy.deepcopy(processGame())
        cells = copy.deepcopy(buffer_grid)
        time.sleep(0.125)
    
def mouseClicked():
    x = mouseX / CELL_WIDTH
    y = mouseY / CELL_WIDTH
    cells[x][y] = 1 - cells[x][y]

def mouseDragged():
    x = mouseX / CELL_WIDTH
    y = mouseY / CELL_WIDTH
    cells[x][y] = 1 - cells[x][y]
    
def keyPressed():
    global game_is_running
    game_is_running = not game_is_running
    
    