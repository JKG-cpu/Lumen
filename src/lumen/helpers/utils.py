from .imports import Path, pygame

__all__ = ["load_sprite", "load_sprites"]


def load_sprite(path: Path, convert_alpha: bool = True, scale: tuple[int, int] = (1, 1)) -> pygame.Surface:
    image = pygame.image.load(path)

    if convert_alpha:
        image = image.convert_alpha()

    return pygame.transform.scale(image, (image.get_width() * scale[0], image.get_height() * scale[1]))

def load_sprites(path: Path, sprite_width: int, sprite_height: int, total_sprites: int, convert_alpha: bool = True, scale: tuple[int, int] = (1, 1)) -> list[pygame.Surface]:
    sheet = load_sprite(path, convert_alpha, scale)
    sprite_width *= scale[0]
    sprite_height *= scale[1]
    sprites = []

    for i in range(total_sprites):
        x = i * sprite_width
        y = 0

        rect = pygame.Rect(x, y, sprite_width, sprite_height)
        sprite = sheet.subsurface(rect)
        sprites.append(sprite)

    return sprites
