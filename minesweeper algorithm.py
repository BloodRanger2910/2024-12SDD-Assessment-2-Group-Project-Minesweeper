import random
rows,cols = 8,8
minefield = None
playerField = [[0 for _ in range(cols)] for _ in range(rows)]


def findNeighbours(row,col,totalRows,totalCols): #find all 9 neighbours around a cell
    neighbours = []

    if row > 0: #up
        neighbours.append((row-1,col))
    if row < (totalRows - 1): #down
        neighbours.append((row+1,col))
    if col > 0: #left
        neighbours.append((row, col - 1))
    if col < (totalCols-1): #right
        neighbours.append((row, col + 1))
    if row > 0 and col > 0: #top left
        neighbours.append((row-1,col-1))
    if row > 0 and col < (totalCols-1): #top right
        neighbours.append((row-1,col+1))
    if row < (totalRows-1) and col > 0: #bottom left
        neighbours.append((row+1,col-1))
    if row < (totalRows-1) and col < (totalCols-1): #bottom right
        neighbours.append((row+1,col+1))

    return neighbours

def generateGrid(rows,cols,mines):
    field = [[0 for _ in range(cols)] for _ in range(rows)]
    mine_positions = set()

    for mine in range(mines): #setting mine positions
        row = random.randint(0,rows-1)
        col = random.randint(0,cols-1)
        pos = (row,col)

        while pos in mine_positions:
            row = random.randint(0,rows-1)
            col = random.randint(0,cols-1)
            pos = (row,col)

        mine_positions.add(pos)
        field[row][col] = -1

def revealAllAdjacent(row,col): #meant to reveal all 8 squares around an empty square
    neighbours = findNeighbours(row,col,rows,cols) #find all neighbours

    for r,c in neighbours: #loop through
        try:
            if playerField[r][c] == 0:
                playerField[r][c] = 1 
                if minefield[r][c] == 0:
                    revealAllAdjacent(r,c) #recursive function 
        except:
            pass

def leftClick(row,col): #clicks square to reveal
    global gameOver
    global playerField

    if minefield[row][col] ==  -1: #stepped on a mine
        gameOver = True
    else:
        if minefield[row][col] > 0:
            playerField[row][col] = 1

        elif minefield[row][col] == 0:
            revealAllAdjacent(row,col)


minefield = [[0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,1,1,1,0,0],
             [0,0,0,1,-1,1,1,1],
             [1,1,1,1,1,1,0,0],
             [1,1,1,0,0,0,0,0],
             [-1,1,1,0,0,0,0,0],
             ]

leftClick(0,0)
for i in playerField:
    print(i)


