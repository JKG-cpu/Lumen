from ..helpers import *

__all__ = ["ObstacleSprite"]


class ObstacleSprite(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], size: tuple[int, int], *groups: pygame.sprite.Group) -> None:
        super().__init__(*groups)
        self.screen = pygame.display.get_surface()

        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill("grey")

        self.rect = self.image.get_frect(center = position)

        self.hitbox = self.rect.copy()
        self.beam_behavior = "wall"

    def draw(self) -> None:
        self.screen.blit(self.image, self.rect)