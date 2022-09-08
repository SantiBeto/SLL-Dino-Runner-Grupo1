import pygame
from unittest.mock import DEFAULT
from pygame.sprite import Sprite

from utils.constants import DEFAULT_TYPE, DUCKING, DUCKING_SHIELD, JUMPING, JUMPING_SHIELD, RUNNING, RUNNING_SHIELD, SHIELD_TYPE, SHIELD

class Dinosaur(Sprite):
    X_POS = 80
    Y_POS= 300
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5
    
    def __init__(self):
        self.duck_ing = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD}
        self.run_ing = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD}
        self.jump_ing = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD} 
        self.type = DEFAULT_TYPE
        self.image = self.run_ing[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
        self.step_index = 0

    def update(self, user_input):
       if self.dino_jump:
            self.jump()
       if self.dino_duck:
            self.duck()
       if self.dino_run:
            self.run()

       if user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False
       elif user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
       elif not self.dino_jump:
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False

       if self.step_index >= 10:
            self.step_index = 0

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x , self.dino_rect.y))

    def run(self):
        self.image = self.run_ing[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def duck(self):
        self.image = self.duck_ing[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def jump(self):
        self.image = self.jump_ing[self.type]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_rect.y = self.Y_POS
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL