import pygame
from components.dinosaur import Dinosaur
from components.obstacle_manager import ObstacleManager
from components.powerups.powerup_manager import PowerUpManager
from utils import text_utils

from utils.constants import BG, HALF_SCREEN_HEIGHT, HALF_SCREEN_WIDTH, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.crashed = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.dinosaur = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.powerup_manager = PowerUpManager()
        self.points = 0
        self.game_running = True
        self.dinosaur_shield = False

    def run(self):
        # Game loop: events - update - draw
        self.reset_components()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def reset_components(self):
        self.obstacle_manager.reset_obstacles()
        self.powerup_manager.reset_power_ups()
        self.points = 0

    def execute(self):
        while self.game_running:
            if not self.playing:
                self.show_menu()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.game_running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.dinosaur.update(user_input)
        self.obstacle_manager.update(self)
        self.powerup_manager.update(self)

        if self.dinosaur.shield_time_up < pygame.time.get_ticks():
            self.dinosaur.type = DEFAULT_TYPE
            self.dinosaur_shield = False

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.dinosaur.draw(self.screen)
        self.show_score()
        self.obstacle_manager.draw(self.screen)
        self.powerup_manager.draw(self.screen)
        pygame.display.update() 
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def show_score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1
        text, text_rect = text_utils.get_score_element(self.points)
        self.screen.blit(text, text_rect)

    def show_menu(self):
        self.game_running = True

        white_color = (255, 255, 255)
        self.screen.fill(white_color)

        self.show_options_menu()

        pygame.display.update()

        self.handle_key_events_menu()

    def show_options_menu(self):
        HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2
        HALF_SCREEN_WIDTH = SCREEN_WIDTH // 2

        text_to_show_1 = 'Press any Key to Start'
        text_to_show_2 = 'Do you want to try again? Press any key to restart'
        if not self.crashed:
            text_to_show = text_to_show_1
        else:
            text_to_show = text_to_show_2
        text, text_rect = text_utils.get_text_element(text_to_show, HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT)

        self.screen.blit(text, text_rect)

    def handle_key_events_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.game_running = False
                pygame.display.quit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                self.run()