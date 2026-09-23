from .imports import Path, pygame

__all__ = ["load_image"]


def load_image(path: Path, convert_alpha: bool = True) -> pygame.Surface:
    image = pygame.image.load(path)

    if convert_alpha:
        image = image.convert_alpha()

    return image
