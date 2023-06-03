from setup import *
from grid import Grid


class Game:

    def __init__(self):
        self.grid = Grid(25, 25, 100)
        self.game_over = False

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return COMMAND_EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return COMMAND_RESTART

        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed()
        if self.grid.update(delta, mouse_pos, mouse_button):
            for bomb in self.grid.bombs:
                bomb.reveal()
            return COMMAND_LOSE
        if self.grid.win():
            return COMMAND_WIN

        return COMMAND_NONE

    def draw(self, screen):
        screen.fill(BLACK)
        self.grid.draw(screen)
