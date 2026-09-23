from ..helpers import *
from .sprite import Sprite

__all__ = ["LightBulbSprite"]


class LightBulbSprite(Sprite):
    def __init__(self, position: tuple[int, int], *group: pygame.sprite.Group) -> None:
        self.on_image_path = Path("src", "lumen", "assets", "lightbulb", "on.png")

        super().__init__(load_image(self.on_image_path), position, group)
