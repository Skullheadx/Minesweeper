from setup import *
from game import Game
from menus import Lose, Win


def main():
    scene = Game()
    is_running = True
    while is_running:
        delta = clock.tick(60) / 1000

        status = scene.update(delta)
        scene.draw(screen)
        pygame.display.update()

        if status == COMMAND_EXIT:
            is_running = False
        elif status == COMMAND_RESTART:
            scene = Game()
        elif status == COMMAND_WIN:
            scene = Win(screen)
        elif status == COMMAND_LOSE:
            scene = Lose(screen)


if __name__ == "__main__":
    main()
