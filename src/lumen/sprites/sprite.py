from ..helpers import *

__all__ = ["Sprite"]


class Sprite(pygame.sprite.Sprite):
    def __init__(
        self,
        image: pygame.Surface,
        position: tuple[int, int],
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(groups)
        self.screen = pygame.display.get_surface()

        self.image = image
        self.rect = self.image.get_frect(center=position)

    def draw(self) -> None:
        self.screen.blit(self.image, self.rect)

    def update(self) -> None:
        self.draw()
