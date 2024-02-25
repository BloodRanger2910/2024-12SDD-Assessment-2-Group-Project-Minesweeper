import pygame

pygame.init()

display_width = 800
display_height = 600

white = (255,255,255)
black = (0,0,0)
red = (175,0,0)
green = (34,177,76)
yellow = (175,175,0)
blue = (30,144,255)
light_green = (0,255,0)
light_red = (255,0,0)
light_yellow = (255,255,0)
light_blue = (0,191,255)

smallFont = pygame.font.SysFont("Comicsansms", 20)
medFont = pygame.font.SysFont("Comicsansms", 45)
largeFont = pygame.font.SysFont("Comicsansms", 55)



gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Typing Game")


def text_objects(text, color, size):
    if size == "small":
        textSurf = smallFont.render(text, True, color)
    elif size == "medium":
        textSurf = medFont.render(text, True, color)
    elif size == "large":
        textSurf = largeFont.render(text, True, color)

    return textSurf, textSurf.get_rect()


def messageToScreen(msg, color, y_displace = 0, size = "small"):
    textSurface, textRect = text_objects(msg, color, size)
    textRect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurface, textRect)

def text_to_button(msg, color, buttonX, buttonY, buttonWidth, buttonHeight, size = "small"):
    textSurface, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonX + (buttonWidth/2), buttonY + (buttonHeight/2)))
    gameDisplay.blit(textSurface, textRect)


def button(text, x, y, width, height, inactiveColor , activeColor,textColor = black, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+ width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, activeColor, (x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "directions":
                gameDisplay.fill(white)
                pygame.display.update()
                directions()
            if action == "lvl":
                gameDisplay.fill(white)
                pygame.display.update()
                levelScreen()
            if action == "clear":
                gameDisplay.fill(white)
                pygame.display.update()
                clearData()
            if action == "main":
                gameDisplay.fill(white)
                pygame.display.update()
                startScreen()
            if action == "page2":
                gameDisplay.fill(white)
                pygame.display.update()
                page2()
            if action == "page3":
                gameDisplay.fill(white)
                pygame.display.update()
                page3()


    else:
        pygame.draw.rect(gameDisplay, inactiveColor, (x,y,width,height))

    text_to_button(text,textColor,x,y,width,height)

def clearData():
    pass

def levelScreen():
    level = True

    while level:
        global levelnumber
        levelnumber = 1 
        gameDisplay.fill(white)
        messageToScreen("Level Select", green, -200, size = "large")
        button("Back",150, 500,150,50, light_yellow, yellow, action = "main")
        button("Quit",350,500,150,50,light_red,red,action = "quit")
        button("Next",550,500,150,50,light_yellow,yellow,action = "page2")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level = False
                pygame.quit()
                quit()

def page2():
    level = True
    print("page2")
    while level:
        gameDisplay.fill(white)
        messageToScreen("Level Select", green, -200, size = "large")
        button("Previous",150, 500,150,50, light_yellow, yellow, action = "lvl")
        button("Quit",350,500,150,50,light_red,red,action = "quit")
        button("Next",550,500,150,50,light_yellow,yellow,action = "page3")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level = False
                pygame.quit()
                quit()

def page3():
    level = True
    print("page3")

    while level: 
        gameDisplay.fill(white)
        messageToScreen("Level Select 2", green, -200, size = "large")
        button("Previous",150, 500,150,50, light_yellow, yellow, action = "lvl")
        button("Quit",350,500,150,50,light_red,red,action = "quit")
        button("Next",550,500,150,50,light_yellow,yellow,action = "main")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level = False
                pygame.quit()
                quit()


def directions():
    directions = True

    while directions:

        gameDisplay.fill(white)
        messageToScreen("Directions", green, -200, size = "large")
        messageToScreen("Click The Buttons To Navigate",black,-100)
        messageToScreen("Select Level Buttons To Start The Level",black,-60)
        messageToScreen("Complete A Level By Typing All The Words In The Level",black,-20)
        messageToScreen("Each Level Is Timed And Gets Harder And Harder",black,20)
        messageToScreen("Have Fun!!!",blue,80, size = "medium")
        button("Back",150, 500,150,50, light_yellow, yellow, action = "main")
        button("Quit",550,500,150,50,light_red,red,action = "quit")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                directions = False
                pygame.quit()
                quit()



def startScreen():

    game = True
    while game:
        gameDisplay.fill(white)


        messageToScreen("Welcome To The Typing Game", green, -100, size = "large")
        button("Lvl Select",150, 300,150,50, light_green, green, action = "lvl")
        button("Directions",350, 300,150,50, light_yellow, yellow, action = "directions")
        button("Quit Game",550, 300,150,50, light_red, red, action = "quit")
        button("Clear Data", 350, 400,150,50, light_blue, blue, action = "clear")


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                pygame.quit()
                quit()
startScreen()
