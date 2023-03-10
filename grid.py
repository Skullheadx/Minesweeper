import random
from setup import *


class Grid:

	def __init__(self, length, height, bomb_count):
		self.length, self.height = length, height
		self.grid = [[Cell(j, i) for j in range(self.length)] for i in range(self.height)]

		self.bomb_count = bomb_count
		self.place_bombs(self.bomb_count)

		self.mouse_cooldown = 0

		for row in self.grid:
			for cell in row:
				neighbors = []
				for i in range(-1, 2):
					for j in range(-1, 2):
						x = int(cell.position.x // Cell.cell_size + i)
						y = int(cell.position.y // Cell.cell_size + j)
						if 0 <= y < self.height and 0 <= x < self.length and not (i == 0 and j == 0):
							neighbors.append(self.grid[y][x])
				cell.give_number(neighbors)

	def update(self, delta, mouse_pos, mouse_button):
		if self.mouse_cooldown > 0:
			self.mouse_cooldown -= delta
			return False

		for row in self.grid:
			for cell in row:
				if cell.position.x <= mouse_pos[0] <= cell.position.x + Cell.cell_size and cell.position.y <= mouse_pos[1] <= cell.position.y + Cell.cell_size:
					if mouse_button[0] == 1:
						self.mouse_cooldown = 0.2
						if cell.update(self.grid, self.height, self.length):
							return True
					elif mouse_button[2] == 1:
						if not cell.discovered:
							cell.flagged = not cell.flagged
							self.mouse_cooldown = 0.2
		return False

	def win(self):
		for row in self.grid:
			for cell in row:
				if not cell.is_bomb and not cell.discovered:
					return False
		return True

	def draw(self, screen):
		for row in self.grid:
			for cell in row:
				cell.draw(screen)

	def place_bombs(self, bomb_count):
		while bomb_count > 0:
			x = random.randint(0, self.length - 1)
			y = random.randint(0, self.height - 1)
			if not self.grid[y][x].is_bomb:
				self.grid[y][x].is_bomb = True
				bomb_count -= 1


class Cell:
	cell_size = 25
	font = pygame.font.SysFont("Arial", 20)

	def __init__(self, x, y):
		self.position = pygame.Vector2(x * self.cell_size, y * self.cell_size)
		self.is_bomb = False
		self.flagged = False
		self.number = 0
		self.discovered = False
		self.color = GRAY
		self.text = None

	def update(self, grid, height, length):
		if self.discovered or self.flagged:
			return False
		self.discovered = True
		self.color = GREEN
		if self.is_bomb:
			self.color = RED
			return True

		if self.number == 0:
			for i in range(-1, 2):
				for j in range(-1, 2):
					x = int(self.position.x // self.cell_size + i)
					y = int(self.position.y // self.cell_size + j)
					if 0 <= y < height and 0 <= x < length and not (i == 0 and j == 0):
						if not grid[y][x].discovered and not grid[y][x].flagged:
							grid[y][x].update(grid, height, length)

		return False

	def give_number(self, neighbors):
		if self.is_bomb:
			return
		for neighbor in neighbors:
			if neighbor.is_bomb:
				self.number += 1

		self.text = self.font.render(str(self.number), True, BLACK)

	def draw(self, screen):
		display_color = self.color
		if self.flagged:
			display_color = BLUE

		pygame.draw.rect(screen, display_color, (self.position.x, self.position.y, self.cell_size, self.cell_size))
		pygame.draw.rect(screen, BLACK, (self.position.x, self.position.y, self.cell_size, self.cell_size), 1)
		if self.discovered and self.number > 0:
			screen.blit(self.text, self.text.get_rect(
				center=(self.position.x + self.cell_size / 2, self.position.y + self.cell_size / 2)))
