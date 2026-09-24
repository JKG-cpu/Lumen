from .helpers import *
from .sprites import LightBulbSprite

__all__ = ["Game"]


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.lightbulb_sprite = LightBulbSprite((100, 100))

    def run(self) -> None:
        while True:
            self.screen.fill("Black")

            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    cc()
                    sys.exit(0)

            self.lightbulb_sprite.draw()
            self.lightbulb_sprite.update(dt)

            pygame.display.update()
