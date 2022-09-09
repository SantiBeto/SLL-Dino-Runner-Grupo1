import pygame
import random
from components.cactus import Cactus
from utils.constants import LARGE_CACTUS, SMALL_CACTUS, DEFAULT_TYPE


class ObstacleManager():
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            #self.obstacles.append(Cactus(SMALL_CACTUS)) 
            #self.obstacles.append(Cactus(LARGE_CACTUS))
            self.obstacles.append(random.choice([Cactus(SMALL_CACTUS),Cactus(LARGE_CACTUS)]))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.dinosaur.dino_rect.colliderect(obstacle.rect):
                if not game.dinosaur_shield:
                    pygame.time.delay(300)
                    game.playing = False
                    game.crashed = True
                    game.points = 0
                else:
                    self.obstacles.remove(obstacle)
                    game.dinosaur.type = DEFAULT_TYPE
                    game.dinosaur_shield = False
    
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []