from ..helpers import *

__all__ = ["ObstacleGroup"]


class ObstacleGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()

        self.screen = pygame.display.get_surface()
    
    def draw(self) -> None:
        for sprite in self:
            sprite.draw()

    def update(self, dt: float) -> None:
        for sprite in self:
            sprite.update(dt)