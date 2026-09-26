from ..helpers import *

__all__ = ["MirrorSprite"]


class MirrorSprite(pygame.sprite.Sprite):
    def __init__(
        self, position: tuple[int, int], starting_rotation: float, *groups: pygame.sprite.Group
    ) -> None:
        super().__init__(*groups)
        self.screen = pygame.display.get_surface()

        self.original_image = load_sprite(
            MIRROR_ON, scale=(SPRITE_SCALE[0] - 2, SPRITE_SCALE[1] - 2)
        )

        self.position = vector(position)
        self.angle = starting_rotation
        self.rotation_speed = 50.0

        self.image = self.original_image.copy()
        self.rect = self.image.get_frect(center=position)
        self.half_length = self.original_image.get_height() / 2

        self.beam_behavior = "mirror"
        self.hitbox = self.rect.inflate(-4, -4)

        self._update_image()

    def rotate(self, delta: float) -> None:
        self.angle = (self.angle + delta) % 180
        self._update_image()

    def _update_image(self) -> None:
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_frect(center=self.position)

    def get_segment(self) -> tuple[vector, vector]:
        direction = vector(1, 0).rotate(-self.angle)
        return (
            self.position - direction * self.half_length,
            self.position + direction * self.half_length,
        )

    def draw(self) -> None:
        self.screen.blit(self.image, self.rect)

    def handle_input(self, dt: float) -> None:
        mouse_pos = pygame.mouse.get_pos()

        if not self.rect.collidepoint(mouse_pos):
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-self.rotation_speed * dt)
        if keys[pygame.K_d]:
            self.rotate(self.rotation_speed * dt)

    def update(self, dt: float) -> None:
        self.handle_input(dt)