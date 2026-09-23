from .helpers import *
from .sprites import LightBulbSprite

__all__ = ["Game"]


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.lightbulb_sprite = LightBulbSprite(
            (50, 50)
        )

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    cc()
                    sys.exit(0)

            self.lightbulb_sprite.draw()

            pygame.display.update()
