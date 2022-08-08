import os
import random

import pyautogui
import pygame
from pygame import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLUE = (0, 0, 255)
FPS = 60
PLAYER_WIDTH, PLAYER_HEIGHT = 155, 140
VEL = 5


class Game:

    def __init__(self) -> None:
        # os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.font.init()
        pygame.mixer.init()
        pygame.init()
        self.width, self.height = pyautogui.size()
        self.screen = pygame.display.set_mode([self.width - 40, self.height - 100])
        pygame.display.set_caption("Ciii Game!")
        self.icon = pygame.image.load('pics/ball_icon.png')
        pygame.display.set_icon(self.icon)

        self.BALL_SPEED_X = 5
        self.BALL_SPEED_Y = 4

        self.GOALS_FONT = pygame.font.SysFont('comicsans', 60)
        self.CII_FONT = pygame.font.SysFont('comicsans', 100)
        self.WINNER_FONT = pygame.font.SysFont('comicsans', 100)

        self.BORDER = pygame.Rect(self.width // 2 - 30, 0, 1, self.height)

        self.KICK_SOUND = pygame.mixer.Sound('./pics/kick.wav')
        self.GOAL_SOUND = pygame.mixer.Sound('./pics/SUIII.wav')

        HAL_IMAGE = pygame.image.load('./pics/hal.png')
        self.hal = pygame.transform.rotate(pygame.transform.scale(
            HAL_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), 0)

        VINI_IMAGE = pygame.image.load(os.path.join('./pics/vini.png'))
        self.vini = pygame.transform.rotate(pygame.transform.scale(
            VINI_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), 0)

        BALL_IMAGE = pygame.image.load(os.path.join('./pics/ball_icon.png'))
        self.ball = pygame.transform.rotate(pygame.transform.scale(
            BALL_IMAGE, (PLAYER_WIDTH / 4, PLAYER_HEIGHT / 4)), 0)

        self.bg = pygame.image.load("pics/pitch2.jpg")
        self.bg = pygame.transform.scale(self.bg, (self.width - 40, self.height - 100))

        self.hal_goals = 0
        self.vini_goals = 0

        self.FRAME_COUNT = 0
        self.START_TIME = 90
        self.FRAME_RATE = 60

        self.is_goal=False

    def draw_window(self, hal, vini, hal_goals, vini_goals, ball, goal_right, goal_left):
        self.screen.blit(self.bg, (0, 0))

        hal_text = self.GOALS_FONT.render("Goals: " + str(hal_goals), 1, BLACK)
        vini_text = self.GOALS_FONT.render("Goals: " + str(vini_goals), 1, BLACK)
        self.screen.blit(hal_text, (self.width - hal_text.get_width() - 180, 10))
        self.screen.blit(vini_text, (150, 10))

        self.screen.blit(self.hal, (hal.x, hal.y))
        self.screen.blit(self.vini, (vini.x, vini.y))
        self.screen.blit(self.ball, (ball.x, ball.y))
        pygame.draw.rect(self.screen,color=RED,rect=goal_right)
        pygame.draw.rect(self.screen,color=RED,rect=goal_left)
        total_sec=self.START_TIME-(self.FRAME_COUNT//self.FRAME_RATE)
        if total_sec<0:
            total_sec=0
        self.min=total_sec//60
        self.sec=total_sec%60
        output_time="Time left: {0:02}:{1:02}".format(self.min,self.sec)
        clock_text = self.GOALS_FONT.render(output_time, 1, BLACK)
        self.screen.blit(clock_text, (self.width/2 -250, 10))
        pygame.display.update()



    def restart_ball(self,ball):
        ball.y=(self.width / 2) - 40
        ball.x=(self.height / 2) - 60

    def celebrate_goal(self):
        self.GOAL_SOUND.play()
        cii_text = self.GOALS_FONT.render("Ciiiiii!!!", 1, BLACK)
        self.screen.blit(cii_text, (self.width / 2 - 200, 100))
        CR72 = pygame.image.load('./pics/cr72.png')
        self.ciir72 = pygame.transform.rotate(pygame.transform.scale(
            CR72, (PLAYER_WIDTH * 4, PLAYER_HEIGHT * 4)), 0)
        self.screen.blit(self.ciir72, (self.width / 2 - 350, 200))
        pygame.display.update()
        cii_text = self.GOALS_FONT.render("Ciiiiii!!!", 1, BLACK)
        self.screen.blit(cii_text, (self.width / 2 - 200, 100))
        CR7 = pygame.image.load('./pics/cr7.png')
        self.ciir7 = pygame.transform.rotate(pygame.transform.scale(
            CR7, (PLAYER_WIDTH * 4, PLAYER_HEIGHT * 4)), 0)
        self.screen.blit(self.ciir7, (self.width / 2 - 350, 200))
        pygame.display.update()


    def ball_moving(self, ball, vini, hal,goal_left, goal_right):
        ball.y += self.BALL_SPEED_Y
        ball.x += self.BALL_SPEED_X
        COLL_TOLL = 10
        COLL_TOLL_GOAL= 7

        if ball.colliderect(goal_left):
            if abs(goal_left.right - ball.left) < COLL_TOLL_GOAL:
                self.hal_goals+=1
                self.restart_ball(ball)
                self.is_goal=True
                # self.celebrate_goal()
                # pygame.display.update()




        if ball.colliderect(goal_right):
            if abs(goal_right.left - ball.right) < COLL_TOLL_GOAL:
                self.vini_goals+=1
                self.restart_ball(ball)
                self.is_goal=True


        if ball.right >= self.width -40 or ball.left <= 0:
            self.BALL_SPEED_X *= -1
        if ball.bottom >= self.height -80 or ball.top <= 0:
            self.BALL_SPEED_Y *= -1
        if ball.colliderect(vini):
            self.KICK_SOUND.play()
            if abs(vini.top - ball.bottom) < COLL_TOLL and self.BALL_SPEED_Y > 0:
                self.BALL_SPEED_Y *= -1
            if abs(vini.bottom - ball.top) < COLL_TOLL and self.BALL_SPEED_Y < 0:
                self.BALL_SPEED_Y *= -1
            if abs(vini.right - ball.left) < COLL_TOLL and self.BALL_SPEED_X < 0:
                self.BALL_SPEED_X *= -1
            if abs(vini.left - ball.right) < COLL_TOLL and self.BALL_SPEED_X > 0:
                self.BALL_SPEED_X *= -1
        if ball.colliderect(hal):
            self.KICK_SOUND.play()
            if abs(hal.top - ball.bottom) < COLL_TOLL and self.BALL_SPEED_Y > 0:
                self.BALL_SPEED_Y *= -1
            if abs(hal.bottom - ball.top) < COLL_TOLL and self.BALL_SPEED_Y < 0:
                self.BALL_SPEED_Y *= -1
            if abs(hal.right - ball.left) < COLL_TOLL and self.BALL_SPEED_X < 0:
                self.BALL_SPEED_X *= -1
            if abs(hal.left - ball.right) < COLL_TOLL and self.BALL_SPEED_X > 0:
                self.BALL_SPEED_X *= -1

    def vini_handle_movment(self, key_pressed, vini):
        if key_pressed[pygame.K_a] and vini.x - VEL > 0:  # left
            vini.x -= VEL
        if key_pressed[pygame.K_d] and vini.x + VEL + vini.width - 1 < self.BORDER.x + 22:  # right
            vini.x += VEL
        if key_pressed[pygame.K_w] and vini.y - VEL > 0:  # up
            vini.y -= VEL
        if key_pressed[pygame.K_s] and vini.y + VEL + vini.width < self.height:  # down
            vini.y += VEL

    def hal_handle_movment(self, key_pressed, hal):
        if key_pressed[pygame.K_LEFT] and hal.x - VEL > self.BORDER.x - 18:  # left
            hal.x -= VEL
        if key_pressed[pygame.K_RIGHT] and hal.x + VEL + hal.width - 10 < self.width:  # right
            hal.x += VEL
        if key_pressed[pygame.K_UP] and hal.y - VEL > 0:  # up
            hal.y -= VEL
        if key_pressed[pygame.K_DOWN] and hal.y + VEL + hal.width < self.height:  # down
            hal.y += VEL

    def draw_winner(self,text):
        WINNER_FONT = pygame.font.SysFont('comicsans', 100)
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        if text=="Tie":
            self.screen.blit(draw_text, (self.width / 2 - draw_text.get_width() / 2, self.height / 2 - draw_text.get_height() / 2))
        if text=="Halland":
            self.screen.blit(draw_text, (self.width/2 -200, 100))
            Gold_Ball = pygame.image.load('./pics/hal_win.png')
            self.gold = pygame.transform.rotate(pygame.transform.scale(
                Gold_Ball, (PLAYER_WIDTH*4, PLAYER_HEIGHT*4)), 0)
            self.screen.blit(self.gold,(self.width/2 -350, 200))
        if text=="Rodrygo":
            self.screen.blit(draw_text, (self.width/2 -200, 100))
            Gold_Ball = pygame.image.load('./pics/vin_win.png')
            self.gold = pygame.transform.rotate(pygame.transform.scale(
                Gold_Ball, (PLAYER_WIDTH*4, PLAYER_HEIGHT*4)), 0)
            self.screen.blit(self.gold,(self.width/2 -350, 200))
        pygame.display.update()
        pygame.time.delay(5000)

    def play(self):
        hal = pygame.Rect(1700, 390, PLAYER_WIDTH, PLAYER_HEIGHT)
        vini = pygame.Rect(60, 390, PLAYER_WIDTH, PLAYER_HEIGHT)
        ball = pygame.Rect((self.width / 2) - 40, (self.height / 2) - 60, PLAYER_WIDTH / 4, PLAYER_HEIGHT / 4)
        goal_right = pygame.Rect(1800,435, 5, PLAYER_HEIGHT / 1.25)
        goal_left = pygame.Rect(80, 435, 5, PLAYER_HEIGHT / 1.25)
        self.clock = pygame.time.Clock()
        run = True
        while run:
            self.FRAME_COUNT+=1
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.screen.fill((250, 250, 250))
            self.screen.blit(self.bg, (0, 0))

            key_pressed = pygame.key.get_pressed()
            self.vini_handle_movment(key_pressed, vini)
            self.hal_handle_movment(key_pressed, hal)
            self.ball_moving(ball, vini, hal,goal_left,goal_right)
            self.draw_window(hal, vini, self.hal_goals, self.vini_goals, ball,goal_right,goal_left)
            if self.is_goal==True:
                self.celebrate_goal()
                time.wait(2000)
                self.is_goal=False


            if self.min==0 and self.sec==0:
                winner_text=""
                if self.hal_goals>self.vini_goals:
                    winner_text="Halland"
                if self.vini_goals>self.hal_goals:
                    winner_text="Rodrygo"
                if self.hal_goals==self.vini_goals:
                    winner_text="Tie"
                self.draw_winner(winner_text)
                break

        pygame.quit()


x = Game()
x.play()
