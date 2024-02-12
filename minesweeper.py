import pygame
import random
import math

pygame.init()
menuHeight = 432
menuWidth = 800
refreshRate = 60

width = 0
height = 0

time = 0
time_in_menu = 0

screen = pygame.display.set_mode((menuWidth,menuHeight))
pygame.display.set_caption('Minesweeper')
rows,cols,mines = 0,0,0

#loading image assets
button_img = pygame.image.load('images/start_btn.png').convert_alpha()
exit_img = pygame.image.load('images/exit_btn.png').convert_alpha()
beginner_img = pygame.image.load('images/button_resume.png').convert_alpha()
square_img = pygame.image.load('images/square.png').convert_alpha()
mine_img = pygame.image.load('images/mine2.png').convert_alpha()
flag_img = pygame.image.load('images/flag.png').convert_alpha()
clock_img = pygame.image.load('images/clock.png').convert_alpha()
flag_custom_img = pygame.image.load('images/flag_custom.png').convert_alpha()
darkgreen_tile = pygame.image.load('images/darkgreen_tile.png').convert_alpha()
lightgreen_tile = pygame.image.load('images/lightgreen_tile.png').convert_alpha()

scroll = 0

bg_images = []
for i in range(1,6):
    bg_image = pygame.image.load(f'images/plx-{i}.png').convert_alpha()
    bg_images.append(bg_image)
backgroundWidth = bg_images[0].get_width()

tiles = math.ceil(menuWidth/backgroundWidth) + 1

def drawBackground():
    for i in range(tiles):
        for layer in bg_images:
            screen.blit(layer, (i*backgroundWidth + scroll,0))

startGame = False #triggers with start button
loadDifficultySelect = False #to open difficulty select screen
loadGame = False #to setup game         
minefield = None #stores the minefield (-1 for mine), pre laced with mine counts
playerField = None #the field that the player sees, 0 for unrevealed, 1 for revealed, 2 for flagged
gameOver = False #triggers when player steps on a mine
font = pygame.font.Font('munro.ttf', 30) 
textRect = None 
flagsPlaced = 0
displayEndGame = False
firstClickDone = False


class button(): #general button class
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.normalImage = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.center = (int(x+width/2), int(y+height/2))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        
        self.clicked = False
        self.img_scaled = pygame.transform.scale(image, (int(width * 1.1 * scale), int(height * 1.1 * scale)))

        self.scaledRect = self.img_scaled.get_rect()
        self.scaledRect.topleft = (x-(0.1*width)/2, y - (0.1*height)/2)


    def draw(self):
        action = False
        #get position of mouse
        pos = pygame.mouse.get_pos()

        #check if mouse is over button
        if self.rect.collidepoint(pos) == True:
            screen.blit(self.img_scaled, (self.scaledRect.x, self.scaledRect.y))

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))

        if pygame.mouse.get_pressed()[0] ==  0:
            self.clicked = False
            


        return action
    
class square(): #dimensions of a square will be 30x30
    def __init__(self, x, y, image):
        self.imageAsset = image
        self.image = pygame.transform.scale(self.imageAsset, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        screen.blit(self.image, (self.rect.x,self.rect.y))



startButton = button(310, 250, button_img, 1.5)
exitButton = button(310, 330, exit_img, 1.5)
beginnerButton = button(300, 200, beginner_img, 1)


#how big is the image in pixels
def setupGame(difficulty):  

    global rows
    global cols
    global mines

    if difficulty == 'beginner':
        rows,cols,mines = 8,8,10

    elif difficulty == 'intermediate':
        rows,cols,mines = 16,16,40

    elif difficulty == 'advanced':
        rows,cols,mines = 16,30,99
    
    elif difficulty == 'master':
        rows,cols,mines = 20,30,150
    
    global minefield
    global playerField
    global screen
    global time
    global time_in_menu
    global width
    global height

    minefield = generateGrid(rows, cols, mines)
    playerField = [[0 for _ in range(cols)] for _ in range(rows)]

    width = 30*cols
    height = 30*rows + 100

    screen = pygame.display.set_mode((width,height)) #resize the window to accompany the cells, extra space for side padding

    time_in_menu = time
    time = 0


def drawField(): #render the board
    global minefield
    global playerField

    for y, row in enumerate(playerField): #y is the number of squares deep (y-direction) the square is at
        for x, col in enumerate(row):  #x is the number of squares across (x-direction) the square is at
            if playerField[y][x] == 0  or playerField[y][x] == 2:
                y_cord = y*30
                x_cord = x*30
                if y%2 == 0:
                    if x%2 == 0:
                        box = square(x_cord, y_cord+100,darkgreen_tile)
                        box.draw()
                    else:
                        box = square(x_cord, y_cord+100,lightgreen_tile)
                else:
                    if x%2 != 0:
                        box = square(x_cord, y_cord+100,darkgreen_tile)
                    else:
                        box = square(x_cord, y_cord+100,lightgreen_tile)
                box.draw()

            if minefield[y][x] == -1:
                y_cord = y*30
                x_cord = x*30
                mine = square(x_cord, y_cord+100,mine_img)
                mine.draw()

            
            if playerField[y][x] == 2:
                y_cord = y*30
                x_cord = x*30

                flag = square(x_cord, y_cord+100,flag_custom_img)
                flag.draw()

            

    pass
    #perhaps make it so that when player clicks, the box dissapears and reveals number below it?

def drawTopPanel():
    global clock_img
    
    timeText = font.render(str(time), True, (0,0,0))
    textRect = timeText.get_rect()
    textRect.center = (100, 50)
    screen.blit(timeText, textRect)

    clock_img2 = pygame.transform.scale(clock_img, (int(clock_img.get_width()*0.20), int(clock_img.get_height()*0.20)))
    clockRect = clock_img2.get_rect()
    clockRect.center = (50,50)
    screen.blit(clock_img2, clockRect)

    flagsText = font.render(str(mines-flagsPlaced), True, (0,0,0))
    flagsTextRect = flagsText.get_rect()
    flagsTextRect.center = (200,50)
    screen.blit(flagsText,flagsTextRect)

    flagImg = pygame.transform.scale(flag_custom_img, (int(flag_custom_img.get_width()), int(flag_custom_img.get_height())))
    flagRect = flagImg.get_rect()
    flagRect.center = (150,50)
    screen.blit(flagImg, flagRect)



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

    for mine in mine_positions: #incrementing 1 to all neighbours of mines
        neighbours = findNeighbours(*mine, rows, cols)
        print(neighbours)
        for r,c, in neighbours:
            if field[r][c] != -1:
                field[r][c] += 1

    return field

def revealAllAdjacent(row,col): #meant to reveal all 8 squares around an empty square
    global rows
    global cols
    neighbours = findNeighbours(row,col,rows,cols) #find all neighbours

    playerField[row][col] = 1 #set square to be revealed

    for r,c in neighbours: #loop through
        if playerField[r][c] == 0:
            playerField[r][c] = 1 
            if minefield[r][c] == 0:
                revealAllAdjacent(r,c) #recursive function 

def leftClick(row,col): #clicks square to reveal
    global gameOver
    global playerField
    global loadGame
    global firstClickDone
    global minefield

    try:
        print('value', playerField[row][col])
    except:
        return
    
    if (row < 0 or col < 0) or playerField[row][col] == 2:
        return
    
    while not firstClickDone and minefield[row][col] <=  -1:
        minefield = generateGrid(rows, cols, mines)

    firstClickDone = True
        
    if minefield[row][col] <=  -1: #stepped on a mine
        gameOver = True
        print('mine!')
        gameOver = True
        loadGame = False

    else:
        if minefield[row][col] > 0: #clicked on a square that is adjacent to at least one mine
            playerField[row][col] = 1
            print('revealed',row,col)

        elif minefield[row][col] == 0: #clicked on empty square
            revealAllAdjacent(row,col)
            print('revealed',row,col)
            

def rightClick(row,col):
    global playerField
    global flagsPlaced

    try:
        print('flagged', row,col)
        playerField[row][col]
    except:
        return
    
    if row < 0 or col < 0:
        return
    
    if playerField[row][col] == 1: #flagged on an already revealed square
        return
    if playerField[row][col] == 2: #remove already placed flag
        playerField[row][col] = 0
        flagsPlaced -= 1
        return
    
    playerField[row][col] = 2
    flagsPlaced += 1

def getClickedCords(clickPos):
    global minefield
    global playerField
    global width
    global height

    x = clickPos[0]
    y = clickPos[1] - 100

    col = x//30
    row = y//30

    return (row,col)

def revealGrid():
    for r,row in enumerate(playerField):
        for c,col in enumerate(row):
            playerField[r][c] = 1
            drawField()
    return

#main game loop 
clock = pygame.time.Clock()
run = True
pygame.time.set_timer(pygame.USEREVENT, 1000) #initalise clock

while run:

    screen.fill((202,228,241))
    scroll -= 1
    if abs(scroll) > backgroundWidth:
        scroll = 0

    if startGame == False: #hides start button once start is clicked
        drawBackground()
        if startButton.draw() == True: #check if clicked -> toggles game start and stops displaying start and exit buttons
            print('starting game')
            startGame = True
            pygame.time.delay(75)
        if exitButton.draw() == True:
            run = False
    else:
        if loadDifficultySelect == False: 
            drawBackground()
            if beginnerButton.draw() == True:
                difficulty = 'advanced'
                loadDifficultySelect = True
                loadGame = True
                setupGame(difficulty) #initalises the board
                print(time_in_menu)
                pygame.time.delay(75)
            
        if loadGame: #commands for when game has been started
            drawField()
            drawTopPanel()

        if gameOver and not displayEndGame:
            drawTopPanel()
            revealGrid()
        
        if displayEndGame:
            drawTopPanel()  
        pass 

    
    for event in pygame.event.get():
        clock.tick(refreshRate)
        mouse = pygame.mouse.get_pressed()

        if event.type == pygame.USEREVENT and not gameOver:
            time += 1
        if event.type == pygame.QUIT:
            run = False 

        if loadGame == True and mouse[0]: #detect left click on grid
            mousePos = pygame.mouse.get_pos()
            row,col = getClickedCords(mousePos)
            if row > rows or cols > cols:
                continue
            leftClick(row,col)

        if loadGame == True and mouse[2]: #detect right click and place flag
            mousePos = pygame.mouse.get_pos()
            row,col = getClickedCords(mousePos)
            rightClick(row,col)
            pygame.time.delay(30)

    pygame.display.update()


#checking empty adjacent squares algorithm
#function to check all 8 adjacent squares from clicked square
#if any one of the 8 squares is empty, reveal all 8 sqaures around empty square
#recursive repeat for each square that was just revealed
