import pygame
import random
import math
import os

mixer=pygame.mixer
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
menuHeight = 432
menuWidth = 800
refreshRate = 60
pause = False
mute = False
width = 0
height = 0
gameWon = False
display_highscore = False
time = 0
time_in_menu = 0
file_names = {'beginner':'beginner', 'intermediate':'intermediate', 'advanced': 'advanced', 'master':'master'}


highscoredata = []

screen = pygame.display.set_mode((menuWidth,menuHeight))

pygame.display.set_caption('Minesweeper')
rows,cols,mines = 0,0,0

#load sound assets
trapsong = pygame.mixer.Sound('sounds/videogame beat 1 for software minesweeper.mp3')
trapsong.set_volume(0.8)
trapsong.play(loops=-1)
grass_sfx = pygame.mixer.Sound('sounds/grass sfx.mp3')
grass_sfx.set_volume(3)
explosion_sfx = pygame.mixer.Sound('sounds/explosion sfx.mp3')
flag_sfx = pygame.mixer.Sound('sounds/flag sfx.mp3')


#loading image assets
button_img = pygame.image.load('images/start_btn.png').convert_alpha()
exit_img = pygame.image.load('images/exit_btn.png').convert_alpha()
resume_img = pygame.image.load('images/resume_btn.png').convert_alpha() #if not work, rename to resume_button
menu_img - pygame.image.load('image/menu_btn')
mine_img = pygame.image.load('images/landmine.png').convert_alpha()
clock_img = pygame.image.load('images/clock.png').convert_alpha()
flag_custom_img = pygame.image.load('images/flag_custom.png').convert_alpha()
darkgreen_tile = pygame.image.load('images/GRASS+1.png').convert_alpha()
lightgreen_tile = pygame.image.load('images/GRASS+2.png').convert_alpha()
floortile_dark = pygame.image.load('images/floortile_dark.png').convert_alpha()
floortile_light = pygame.image.load('images/floortile_light.png').convert_alpha()
soundbutton_img = pygame.image.load('images/soundbutton.jpg').convert_alpha()
minesweeper_text = pygame.image.load('images/minesweeper text logo.png').convert_alpha()
highScore_image = pygame.image.load('images/highscorebutton.png').convert_alpha()
highScore_frame = pygame.image.load('images/frame.png').convert_alpha()
close_img = pygame.image.load('images/close_button.png').convert_alpha()
sound_on_img = pygame.image.load('images/sound_on.png').convert_alpha()
sound_off_img = pygame.image.load('images/sound_off.png').convert_alpha()

difficultyButtons = {}
for x in file_names.values():
    asset = pygame.image.load(f'images/{x}_button.png').convert_alpha()
    difficultyButtons[x] = asset

scroll = 0

bg_images = [] #loading background image layers
for i in range(1,6):
    bg_image = pygame.image.load(f'images/plx-{i}.png').convert_alpha()
    bg_images.append(bg_image)
backgroundWidth = bg_images[0].get_width()
tiles = math.ceil(menuWidth/backgroundWidth) + 1

numbers = {} #loading numbers 
for i in range(1,9):
    numberPic = pygame.image.load(f'images/number {i}.png').convert_alpha()
    numbers[i] = numberPic

def drawLogo(): #draws the minesweeper logo on the starting screen
    logoImage = pygame.transform.scale(minesweeper_text, (minesweeper_text.get_width() *0.5, minesweeper_text.get_height()*0.5))
    screen.blit(logoImage, (100,30))
    
def displayHighScores():
    global file_names, display_highscore
    colors = {'beginner': (144,238,144), 'intermediate': (0,255,255), 'advanced': (255, 172, 28), 'master':(128, 0, 0)}

    frameImage = pygame.transform.scale(highScore_frame, (highScore_frame.get_width() *3, highScore_frame.get_height()*3))
    screen.blit(frameImage, (270,20))

    for n,scoreFile in enumerate(file_names.values()):
        with open(f'Highscores/highscore_{scoreFile}.txt', "r") as file:
            topScore = file.readline().strip()
            if topScore == '':
                topScore = '-'
            else:
                topScore += 's'

        labelText = font.render(scoreFile.capitalize(), True, colors[scoreFile])
        labelRect = labelText.get_rect()
        labelRect.center = (410,80+80*n)
        screen.blit(labelText, labelRect)

        scoreText = font.render(str(topScore), True, (0,0,0))
        scoreRect = scoreText.get_rect()
        scoreRect.center = (410,115+80*n)
        screen.blit(scoreText, scoreRect)

    closeButton = button(378,400, close_img, 1)

    if closeButton.draw():
        pygame.time.delay(30)
        display_highscore = False
        pygame.time.delay(30)


def drawBackground(): #draws background on starting screen and difficulty select screen
    for i in range(tiles):
        for layer in bg_images:
            screen.blit(layer, (i*backgroundWidth + scroll,0))
            

startGame = False #triggers with start button
loadDifficultySelect = False #to open difficulty select screen
loadGame = False #to setup game         
minefield = None #stores the minefield (-1 for mine), pre laced with mine counts
playerField = None #the field that the player sees, 0 for unrevealed, 1 for revealed, 2 for flagged
gameOver = False #triggers when player steps on a mine
game_over = False
font = pygame.font.Font('munro.ttf', 30) 
textRect = None 
flagsPlaced = 0
displayEndGame = False
firstClickDone = False


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:  # Adjusted comparison for descending order
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        
def save_highscore(time, highscore_file):
    # Check if the file exists
    highscores = []
    if not os.path.exists(highscore_file):
        with open(highscore_file, "w") as file:
            file.write(f"{time}\n")
        return

    # Read existing high scores
    with open(highscore_file, "r") as file:
        for score in file.readlines():
            if score.strip() != '':
                highscores.append(int(score.strip()))

    # Add the new score
    highscores.append(time)

    # Sort the high scores
    insertion_sort(highscores)

    # Keep only the top 5 scores
    highscores = highscores[:5]

    # Write the updated high scores to the file
    with open(highscore_file, "w") as file:
        for score in highscores:
            file.write(f"{score}\n")
            
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
        self.scaledRect.topleft = (x-(0.1*width*scale)/2, y - (0.1*height*scale)/2)

    def draw(self):
        action = False
        #get position of mouse
        pos = pygame.mouse.get_pos()

        #check if mouse is over button
        if self.rect.collidepoint(pos) == True:
            screen.blit(self.img_scaled, (self.scaledRect.x, self.scaledRect.y))

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                pygame.time.delay(100)
                self.clicked = True
                action = True
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))

        if pygame.mouse.get_pressed()[0] ==  0:
            self.clicked = False

        return action
    
class TestWinButton:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.clicked = False

    def draw(self):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
    
class square(): #dimensions of a square will be 30x30
    def __init__(self, x, y, image):
        self.imageAsset = image
        self.image = pygame.transform.scale(self.imageAsset, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        screen.blit(self.image, (self.rect.x,self.rect.y))

def recordHighScore():
    global time
    #compare if time is in top 5
    #if time is in top 5 -> insertion sort time into list -> remove after 4th index -> update persistence

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

def drawPause():
    global pause 
    global run
    surface = pygame.Surface((width, height), pygame.SRCALPHA) 
    pygame.draw.rect(surface, (128, 128, 128, 150), [0, 0, width, height])
    screen.blit(surface, (0,0))

    resumeButton = button(width/2 - resume_img.get_width()*1.25, height/2 - 20, resume_img, 2.5)
    if resumeButton.draw():
        pause = False

    menuButton = button(width/2 - menu_img.get_width()*1.25, height/2 + 60, menu_img, 2.5)
    if menuButton.draw():
        reset_game_stats()
        pause = False


def drawField(): #render the board
    global minefield
    global playerField

    for y, row in enumerate(playerField): #y is the number of squares deep (y-direction) the square is at
        for x, col in enumerate(row):  #x is the number of squares across (x-direction) the square is at
            y_cord = y*30
            x_cord = x*30 #determine the position of the square

            if y%2 == 0: #drawing the floor tiles
                if x%2 == 0:
                    floorTile  = square(x_cord, y_cord+100,floortile_dark)
                else:
                    floorTile = square(x_cord, y_cord+100,floortile_light)
            else:
                if x%2 != 0:
                    floorTile = square(x_cord, y_cord+100,floortile_dark)
                else:
                    floorTile = square(x_cord, y_cord+100,floortile_light)
            floorTile.draw()

            #drawing numbers ontop of floor tiles
            if minefield[y][x] > 0:
                num = square(x_cord, y_cord+100,numbers[minefield[y][x]])
                num.draw()

            if minefield[y][x] == -1: #if square is mined (move this to below green tiles later)
                y_cord = y*30
                x_cord = x*30
                mine = square(x_cord, y_cord+100,mine_img)
                mine.draw()

            if playerField[y][x] == 0  or playerField[y][x] == 2: #check if not revealed or flagged
                if y%2 == 0: #drawing the green tiles
                    if x%2 == 0:
                        box = square(x_cord, y_cord+100,darkgreen_tile)
                        
                    else:
                        box = square(x_cord, y_cord+100,lightgreen_tile)
                else:
                    if x%2 != 0:
                        box = square(x_cord, y_cord+100,darkgreen_tile)
                    else:
                        box = square(x_cord, y_cord+100,lightgreen_tile)
                box.draw()


            
            if playerField[y][x] == 2: #if square is flagged
                y_cord = y*30
                x_cord = x*30

                flag = square(x_cord, y_cord+100,flag_custom_img)
                flag.draw()

    pass
    #perhaps make it so that when player clicks, the box dissapears and reveals number below it?


def drawTopPanel():
    global clock_img
    global width
    global height
    global mute
    
    timeText = font.render(str(time), True, (0,0,0))
    textRect = timeText.get_rect()
    textRect.center = (width/10 + 40, 50)
    screen.blit(timeText, textRect)

    clock_img2 = pygame.transform.scale(clock_img, (int(clock_img.get_width()*0.20), int(clock_img.get_height()*0.20)))
    clockRect = clock_img2.get_rect()
    clockRect.center = (width/10 ,50)
    screen.blit(clock_img2, clockRect)

    flagsText = font.render(str(mines-flagsPlaced), True, (0,0,0))
    flagsTextRect = flagsText.get_rect()
    flagsTextRect.center = (width/10 + 100 ,50)
    screen.blit(flagsText,flagsTextRect)

    flagImg = pygame.transform.scale(flag_custom_img, (int(flag_custom_img.get_width()), int(flag_custom_img.get_height())))
    flagRect = flagImg.get_rect()
    flagRect.center = (width/10 + 70,50)
    screen.blit(flagImg, flagRect)

    if mute:
        soundButton = button((width/10)*9-30, 30, sound_off_img, 0.7)
    else:
        soundButton = button((width/10)*9-30, 30, sound_on_img, 0.7)

    if soundButton.draw():
        if mute == False:
            mute = True
            trapsong.set_volume(0)
            grass_sfx.set_volume(0)
            explosion_sfx.set_volume(0)
            flag_sfx.set_volume(0)
            pygame.time.delay(120)
        else:
            mute = False 
            trapsong.set_volume(0.8)
            grass_sfx.set_volume(3)
            explosion_sfx.set_volume(1)
            flag_sfx.set_volume(1)
            pygame.time.delay(120)


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
    
    while not firstClickDone and minefield[row][col] !=  0: #prevents mine from being stepped on first click
        minefield = generateGrid(rows, cols, mines)

    firstClickDone = True
        
    if minefield[row][col] <=  -1: #stepped on a mine
        gameOver = True
        print('mine!')
        gameOver = True
        loadGame = False
        explosion_sfx.play()
        revealGrid()

    else:
        if playerField[row][col] == 0:
            grass_sfx.play()


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
    flag_sfx.play()
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
    return

def checkWinCondition():
    global playerField, rows, cols, mines, gameWon, displayEndGame
    revealed_count = sum(row.count(1) for row in playerField)
    total_squares = rows * cols
    if revealed_count == total_squares - mines:
        gameWon = True
        displayEndGame = True
#checks if the amount of revealed squares are the same as the amount of non mine squares
        
def reset_game_stats():
    global menuHeight, menuWidth,width,height,gameWon,time,rows,cols,mines,startGame,loadDifficultySelect,loadGame, minefield,playerField,gameOver
    global flagsPlaced, displayEndGame, firstClickDone, screen
    
    menuHeight = 432
    menuWidth = 800
    screen = pygame.display.set_mode((menuWidth,menuHeight))
    width = 0
    height = 0
    gameWon = False
    time = 0
    rows,cols,mines = 0,0,0
    startGame = False #triggers with start button
    loadDifficultySelect = False #to open difficulty select screen
    loadGame = False #to setup game         
    minefield = None #stores the minefield (-1 for mine), pre laced with mine counts
    playerField = None #the field that the player sees, 0 for unrevealed, 1 for revealed, 2 for flagged
    gameOver = False #triggers when player steps on a mine
    flagsPlaced = 0
    displayEndGame = False
    firstClickDone = False
    print('reset!')
    pass


test_win_button = TestWinButton(50, 50, 200, 50, "Test Win")

#main game loop 
clock = pygame.time.Clock()
run = True
pygame.time.set_timer(pygame.USEREVENT, 1000) #initalise clock

reveal_all_button = button(0, 0, button_img, 1)

def drawMenu():
    global startGame, run, display_highscore,mute
    startButton = button(310, 140, button_img, 2.8)
    exitButton = button(319, 330, exit_img, 2.5)
    highScoreButton = button(317,230, highScore_image,2.6)
    if mute:
        soundButton = button(740, 385, sound_off_img, 0.8)
    else:
        soundButton = button(740, 385, sound_on_img, 0.8)

    drawBackground()
    drawLogo()

    if not display_highscore:
            if startButton.draw() == True: #check if clicked -> toggles game start and stops displaying start and exit buttons
                print('starting game')
                startGame = True
                pygame.time.delay(75)
            if exitButton.draw() == True:
                run = False

    if highScoreButton.draw() == True:
        print('high scores')
        display_highscore = True

    if display_highscore:
        displayHighScores()

    if soundButton.draw():
        if mute == False:
            mute = True
            trapsong.set_volume(0)
            grass_sfx.set_volume(0)
            explosion_sfx.set_volume(0)
            flag_sfx.set_volume(0)
            pygame.time.delay(120)
        else:
            mute = False 
            trapsong.set_volume(0.8)
            grass_sfx.set_volume(3)
            explosion_sfx.set_volume(1)
            flag_sfx.set_volume(1)
            pygame.time.delay(120)

def drawDifficultySelect():
    global difficulty, loadDifficultySelect, loadGame
    drawBackground()

    beginnerSelectButton = button(20,15, difficultyButtons['beginner'],1)
    if beginnerSelectButton.draw():
        difficulty = 'beginner'
        loadDifficultySelect = True
        loadGame = True
        setupGame(difficulty)
        pygame.time.delay(75)

    intermediateSelectButton = button(410,15, difficultyButtons['intermediate'],1)
    if intermediateSelectButton.draw():
        difficulty = 'intermediate'
        loadDifficultySelect = True
        loadGame = True
        setupGame(difficulty)
        pygame.time.delay(75)

    advancedSelectButton = button(20,220, difficultyButtons['advanced'],1)
    if advancedSelectButton.draw():
        difficulty = 'advanced'
        loadDifficultySelect = True
        loadGame = True
        setupGame(difficulty)
        pygame.time.delay(75)

    masterSelectButton = button(410,220, difficultyButtons['master'],1)
    if masterSelectButton.draw():
        difficulty = 'master'
        loadDifficultySelect = True
        loadGame = True
        setupGame(difficulty)
        pygame.time.delay(75)

    pass


while run:
    screen.fill((202,228,241))
    scroll -= 1
    if abs(scroll) > backgroundWidth:
        scroll = 0

    if startGame == False: #hides start button once start is clicked, put everything on menu here
        drawMenu()
        
    else:
        if loadDifficultySelect == False: 
            drawDifficultySelect()
            
        if loadGame: #commands for when game has been started
            drawField()
            drawTopPanel()

        if pause:
            drawPause()

        if gameOver and not displayEndGame: #clearing the field if player steps on a bomb
            drawTopPanel()
            drawField()
            #code to take the time and write to file
        
        if not gameWon and loadGame and not gameOver: #constantly checking if all squares have been revealed
            checkWinCondition()

        if gameWon and not displayEndGame: #if player wins
            save_highscore(time,f'Highscores/highscore_{file_names[difficulty]}')	
            displayEndGame = True
        
        if displayEndGame:
            drawTopPanel() 
            drawField() 

        if gameWon:
            # Render the win screen
                screen = pygame.display.set_mode((menuWidth, menuHeight))  # Set the mode to the menu size
                win_font = pygame.font.Font(None, 100)
                win_text = win_font.render("Congratulations!", True, (255, 255, 255))
                win_rect = win_text.get_rect(center=(menuWidth // 2, menuHeight // 2))
                screen.blit(win_text, win_rect)
                pygame.display.flip()  # Update the display
           
        if gameOver:
            # Render the lose screen
            screen = pygame.display.set_mode((menuWidth, menuHeight))  # Set the mode to the menu size
            #loss_font = pygame.font.Font(None, 100)
            #loss_text = loss_font.render("Game Over!", True, (255, 255, 255))
            #loss_rect = loss_text.get_rect(center=(menuWidth // 2, menuHeight // 2))
            #screen.blit(loss_text, loss_rect)
            #pygame.display.flip()  
            reset_game_stats() #reset game statistics
        
    
    for event in pygame.event.get():
        clock.tick(refreshRate)
        mouse = pygame.mouse.get_pressed()

        if event.type == pygame.USEREVENT and not gameOver and not gameWon and not pause:
            time += 1
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if pause:
                    pause = False
                else:
                    pause = True
                
        if loadGame == True and mouse[0] and not pause: #detect left click on grid
            mousePos = pygame.mouse.get_pos()
            row,col = getClickedCords(mousePos)
            if row > rows or cols > cols:
                continue
            leftClick(row,col)

        if loadGame == True and mouse[2] and not pause: #detect right click and place flag
            mousePos = pygame.mouse.get_pos()
            row,col = getClickedCords(mousePos)
            rightClick(row,col)
            pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        test_win_button.check_click(event)

    if test_win_button.clicked:
        gameWon = True
        displayEndGame = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False  # Exit the game loop and quit the game
                    break  # Exit the nested event loop as well
            if not run:
                break  # Exit the main event loop if run is False
    pygame.display.update()

#checking empty adjacent squares algorithm
#function to check all 8 adjacent squares from clicked square
#if any one of the 8 squares is empty, reveal all 8 sqaures around empty square
#recursive repeat for each square that was just revealed