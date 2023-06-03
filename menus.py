from setup import *


class Menu:
    title = pygame.font.SysFont("Arial", 30)
    subtitle = pygame.font.SysFont("Arial", 20)
    padding = 10

    def __init__(self, screen, title, subtitle, text_color=RED):
        self.bg = screen.copy()
        self.titleText = self.title.render(title, True, text_color)
        self.subtitleText = self.subtitle.render(subtitle, True, text_color)

    def update(self, delta):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return COMMAND_EXIT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return COMMAND_RESTART
        return COMMAND_NONE

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        titleRect = self.titleText.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        subtitleRect = self.subtitleText.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        boxRect = pygame.Rect(min(titleRect.x, subtitleRect.x) - self.padding,
                              min(titleRect.y, subtitleRect.y) - self.padding,
                              max(titleRect.width, subtitleRect.width) + self.padding * 2,
                              titleRect.height / 2 + subtitleRect.height / 2 + abs(
                                  titleRect.y - subtitleRect.y) + self.padding * 2)
        pygame.draw.rect(screen, BLACK, boxRect)
        pygame.draw.rect(screen, GRAY, boxRect, 4)
        screen.blit(self.titleText, titleRect)
        screen.blit(self.subtitleText, subtitleRect)


class Lose(Menu):

    def __init__(self, screen):
        super().__init__(screen, "You Lose!", "Press R to restart")


class Win(Menu):
    def __init__(self, screen):
        super().__init__(screen, "You Win!", "Press R to play again", GREEN)
