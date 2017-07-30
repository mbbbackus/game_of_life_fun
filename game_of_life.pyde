import time
import copy

CANVAS_WIDTH = 606
CELL_DENSITY = 303
CELL_WIDTH = CANVAS_WIDTH / CELL_DENSITY

cells = [[0 for i in range(CELL_DENSITY)] for j in range(CELL_DENSITY)]
game_is_running = False
game_is_stepping = False

def cellsInit():
    cells[CELL_DENSITY / 2 - 2][CELL_DENSITY / 2] = 1
    cells[CELL_DENSITY / 2 - 1][CELL_DENSITY / 2] = 1
    cells[CELL_DENSITY / 2    ][CELL_DENSITY / 2] = 1
    cells[CELL_DENSITY / 2 + 1][CELL_DENSITY / 2] = 1
    cells[CELL_DENSITY / 2 + 2][CELL_DENSITY / 2] = 1
    
    cells[CELL_DENSITY / 2][CELL_DENSITY / 2 - 2] = 1
    cells[CELL_DENSITY / 2][CELL_DENSITY / 2 - 1] = 1
    cells[CELL_DENSITY / 2][CELL_DENSITY / 2 + 1] = 1
    cells[CELL_DENSITY / 2][CELL_DENSITY / 2 + 2] = 1

def setup():
    size(CANVAS_WIDTH, CANVAS_WIDTH)
    stroke(0)
    cellsInit()

def drawGridLines():
    for i in range(1, CELL_DENSITY):
        separator = (CANVAS_WIDTH /CELL_DENSITY) * i
        line(separator, 0, separator, CANVAS_WIDTH)
        line(0, separator, CANVAS_WIDTH, separator)

def calcNeighbors(row, col):
    num_neighbors = 0
    for m in range(-1, 2):
        for n in range(-1, 2):
            if m == 0 and n == 0:
                continue
            if row + m < 0 or col + n < 0:
                continue
            if row + m >= CELL_DENSITY or col + n >= CELL_DENSITY:
                continue
            if cells[row+m][col+n] == 1:
                num_neighbors += 1
    return num_neighbors

def willLive(cell, num_neighbors):
    if num_neighbors == 3 or (cell == 1 and num_neighbors == 2):
        return 1
    return 0

def willLiveCool(cell, num_neighbors):
    if num_neighbors > 2 and num_neighbors <= 6 or (cell == 1 and num_neighbors == 2):
        return 1
    return 0

def willLiveLiquid(cell, num_neighbors):
    if num_neighbors > 3 and num_neighbors <= 8 or (cell == 1 and (num_neighbors == 2 or num_neighbors == 3)):
        return 1
    return 0

def drawCells():
    for i in range(0, CELL_DENSITY):
        for j in range(0, CELL_DENSITY):
            if cells[i][j] == 1:
                fill(50, 50, 50)
                rect(i * CELL_WIDTH, j * CELL_WIDTH, CELL_WIDTH, CELL_WIDTH)

def processGame():
    buffer_grid = copy.deepcopy(cells)
    for i in range(0, CELL_DENSITY):
        for j in range(0, CELL_DENSITY):
            buffer_grid[i][j] = willLiveCool(cells[i][j], calcNeighbors(i, j))
            if cells[i][j] == 1:
                fill(50, 50, 50)
                rect(i * CELL_WIDTH, j * CELL_WIDTH, CELL_WIDTH, CELL_WIDTH)

    return buffer_grid
    
def draw():
    global cells
    global game_is_running
    global game_is_stepping
    background(255, 255, 255)
    # drawGridLines()
    if not game_is_running and not game_is_stepping:
        drawCells()
    if game_is_running or game_is_stepping:
        buffer_grid = processGame()
        cells = copy.deepcopy(buffer_grid)
        game_is_stepping = False
    
def mouseClicked():
    x = mouseX / CELL_WIDTH
    y = mouseY / CELL_WIDTH
    cells[x][y] = 1 - cells[x][y]

def mouseDragged():
    x = mouseX / CELL_WIDTH
    y = mouseY / CELL_WIDTH
    if x < 0 or y < 0 or x >= CELL_DENSITY or y >= CELL_DENSITY:
        return
    cells[x][y] = 1
    
def keyPressed():
    global game_is_running
    global game_is_stepping
    if key == ' ':
        game_is_running = not game_is_running
    if keyCode == 10:
        game_is_stepping = True
    
    