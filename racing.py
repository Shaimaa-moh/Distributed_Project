from pygame.locals import*  # import all modules from Pygame
import time
import math
import random
import pygame
import sys
from player import Player

from network import Network
pygame.init()  # initializes the Pygame
screen = pygame.display.set_mode((798, 600))

# initializing pygame mixer
pygame.mixer.init()

# changing title of the game window
pygame.display.set_caption('Distributed Car Racing Project')
IntroFont = pygame.font.Font("freesansbold.ttf", 38)
username = ""
input_active = False
click = False
highscore = 0
score_value = 0


def introImg(x, y):
    intro = pygame.image.load("./images/intro.png")

    screen.blit(intro, (x, y))


def play(x, y):
    playtext = IntroFont.render("PLAY", True, (0, 0, 0))
    screen.blit(playtext, (x, y))


def introscreen():
    global username
    global input_active
    global click
    run = True
    pygame.mixer.music.load('./sounds/startingMusic.mp3')
    pygame.mixer.music.play()

    def handle_input_event(event):
        global username
        if event.key == pygame.K_RETURN:
            print("Username:", username)
        elif event.key == pygame.K_BACKSPACE:
            username = username[:-1]
        else:
            username += event.unicode
    while run:
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        # Clear the screen
        screen.fill(WHITE)
        introImg(0, 0)
        play(350, 450)
        ####### getting coordinates of mouse cursor #######
        x, y = pygame.mouse.get_pos()
        font = pygame.font.Font(None, 32)

        # storing rectangle coordinates (x, y, length, height) by making variables
        button1 = pygame.Rect(265, 440, 300, 50)
        # button2 = pygame.Rect(265, 440, 300, 50)
        # button3 = pygame.Rect(600, 440, 165, 50)
        # Render the label
        ##### Drawing rectangles with stored coorditates of rectangles.######
        ###### pygame.draw.rect takes these arguments (surface, color, coordinates, border) #####
        pygame.draw.rect(screen, (255, 255, 255), button1, 6)
        # pygame.draw.rect(screen, (255, 255, 255), button2, 6)
        # pygame.draw.rect(screen, (255, 255, 255), button3, 6)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                if input_rect.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    handle_input_event(event)
        # Render the username label
        label = font.render("Username:", True, BLACK)
        screen.blit(label, (285, 380))

        # Render the text input box
        input_rect = pygame.Rect(275, 400, 200, 30)
        pygame.draw.rect(screen, BLACK, input_rect, 2)

        # Render the text inside the input box
        input_text = font.render(username, True, BLACK)
        screen.blit(input_text, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.flip()

        pygame.display.update()

        # if our cursor is on button1 which is PLAY button
        if button1.collidepoint(x, y):
            # changing from inactive to active by changing the color from white to red
            pygame.draw.rect(screen, (0, 0, 0), button1, 6)
        #### if we click on the PLAY button ####
            if click and username != "":
                click = False
                gameloop()  # CALLING COUNTDOWN FUNCTION TO START OUR GAME

        # checking for mouse click event


def waiting():
    font2 = pygame.font.Font('freesansbold.ttf', 55)
    countdownBacground = pygame.image.load('./images/bg.png')
    waiting = font2.render('Waiting for Other Player', True, (255, 255, 0))
    screen.blit(countdownBacground, (0, 0))

    ###### Displaying waiting for oponents ######
    screen.blit(waiting, (100, 250))
    pygame.display.update()

  ###### Countdown ######


def countdown():
    font2 = pygame.font.Font('freesansbold.ttf', 85)
    countdownBacground = pygame.image.load('./images/bg.png')
    three = font2.render('3', True, (187, 30, 16))
    two = font2.render('2', True, (255, 255, 0))
    one = font2.render('1', True, (51, 165, 50))
    go = font2.render('GO!!!', True, (0, 255, 0))

    ##### displaying blank background #####
    screen.blit(countdownBacground, (0, 0))
    pygame.display.update()

    ###### Displaying  three (3) ######
    screen.blit(three, (350, 250))
    pygame.display.update()
    time.sleep(1)

    ##### displaying blank background #####
    screen.blit(countdownBacground, (0, 0))
    pygame.display.update()
    time.sleep(1)

    ###### Displaying  two (2) ######
    screen.blit(two, (350, 250))
    pygame.display.update()
    time.sleep(1)

    ##### displaying blank background #####
    screen.blit(countdownBacground, (0, 0))
    pygame.display.update()
    time.sleep(1)

    ###### Displaying  one (1) ######
    screen.blit(one, (350, 250))
    pygame.display.update()
    time.sleep(1)

    ##### displaying blank background #####
    screen.blit(countdownBacground, (0, 0))
    pygame.display.update()
    time.sleep(1)

    ###### Displaying  Go!!! ######
    screen.blit(go, (300, 250))
    pygame.display.update()
    # calling the gamloop so that our game can start after the countdown
    time.sleep(1)
    pygame.display.update()


def redrawScreen(screen, player, player2):
    player.draw(screen)
    player2.draw(screen)
    pygame.display.update()


# defining our gameloop function
def gameloop():
    global username
    global score_value
    global highscore
    ####### music #######
    pygame.mixer.music.load('./sounds/BackgroundMusic.mp3')
    pygame.mixer.music.play()
    ###### sound effect for collision ######
    crash_sound = pygame.mixer.Sound('./sounds/car_crash.wav')

    ####### scoring part ######

    font1 = pygame.font.Font("freesansbold.ttf", 25)

    def show_score(x, y, color):

        score = font1.render("SCORE: " + str(score_value), True, color)
        screen.blit(score, (x, y))

    def show_highscore(x, y, color):
        global highscore
        Hiscore_text = font1.render(
            'HIGHSCORE :' + str(highscore), True, color)
        screen.blit(Hiscore_text, (x, y))
        pygame.display.update()

    def victory():
        gameoverImg = pygame.image.load("./images/win.jpg")
        run = True
        while run:

            screen.blit(gameoverImg, (0, 0))
            time.sleep(0.5)
            show_score(330, 400, (0, 0, 0))
            time.sleep(0.5)
            show_highscore(330, 450, (0, 0, 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        introscreen()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    ###### creating our game over function #######

    def gameover():
        gameoverImg = pygame.image.load("./images/gameover.png")
        run = True
        while run:

            screen.blit(gameoverImg, (0, 0))
            time.sleep(0.5)
            show_score(330, 400, (255, 0, 0))
            time.sleep(0.5)
            show_highscore(330, 450, (255, 0, 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        introscreen()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    # setting background image
    bg = pygame.image.load('./images/bg.png')
    run = True
    n = Network()
    p = n.getP()
    p.draw(screen)
    # other cars

    car2 = pygame.image.load('./images/car2.png')
    car2X = random.randint(178, 490)
    car2Y = 100
    car2Ychange = 7

    car3 = pygame.image.load('./images/car3.png')
    car3X = random.randint(178, 490)
    car3Y = 100
    car3Ychange = 7

    clock = pygame.time.Clock()
    reply = n.send({"Player": p, "Crashed": False,
                   "Username": username, "score": score_value, "Game": "start", })
    highscore = reply["Highscore"]
    print("Reply:", reply)
    waiting()
    while reply["Connections"] < 2:
        reply = n.send({"Player": p, "Crashed": False,
                       "Username": username, "score": score_value, "Game": "Playing", })

    countdown()
    while run:

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

                # checking if any key has been pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    p.x_change += 5

                if event.key == pygame.K_LEFT:
                    p.x_change -= 5

                if event.key == pygame.K_UP:
                    p.y_change -= 5

                if event.key == pygame.K_DOWN:
                    p.y_change += 5

                # checking if key has been lifted up
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    p.x_change = 0

                if event.key == pygame.K_LEFT:
                    p.x_change = 0

                if event.key == pygame.K_UP:
                    p.y_change = 0

                if event.key == pygame.K_DOWN:
                    p.y_change = 0

        if p.x < 178:
            p.x = 178
        if p.x > 490:
            p.x = 490

        if p.y < 0:
            p.y = 0
        if p.y > 495:
            p.y = 495
        reply = n.send({"Player": p, "Crashed": False,
                       "Username": username, "score": score_value, "Game": "Playing", })

        # CHANGING COLOR WITH RGB VALUE, RGB = RED, GREEN, BLUE
        screen.fill((0, 0, 0))

        # displaying the background image
        screen.blit(bg, (0, 0))

        # displaying our main cars
        redrawScreen(screen, p, reply["Oponent"])

        screen.blit(car2, (car2X, car2Y))
        screen.blit(car3, (car3X, car3Y))
        # calling our show_score function
        show_score(570, 280, (255, 0, 0))
        # calling show_hiscore function
        show_highscore(0, 0, (255, 0, 0))

        p.x += p.x_change
        p.y += p.y_change

        # movement of the enemies

        car2Y += car2Ychange
        car3Y += car3Ychange

        if car2Y > 670:
            car2Y = -150
            car2X = reply["car1"]
            score_value += 1
        if car3Y > 670:
            car3Y = -200
            car3X = reply["car2"]
            score_value += 1

        # checking if highscore has been created
        if score_value > int(highscore):
            highscore = score_value

        # DETECTING COLLISIONS BETWEEN THE CARS

        # getting distance between our main car and car2

        def iscollision(car2X, car2Y, player):
            distance = math.sqrt(
                math.pow(car2X-player.x, 2) + math.pow(car2Y - player.y, 2))

            # checking if distance is smaller than 50 after then collision will occur
            if distance < 50:
                return True
            else:
                return False

        # getting distance between our main car and car3
        def iscollision(car3X, car3Y, player):
            distance = math.sqrt(
                math.pow(car3X-player.x, 2) + math.pow(car3Y - player.y, 2))

            # checking if distance is smaller then 50 after then collision will occur
            if distance < 50:
                return True
            else:
                return False

        ##### giving collision a variable #####

        # collision between maincar and car2
        coll2 = iscollision(car2X, car2Y, p)

        # collision between maincar and car3
        coll3 = iscollision(car3X, car3Y, p)

        # if coll2 occur
        if coll2:

            car2Ychange = 0
            car3Ychange = 0
            car2Y = 0
            car3Y = 0
            p.x_change = 0
            p.y_change = 0
            pygame.mixer.music.stop()
            crash_sound.play()
        ###### calling our game over function #######
            run = False
            reply = n.send(
                {"Player": p, "Crashed": True, "Username": username, "score": score_value, "Game": "Playing", })
            try:
                while reply["End_Game"] == False:
                    reply = n.send(
                        {"Player": p, "Crashed": True, "Username": username, "score": score_value, "Game": "Playing", })
            except:
                gameover()
            if reply["Victory"] == True:
                highscore = reply["Highscore"]
                victory()
            else:
                highscore = reply["Highscore"]
                gameover()

        # if coll3 occur
        if coll3:

            car2Ychange = 0
            car3Ychange = 0
            car2Y = 0
            car3Y = 0
            p.x_change = 0
            p.y_change = 0
            pygame.mixer.music.stop()
            crash_sound.play()
        ###### calling our game over function #######
            run = False
            reply = n.send(
                {"Player": p, "Crashed": True, "Username": username, "score": score_value, "Game": "Playing", })
            try:
                while reply["End_Game"] == False:
                    reply = n.send(
                        {"Player": p, "Crashed": True, "Username": username, "score": score_value, "Game": "Playing", })
            except:
                gameover()
            if reply["Victory"] == True:
                highscore = reply["Highscore"]
                victory()
            else:
                highscore = reply["Highscore"]
                gameover()

        if car2Ychange == 0 and car3Ychange == 0:
            pass

        pygame.display.update()


introscreen()
