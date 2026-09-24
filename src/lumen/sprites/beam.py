import itertools

from ..helpers import *
from ..logic import (
    Obstacle,
    calculate_vector_distance,
    convert_beam_direction_to_vector,
    get_beam_positions,
)

__all__ = ["BeamSprite"]


class BeamSprite(pygame.sprite.Sprite):
    def __init__(
        self, starting_position: tuple[int, int], obstacle_group: pygame.sprite.Group, *groups: pygame.sprite.Group
    ) -> None:
        super().__init__(*groups)
        self.screen = pygame.display.get_surface()
        self.obstacle_group = obstacle_group

        self.beam_direction: float = 90.0
        self.speed: int = 50
        self.sped_up_speed: int = 100
        self.speed_up: bool = False
        self.starting_position = starting_position
        self.obstacles: list[pygame.Rect] = []

        self.original_base_image = load_sprite(BASE, scale=SPRITE_SCALE)
        self.original_beam_image = load_sprite(BEAM, scale=SPRITE_SCALE)

        self.base_image = self.original_base_image.copy()
        self.base_rect = self.base_image.get_frect(midbottom=starting_position)

        self.beam_segments: list[tuple[pygame.Surface, pygame.FRect]] = []

    def set_obstacles(self, obstacles: list[pygame.Rect]) -> None:
        self.obstacles = obstacles

    def draw(self) -> None:
        for image, rect in self.beam_segments:
            self.screen.blit(image, rect)
        self.screen.blit(self.base_image, self.base_rect)

    def clamp_beam_direction(self, current_direction: float) -> float:
        return max(25.0, min(current_direction, 155.0))

    def handle_input(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.beam_direction += self.speed * dt if not self.speed_up else self.sped_up_speed * dt
            self.beam_direction = self.clamp_beam_direction(self.beam_direction)

        if keys[pygame.K_RIGHT]:
            self.beam_direction -= self.speed * dt if not self.speed_up else self.sped_up_speed * dt
            self.beam_direction = self.clamp_beam_direction(self.beam_direction)

        if keys[pygame.K_LSHIFT]:
            self.speed_up = True
        
        else:
            self.speed_up = False

    def rotate_base(self) -> None:
        self.base_image = pygame.transform.rotate(
            self.original_base_image, self.beam_direction - 90
        )
        base_offset = vector(0, self.original_base_image.get_height() / 2)
        rotated_base_offset = base_offset.rotate(-self.beam_direction + 90)
        self.base_rect = self.base_image.get_frect(
            center=self.starting_position - rotated_base_offset
        )

    def build_beam_segments(
        self, points: list[vector]
    ) -> list[tuple[pygame.Surface, pygame.FRect]]:
        segments = []
        width = self.original_beam_image.get_width()

        for a, b in itertools.pairwise(points):
            length = calculate_vector_distance(a, b)
            if length < 1:
                continue

            angle = math.degrees(math.atan2(-(b.y - a.y), b.x - a.x))
            image = pygame.transform.scale(
                self.original_beam_image, (width, int(length))
            )
            image = pygame.transform.rotate(image, angle - 90)
            rect = image.get_frect(center=(a + b) / 2)

            segments.append((image, rect))

        return segments

    def update_beam(self) -> None:
        direction = convert_beam_direction_to_vector(-self.beam_direction)
        muzzle = (
            vector(self.starting_position)
            + direction * self.original_base_image.get_height()
        )

        margin = self.original_beam_image.get_height()
        bounds = self.screen.get_rect().inflate(margin * 2, margin * 2)

        obstacles = [
            Obstacle(s.hitbox, s.beam_behavior, s)
            for s in self.obstacle_group.sprites()
        ]
        points, hit_targets = get_beam_positions(muzzle, direction, obstacles, bounds)
        self.beam_segments = self.build_beam_segments(points)

        for sprite in self.obstacle_group.sprites():
            if sprite.beam_behavior == "target":
                sprite.set_lit(sprite in hit_targets)

    def update(self, dt: float) -> None:
        self.handle_input(dt)
        self.rotate_base()
        self.update_beam()
