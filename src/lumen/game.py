from .groups import ObstacleGroup
from .helpers import *
from .sprites import BeamSprite, LightBulbSprite, MirrorSprite, ObstacleSprite

__all__ = ["Game"]


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.winner = False

        self.obstacles = ObstacleGroup()
        
        self.lightbulb_sprite = LightBulbSprite((100, 100), self.obstacles)

        self.beam_sprite = BeamSprite((WINDOW_WIDTH / 2, WINDOW_HEIGHT + 15), self.obstacles)

        self.font = pygame.font.Font(size = 50)
        self.font_text = self.font.render("You win!", True, color = "white")
        self.font_rect = self.font_text.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # Obstacles
        ObstacleSprite((200, 300), (500, 50), self.obstacles)
        ObstacleSprite((400, 600), (50, 300), self.obstacles)
        ObstacleSprite((800, 600), (500, 50), self.obstacles)
        ObstacleSprite((1300, 700), (100, 300), self.obstacles)

        # Mirrors
        MirrorSprite((1200, 700), 90, self.obstacles)
        MirrorSprite((525, 990), 90, self.obstacles)
        MirrorSprite((20, 700), 75, self.obstacles)
        MirrorSprite((300, 400), 50, self.obstacles)
        MirrorSprite((1400, 450), 90, self.obstacles)

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

            self.obstacles.draw()

            self.obstacles.update(dt)

            self.beam_sprite.draw()
            self.beam_sprite.update(dt)

            # Check for winner
            for sprite in self.obstacles.sprites():
                if isinstance(sprite, LightBulbSprite) and sprite.is_on:
                    self.winner = True

            if self.winner:
                self.screen.fill("black")
                self.screen.blit(self.font_text, self.font_rect)

            pygame.display.update()
