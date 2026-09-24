from .helpers import *
from .sprites import BeamSprite, LightBulbSprite

__all__ = ["Game"]


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.obstacles = pygame.sprite.Group()
        
        self.lightbulb_sprite = LightBulbSprite((100, 100), self.obstacles)

        self.beam_sprite = BeamSprite((WINDOW_WIDTH / 2, WINDOW_HEIGHT + 15), self.obstacles)

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                cc()
                sys.exit(0)

    def run(self) -> None:
        while True:
            self.screen.fill("Black")

            dt = self.clock.tick(60) / 1000

            events = pygame.event.get()

            self.handle_events(events)

            self.lightbulb_sprite.draw()
            self.beam_sprite.draw()

            self.lightbulb_sprite.update(dt)
            self.beam_sprite.update(dt)

            pygame.display.update()
