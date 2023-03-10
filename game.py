import pygame.event

from setup import *
from grid import Grid


class Game:

	def __init__(self):
		self.grid = Grid(20, 20, 50)

		self.game_over = False

	def update(self, delta):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return COMMAND_EXIT

		mouse_pos = pygame.mouse.get_pos()
		mouse_button = pygame.mouse.get_pressed()
		if self.grid.update(delta, mouse_pos, mouse_button):
			return COMMAND_LOSE
		if self.grid.win():
			return COMMAND_WIN

		return COMMAND_NONE

	def draw(self, screen):
		screen.fill(BLACK)
		self.grid.draw(screen)