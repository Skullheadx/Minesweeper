import random
from setup import *


class Grid:

    def __init__(self, length, height, bomb_count):
        self.length, self.height = length, height
        self.position = pygame.Vector2(SCREEN_WIDTH / 2 - Cell.cell_size * self.length / 2,
                                       SCREEN_HEIGHT / 2 - Cell.cell_size * self.height / 2)
        self.grid = [[Cell(self.position.x, self.position.y, j, i) for j in range(self.length)] for i in
                     range(self.height)]

        self.bomb_count = bomb_count
        self.place_bombs(self.bomb_count)

        self.mouse_cooldown = 0

        self.bombs = []

        for row in self.grid:
            for cell in row:
                neighbors = []
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        x = int(cell.grid_position.x + j)
                        y = int(cell.grid_position.y + i)
                        if 0 <= y < self.height and 0 <= x < self.length and not (i == 0 and j == 0):
                            neighbors.append(self.grid[y][x])
                cell.give_number(neighbors)
                if cell.is_bomb:
                    self.bombs.append(cell)

    def update(self, delta, mouse_pos, mouse_button):
        if self.mouse_cooldown > 0:
            self.mouse_cooldown -= delta
            return False

        for row in self.grid:
            for cell in row:
                if cell.position.x <= mouse_pos[0] <= cell.position.x + Cell.cell_size and cell.position.y <= mouse_pos[
                    1] <= cell.position.y + Cell.cell_size:
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
        pygame.draw.rect(screen, BACKGROUND, (
            self.position.x - 2, self.position.y - 2, self.length * Cell.cell_size + 4,
            self.height * Cell.cell_size + 4))
        pygame.draw.rect(screen, BORDER, (
            self.position.x - 2, self.position.y - 2, self.length * Cell.cell_size + 4,
            self.height * Cell.cell_size + 4),
                         2)
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
    numbers = {
        0: pygame.transform.scale(pygame.image.load("assets/empty.png"), (cell_size, cell_size)),
        1: pygame.transform.scale(pygame.image.load("assets/1.png"), (cell_size, cell_size)),
        2: pygame.transform.scale(pygame.image.load("assets/2.png"), (cell_size, cell_size)),
        3: pygame.transform.scale(pygame.image.load("assets/3.png"), (cell_size, cell_size)),
        4: pygame.transform.scale(pygame.image.load("assets/4.png"), (cell_size, cell_size)),
        5: pygame.transform.scale(pygame.image.load("assets/5.png"), (cell_size, cell_size)),
        6: pygame.transform.scale(pygame.image.load("assets/6.png"), (cell_size, cell_size)),
        7: pygame.transform.scale(pygame.image.load("assets/7.png"), (cell_size, cell_size)),
        8: pygame.transform.scale(pygame.image.load("assets/8.png"), (cell_size, cell_size)),
    }

    flag = pygame.transform.scale(pygame.image.load("assets/flag.png"), (cell_size, cell_size))
    undiscovered = pygame.transform.scale(pygame.image.load("assets/undiscovered.png"), (cell_size, cell_size))
    explosion = pygame.transform.scale(pygame.image.load("assets/explosion.png"), (cell_size, cell_size))
    undiscovered_bomb = pygame.transform.scale(pygame.image.load("assets/undiscovered_bomb.png"),
                                               (cell_size, cell_size))

    def __init__(self, pos_x, pos_y, x, y):
        self.position = pygame.Vector2(pos_x + x * self.cell_size, pos_y + y * self.cell_size)
        self.grid_position = pygame.Vector2(x, y)
        self.is_bomb = False
        self.flagged = False
        self.number = 0
        self.discovered = False
        self.revealed = False

    def update(self, grid, height, length):
        if self.discovered or self.flagged:
            return False
        self.discovered = True
        if self.is_bomb:
            return True

        if self.number == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    x = int(self.grid_position.x + i)
                    y = int(self.grid_position.y + j)
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

    def reveal(self):
        if not self.discovered:
            self.revealed = True

    def draw(self, screen):
        if self.revealed:
            screen.blit(self.undiscovered_bomb, self.position)
        elif self.discovered:
            if self.is_bomb:
                screen.blit(self.explosion, self.position)
            else:
                screen.blit(self.numbers[self.number], self.position)
        else:
            screen.blit(self.undiscovered, self.position)
        if self.flagged:
            screen.blit(self.flag, self.position)
