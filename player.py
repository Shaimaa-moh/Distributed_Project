
import pygame
import sys


class Player():
    def __init__(self, x, y, car):  # creating player 1
        self.x = x
        self.y = y
        self.x_change = 0
        self.y_change = 0
        self.car_path = car

    def draw(self, screen):  # draw rectangle on screen
        car = pygame.image.load(self.car_path)
        screen.blit(car, (self.x, self.y))

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

                # checking if any key has been pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.x_change += 5

                if event.key == pygame.K_LEFT:
                    self.x_change -= 5

                if event.key == pygame.K_UP:
                    self.y_change -= 5

                if event.key == pygame.K_DOWN:
                    self.y_change += 5

                # checking if key has been lifted up
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.x_change = 0

                if event.key == pygame.K_LEFT:
                    self.x_change = 0

                if event.key == pygame.K_UP:
                    self.y_change = 0

                if event.key == pygame.K_DOWN:
                    self.y_change = 0

        # setting boundary for our main car
        if self.x < 178:
            self.x = 178
        if self.x > 490:
            self.x = 490

        if self.y < 0:
            self.y = 0
        if self.y > 495:
            self.y = 495

    def update(self):
        self.x += self.x_change
        self.y += self.y_change
  # responsible for updating positions in the window frame
 # update rectangle
