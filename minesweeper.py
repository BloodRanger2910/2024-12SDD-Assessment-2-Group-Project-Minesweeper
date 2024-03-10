import pygame
import random
import math
import os
import sys

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
display_credits = False
display_howto = False
time = 0
time_in_menu = 0
eula_agreement = False
file_names = {'beginner':'beginner', 'intermediate':'intermediate', 'advanced': 'advanced', 'master':'master'}
eula_clicked = False
no_of_clicks_eula = 0
events = []
colors = {'beginner': (144,238,144), 'intermediate': (0,255,255), 'advanced': (255, 172, 28), 'master':(128, 0, 0)}
revealRow = 0
revealCol = 0
gridRevealed = False

#load font
munro_font = pygame.font.Font("Font/munro.ttf", 36)

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
startbtn_img = pygame.image.load('images/start_btn.png').convert_alpha()
exitbtn_img = pygame.image.load('images/exit_btn.png').convert_alpha()
resumebtn_img = pygame.image.load('images/resume_btn.png').convert_alpha() #if not work, rename to resume_button
menu_img = pygame.image.load('images/menu_btn.png').convert_alpha()
mine_img = pygame.image.load('images/landmine.png').convert_alpha()
clock_img = pygame.image.load('images/clock.png').convert_alpha()
flag_custom_img = pygame.image.load('images/flag_custom.png').convert_alpha()
darkgreen_tile = pygame.image.load('images/GRASS+1.png').convert_alpha()
lightgreen_tile = pygame.image.load('images/GRASS+2.png').convert_alpha()
floortile_dark = pygame.image.load('images/floortile_dark.png').convert_alpha()
floortile_light = pygame.image.load('images/floortile_light.png').convert_alpha()
minesweeper_text = pygame.image.load('images/minesweeper text logo.png').convert_alpha()
highScore_image = pygame.image.load('images/highscorebutton.png').convert_alpha()
highScore_frame = pygame.image.load('images/frame.png').convert_alpha()
close_img = pygame.image.load('images/close_button.png').convert_alpha()
sound_on_img = pygame.image.load('images/sound_on.png').convert_alpha()
sound_off_img = pygame.image.load('images/sound_off.png').convert_alpha()
win_screen_img = pygame.image.load("images/SussyBaka.png").convert_alpha()
loss_screen_img = pygame.image.load("images/SussyBaka.png").convert_alpha()
panel_img = pygame.image.load("images/panel_bg.png").convert_alpha()
eula_img = pygame.image.load("images/eula.png").convert_alpha()
howtoplay_img = pygame.image.load("images/howto.png").convert_alpha()
resetbtn_img = pygame.image.load("images/reset_button.png").convert_alpha()
background_image = pygame.image.load("images/highscoreDisplay.png").convert_alpha()
playbtn_img = pygame.image.load("images/play_btn.png").convert_alpha()
howtoplaybtn_img = pygame.image.load("images/howtoplay.png").convert_alpha()
creditsbtn_img = pygame.image.load("images/creditsbtn.png").convert_alpha()
credits_img = pygame.image.load("images/credits.png").convert_alpha()

background_width, background_height = background_image.get_size()  # Get image dimensions
background_rect = background_image.get_rect(x=500, y=75) 
original_width, original_height = background_image.get_size()

# Double the size
new_width = original_width * 2
new_height = original_height * 2

# Scale the image to double size
scaled_background = pygame.transform.scale(background_image, (new_width, new_height)) 
screen.blit(scaled_background, background_rect)

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
    global file_names, display_highscore, colors

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

def displayCredits():
    global display_credits
    
    frameImage = pygame.transform.scale(credits_img, (credits_img.get_width() *1.6, credits_img.get_height()*1.6))
    screen.blit(frameImage, (100,20))
    
    closeButton = button(378,370, close_img, 1)
    
    if closeButton.draw():
        pygame.time.delay(30)
        display_credits = False
        pygame.time.delay(30)
        
def displayHowTo():
    global display_howto
    
    frameImage = pygame.transform.scale(howtoplay_img, (howtoplay_img.get_width() *1, howtoplay_img.get_height()*1))
    screen.blit(frameImage, (50,20))
    
    closeButton = button(378,340, close_img, 1)
    
    if closeButton.draw():
        pygame.time.delay(30)
        display_howto = False
        pygame.time.delay(30)    

def get_top_scores(difficulty):
    topScores = []
    with open(f'Highscores/highscore_{difficulty}.txt', "r") as file:
        for line in file:
            line = line.strip()
            if line !=  '':
                topScores.append(line)
    return topScores
    
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
font = pygame.font.Font('Font/munro.ttf', 30) 
textRect = None 
flagsPlaced = 0
displayEndGame = False
firstClickDone = False
loss_displayed = False
win_displayed = False
game_state = "playing"
ticks = 0


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
        global events

        #check if mouse is over button
        if self.rect.collidepoint(pos):
            screen.blit(self.img_scaled, (self.scaledRect.x, self.scaledRect.y))
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False and self.rect.collidepoint(pos):
                self.clicked = True
                action = True
                events = []
                return action

        
        if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        return action
    
def display_win_screen():
                    global difficulty, colors, difficulty_color, ticks, run, mute


                    duration = 40
                    scale = 250/duration
                    scale2 = 150/duration
                    scale3 = 200/duration
                    scale4 = 300/duration
                    scale5 = 300/duration
                    x_position = 575

                    topScores = get_top_scores(difficulty)
                    drawBackground()
                    # Display the win screen image
                    
                    screen.blit(win_screen_img, (0, 0))

                    difficulty_color = colors[difficulty]
                                        
                    if ticks < duration:
                        difficulty_text = munro_font.render("Difficulty: " + difficulty.capitalize(), True, difficulty_color)
                        win_text = munro_font.render("You Win!", True, (144, 238, 144))
                        time_text = munro_font.render("Time Taken: "+ str(time) +" seconds", True, (255, 255, 255))
                        screen.blit(difficulty_text, (300 - difficulty_text.get_width() // 2, 200 - scale*(duration - ticks)))
                        screen.blit(win_text, (300 - win_text.get_width() // 2, 100 - scale2*(duration - ticks)))
                        screen.blit(time_text, (300 - time_text.get_width() // 2, 150 - scale3*(duration - ticks)))
                        exitButton = button(100, 250 - scale4*(duration - ticks), exitbtn_img, 2.5)
                        reset_button = button(300, 250 - scale5*(duration - ticks), resetbtn_img, 2.5)

                        topScores_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                        alpha_value = 0
                        topScores_surface.fill((255, 255, 255, alpha_value))  # Create a surface to blit the scores
                        
                        for i, score in enumerate(topScores):
                            text_surface = munro_font.render(f'{score}s', True, (255, 212, 47))  # Render the text
                            topScores_surface.blit(text_surface, (0, i * 32 - scale * (duration - ticks)))  # Blit the text onto the surface
                            

                        y_position = 150 - scale * (duration - ticks)  # Adjust y_position based on ticks
                        background_rect = background_image.get_rect(x=500, y=75 - scale*(duration - ticks)) # Adjust 
                        ticks = ticks + 1

                    else:
                        # Display difficulty
                        difficulty_text = munro_font.render("Difficulty: " + difficulty.capitalize(), True, difficulty_color)
                        screen.blit(difficulty_text, (300 - difficulty_text.get_width() // 2, 200))
                        
                        #time taken
                        time_text = munro_font.render("Time Taken: "+ str(time) +" seconds", True, (255, 255, 255))
                        screen.blit(time_text, (300 - time_text.get_width() // 2, 150))
                        
                        #loss text
                        win_text = munro_font.render("You Win!", True, (144, 238, 144))
                        screen.blit(win_text, (300 - win_text.get_width() // 2, 100))
                       
                        #exit button
                        exitButton = button(100, 250, exitbtn_img, 2.5)

                        #reset button
                        reset_button = button(300, 250, resetbtn_img, 2.5)

                        #top score text
                        topScores_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                        alpha_value = 0
                        topScores_surface.fill((255, 255, 255, alpha_value))  # Create a surface to blit the scores
                        font = pygame.font.SysFont(None, 36)  # Choose a font and size
                        for i, score in enumerate(topScores):
                            text_surface = munro_font.render(score, True, (255, 212, 47))  # Render the text
                            topScores_surface.blit(text_surface, (0, i * 36))  # Blit the text onto the surface

                        y_position = 150
                        background_rect = background_image.get_rect(x=500, y=75)

                    screen.blit(background_image, background_rect)
                    # Blit the topScores_surface onto the background image at the desired position
                    screen.blit(topScores_surface, (x_position, y_position))

                    if reset_button.draw():
                        reset_game_stats()

                    
                    if exitButton.draw():
                        run = False

                    if mute:
                        soundButton = button(50, 50, sound_off_img, 0.7)
                    else:
                        soundButton = button(50,50, sound_on_img, 0.7)

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
                    

def display_loss_screen():
                    global difficulty, colors, difficulty_color ,ticks, run, mute
                    #print("You Lose!")
                    
                    duration = 40
                    scale = 250/duration
                    scale2 = 150/duration
                    scale4 = 300/duration
                    scale5 = 300/duration
                    x_position = 575
                     
                    topScores = get_top_scores(difficulty)
                    # Display the loss screen image
                    drawBackground()
                    screen.blit(loss_screen_img, (0, 0))

                    difficulty_color = colors[difficulty]
                    
                    if ticks < duration:
                        difficulty_text = munro_font.render("Difficulty: " + difficulty.capitalize(), True, difficulty_color)
                        loss_text = munro_font.render("You Lose!", True, (255, 0, 0))
                        screen.blit(difficulty_text, (300 - difficulty_text.get_width() // 2, 200 - scale*(duration - ticks)))
                        screen.blit(loss_text, (300 - loss_text.get_width() // 2, 100 - scale2*(duration - ticks)))
                        exitButton = button(100, 250 - scale4*(duration - ticks), exitbtn_img, 2.5)
                        reset_button = button(300, 250 - scale5*(duration - ticks), resetbtn_img, 2.5)

                        topScores_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                        alpha_value = 0
                        topScores_surface.fill((255, 255, 255, alpha_value))  # Create a surface to blit the scores
                        font = pygame.font.SysFont(None, 36)  # Choose a font and size
                        for i, score in enumerate(topScores):
                            text_surface = munro_font.render(f'{score}s', True, (255, 212, 47))  # Render the text
                            topScores_surface.blit(text_surface, (0, i * 25 - scale * (duration - ticks)))  # Blit the text onto the surface
                            

                        y_position = 150 - scale * (duration - ticks)  # Adjust y_position based on ticks
                        background_rect = background_image.get_rect(x=500, y=75 - scale*(duration - ticks)) # Adjust 
                        ticks = ticks + 1

                    else:
                        # Display difficulty
                        difficulty_text = munro_font.render("Difficulty: " + difficulty.capitalize(), True, difficulty_color)
                        screen.blit(difficulty_text, (300 - difficulty_text.get_width() // 2, 200))

                        #loss text
                        loss_text = munro_font.render("You Lose!", True, (255, 0, 0))
                        screen.blit(loss_text, (300 - loss_text.get_width() // 2, 100))

                        #exit button
                        exitButton = button(100, 250, exitbtn_img, 2.5)

                        #reset button
                        reset_button = button(300, 250, resetbtn_img, 2.5)

                        #top score text
                        topScores_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                        alpha_value = 0
                        topScores_surface.fill((255, 255, 255, alpha_value))  # Create a surface to blit the scores
                        font = pygame.font.SysFont(None, 36)  # Choose a font and size

                        for i, score in enumerate(topScores):
                            text_surface = munro_font.render(f'{score}s', True, (255, 212, 47))  # Render the text
                            topScores_surface.blit(text_surface, (0, i * 25))  # Blit the text onto the surface

                        y_position = 150
                        background_rect = background_image.get_rect(x=500, y=75)

                    screen.blit(background_image, background_rect)
                    # Blit the topScores_surface onto the background image at the desired position
                    screen.blit(topScores_surface, (x_position, y_position))

                    if reset_button.draw():
                        reset_game_stats()

                    
                    if exitButton.draw():
                        run = False

                    if mute:
                        soundButton = button(50,50, sound_off_img, 0.7)
                    else:
                        soundButton = button(50,50, sound_on_img, 0.7)

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
        self.x = x
        self.y = y

    def draw(self):
        pos = pygame.mouse.get_pos()
        screen.blit(self.image, (self.rect.x,self.rect.y))

        if self.rect.collidepoint(pos):
            surface = pygame.Surface((30, 30), pygame.SRCALPHA) 
            pygame.draw.rect(surface, (255, 255, 255, 100), [0, 0, 30, 30])
            screen.blit(surface, (self.x,self.y))

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

    resumeButton = button(width/2 - resumebtn_img.get_width()*1.25, height/2 - 20, resumebtn_img, 2.5)
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

def drawTopPanel():
    global clock_img
    global width
    global height
    global mute

    background = pygame.transform.scale(panel_img, (panel_img.get_width(), panel_img.get_height()))
    background_rect = background.get_rect()
    background_rect.topleft = (0,0)
    screen.blit(background,background_rect)

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

    if gameOver:
        smallfont = pygame.font.Font("Font/munro.ttf", 20)
        gameOverText = smallfont.render('Click anywhere to skip',False,(220,20,60))
        gameOverRect = gameOverText.get_rect()
        gameOverRect.center = (width/2,80)
        screen.blit(gameOverText,gameOverRect)
        print('a')
            

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
    global screen
    global events

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
        pygame.time.set_timer(pygame.USEREVENT, 250) 
        playerField[row][col] = 1
        explosion_sfx.play()
        events = []
        #screen = pygame.display.set_mode((menuWidth, menuHeight))

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
    global screen
    global playerField, rows, cols, mines, gameWon, displayEndGame
    revealed_count = sum(row.count(1) for row in playerField)
    total_squares = rows * cols
    if revealed_count == total_squares - mines:
        gameWon = True
        displayEndGame = True
        screen = pygame.display.set_mode((menuWidth, menuHeight))
        save_highscore(time,f'Highscores/highscore_{file_names[difficulty]}.txt')	

#checks if the amount of revealed squares are the same as the amount of non mine squares
        
def reset_game_stats():
    global menuHeight, menuWidth,width,height,gameWon,time,rows,cols,mines,startGame,loadDifficultySelect,loadGame, minefield,playerField,gameOver
    global flagsPlaced, displayEndGame, firstClickDone, screen, win_displayed, loss_displayed, game_state, ticks, revealCol,revealRow,gridRevealed
    
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
    loss_displayed = False
    win_displayed = False
    game_state = "playing"
    ticks = 0
    revealRow = 0
    revealCol = 0
    gridRevealed = False
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    print('reset!')

    pass

def drawEULA(): #work in progrss
    global eula_agreement
    global eula_clicked
    global no_of_clicks_eula


    surface = pygame.Surface((menuWidth, menuHeight), pygame.SRCALPHA) 
    pygame.draw.rect(surface, (128, 128, 128, 150), [0, 0, menuWidth, menuHeight])
    screen.blit(surface, (0,0))

    eula = pygame.transform.scale(eula_img, (eula_img.get_width(), eula_img.get_height()))
    eula_rect = eula.get_rect()
    eula_rect.center = (400,195)
    screen.blit(eula_img, eula_rect)

    exitBtn = button(335,300,playbtn_img,2)

    if exitBtn.draw() and no_of_clicks_eula < 1:
        pygame.time.wait(100)
        eula_agreement = True


test_win_button = TestWinButton(50, 50, 200, 50, "Test Win")

#main game loop 
clock = pygame.time.Clock()
run = True
pygame.time.set_timer(pygame.USEREVENT, 1000) #initalise clock

reveal_all_button = button(0, 0, startbtn_img, 1)

def drawMenu():
    global startGame, run, display_highscore, mute, display_credits, display_howto
    exitButton = button(345, 350, exitbtn_img, 2)
    startButton = button(230, 160, startbtn_img, 2.5)
    howToButton = button(230, 260 , howtoplaybtn_img, 2.5)
    highScoreButton = button(430, 160, highScore_image, 2.5)
    creditsButton = button(430, 260, creditsbtn_img, 2.5)


    if mute:
        soundButton = button(740, 385, sound_off_img, 0.8)
    else:
        soundButton = button(740, 385, sound_on_img, 0.8)

    drawBackground()
    drawLogo()

    if not display_highscore and not display_credits and not display_howto:
            if startButton.draw() == True: #check if clicked -> toggles game start and stops displaying start and exit buttons
                print('starting game')
                startGame = True
                pygame.time.delay(75)
            if exitButton.draw() == True:
                run = False

            if highScoreButton.draw() == True:
                print('high scores')
                display_highscore = True


            if creditsButton.draw() == True:
                print('credits')
                display_credits = True


            if howToButton.draw() == True:
                print("how to play")
                display_howto = True
    
    if display_howto:
        displayHowTo()

    if display_credits:
        displayCredits()

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
    clock.tick(refreshRate)
    screen.fill((202,228,241))
    scroll -= 1

    if abs(scroll) > backgroundWidth:
        scroll = 0
    
    if eula_agreement == False:
        drawBackground()
        drawEULA()

    if startGame == False and eula_agreement: #hides start button once start is clicked, put everything on menu here
        drawMenu()

    elif startGame: 
        if loadDifficultySelect == False:  
            drawDifficultySelect() 
             
        if loadGame: #commands for when game has been started 
            drawField() 
            drawTopPanel() 

        if pause and loadGame and not gameOver and not gameWon:
            drawPause()

        #if gameOver and not displayEndGame: #clearing the field if player steps on a bomb
        #    drawTopPanel()
        #    drawField()
            
        
        if not gameWon and loadGame and not gameOver: #constantly checking if all squares have been revealed
            checkWinCondition()

        #if gameWon or gameOver:
        #    revealGrid()
            
        if gameOver and not gridRevealed:
            drawField()
            drawTopPanel()

    if gameWon == True:
            display_win_screen()

    if gameOver and gridRevealed:
            display_loss_screen()
    
    clock.tick(refreshRate)
    events = pygame.event.get()
    
    for event in events:
        mouse = pygame.mouse.get_pressed()

        if event.type == pygame.USEREVENT and not gameOver and not gameWon and not pause:
            time += 1

        if event.type == pygame.USEREVENT and gameOver and not gridRevealed:

            try:
                while minefield[revealRow][revealCol] != -1:
                    revealCol += 1
                    if revealCol == cols:
                        revealRow += 1
                        revealCol = 0
                    if revealRow > rows-1:
                        gridRevealed = True
                        break
                if minefield[revealRow][revealCol] == -1:
                    playerField[revealRow][revealCol] = 1
                grass_sfx.play()
            except:
                pass
            print('clearing',revealRow,revealCol)

            revealCol += 1
            if revealCol == cols:
                revealRow += 1
                revealCol = 0

            if revealRow > rows-1:
                gridRevealed = True
                print('ahsdbaiydb')

            if gridRevealed:
                pygame.display.set_mode((menuWidth,menuHeight))

            pass

        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if pause:
                    pause = False
                else:
                    pause = True

        if gameOver and mouse[0] and not gridRevealed: #skips revealing grid if click
            gridRevealed = True
            pygame.display.set_mode((menuWidth,menuHeight))
                
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