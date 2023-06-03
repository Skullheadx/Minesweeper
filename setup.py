import pygame

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_h - 60, pygame.display.Info().current_h - 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Minesweeper")
pygame.display.set_icon(pygame.image.load("assets/bomb.png"))
clock = pygame.time.Clock()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BACKGROUND = (51, 28, 23)
BORDER = (187, 127, 87)

COMMAND_EXIT = 0
COMMAND_RESTART = 1
COMMAND_WIN = 2
COMMAND_LOSE = 3
COMMAND_NONE = 4
