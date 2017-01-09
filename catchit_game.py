# encoding: utf-8

import pygame
from pygame.locals import *
import sys
import fborx
# from __future__ import division

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_SIZE = [320, 400]
BAR_SIZE = [20, 5]
BALL_SIZE = [15, 15]

class Game(object):
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        # self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.screen = fborx.getScreen(*SCREEN_SIZE)
        pygame.display.set_caption('Simple Game')

        self.ball_pos_x = SCREEN_SIZE[0] // 2 - BALL_SIZE[0] / 2
        self.ball_pos_y = SCREEN_SIZE[1] // 2 - BALL_SIZE[1] / 2
        self.ball_dir_x = -1  # -1 left ; 1 right
        self.ball_dir_y = -1  # -1 up ; 1 down
        self.ball_pos = pygame.Rect(self.ball_pos_x, self.ball_pos_y, BALL_SIZE[0], BALL_SIZE[1])

        self.score = 0
        self.bar_pos_x = SCREEN_SIZE[0] // 2 - BAR_SIZE[0] // 2
        self.bar_pos = pygame.Rect(self.bar_pos_x, SCREEN_SIZE[1]-BAR_SIZE[1], BAR_SIZE[0], BAR_SIZE[1])

    def bar_move_left(self):
        self.bar_pos_x -= 2

    def bar_move_right(self):
        self.bar_pos_x += 2

    def run(self):
        pygame.mouse.set_visible(0)
        bar_move_left = False
        bar_move_right = False

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSE.BUTTONDOWN and event.button == 1:    # left click
                    bar_move_left = True
                elif event.type == pygame.MOUSE.BUTTONUP and event.button == 1:
                    bar_move_left = False
                elif event.type == pygame.MOUSE.BUTTONDOWN and event.button == 3:     # right click
                    bar_move_right = True
                elif event.type == pygame.MOUSE.BUTTONUP and event.button == 3:
                    bar_move_right = False

            if bar_move_left == True and bar_move_right == False:
                self.bar_move_left()
            if bar_move_left == False and bar_move_right == True:
                self.bar_move_right()

            self.screen.fill(BLACK)
            self.bar_pos.left = self.bar_pos_x
            pygame.draw.rect(self.screen, WHITE, self.bar_pos)

            self.ball_pos.left += self.ball_dir_x * 2
            self.ball_pos.bottom += self.ball_dir_y * 3
            pygame.draw.rect(self.screen, WHITE, self.ball_pos)

            if self.ball_pos.top <= 0 or self.ball_pos.bottom >= (SCREEN_SIZE[1] - BAR_SIZE[1] + 1):
                self.score += 1
                print("Score: ", self.score + '\r')
            elif self.bar_pos.top <= self.ball_pos.bottom and (self.bar_pos.left > self.ball_pos.right or self.bar_pos.right < self.ball_pos.left):
                print("Game Over: ", self.score)
                return self.score

            pygame.display.update()
            self.clock.tick(60)

if __name__  == '__main__':
    game = Game()
    game.run()
