from typing import Any, NamedTuple

from ..helpers import *

__all__ = [
    "Obstacle",
    "calculate_vector_distance",
    "convert_beam_direction_to_vector",
    "get_beam_positions",
    "ray_vs_rect",
]

EPSILON = 1e-6


class Obstacle(NamedTuple):
    rect: pygame.Rect | pygame.FRect
    behavior: str = "mirror"
    owner: Any = None


def convert_beam_direction_to_vector(beam_direction: float) -> vector:
    angle_radians = math.radians(beam_direction)
    dir_x, dir_y = math.cos(angle_radians), math.sin(angle_radians)
    return vector(dir_x, dir_y)


def ray_vs_rect(
    origin: vector, direction: vector, rect: pygame.Rect | pygame.FRect
) -> tuple[float, vector] | None:
    corners = [
        vector(rect.topleft),
        vector(rect.topright),
        vector(rect.bottomright),
        vector(rect.bottomleft),
    ]
    normals = [vector(0, -1), vector(1, 0), vector(0, 1), vector(-1, 0)]

    best = None
    for i in range(4):
        a = corners[i]
        b = corners[(i + 1) % 4]
        edge = b - a

        denom = direction.cross(edge)
        if abs(denom) < EPSILON:
            continue

        t = (a - origin).cross(edge) / denom
        u = (a - origin).cross(direction) / denom

        if t > 0.001 and 0 <= u <= 1 and (best is None or t < best[0]):
            best = (t, normals[i])

    return best


def get_beam_positions(
    beam_origin: vector,
    beam_direction: vector,
    obstacles: list[Obstacle],
    bounds: pygame.Rect | None = None,
) -> tuple[list[vector], list[Any]]:
    if bounds is None:
        bounds = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    origin = vector(beam_origin)
    direction = vector(beam_direction)
    dots = [vector(origin)]
    hit_targets: list[Any] = []

    if direction.length() == 0:
        return dots, hit_targets
    direction = direction.normalize()

    seen = set()

    while True:
        nearest = None
        for obstacle in obstacles:
            hit = ray_vs_rect(origin, direction, obstacle.rect)
            if hit and (nearest is None or hit[0] < nearest[0]):
                nearest = (hit[0], hit[1], obstacle)

        wall_hit = ray_vs_rect(origin, direction, bounds)

        if nearest is None or (wall_hit and wall_hit[0] < nearest[0]):
            if wall_hit:
                dots.append(origin + direction * wall_hit[0])
            break

        distance, normal, obstacle = nearest
        hit_point = origin + direction * distance

        if obstacle.behavior == "mirror":
            state = (
                round(hit_point.x, 2),
                round(hit_point.y, 2),
                round(direction.x, 3),
                round(direction.y, 3),
            )
            if state in seen:
                break
            seen.add(state)

        dots.append(hit_point)

        if obstacle.behavior == "target":
            if obstacle.owner not in hit_targets:
                hit_targets.append(obstacle.owner)
            break

        if obstacle.behavior == "wall":
            break

        direction = direction.reflect(normal)
        origin = hit_point + direction * 0.01

    return dots, hit_targets


def calculate_vector_distance(v1: vector, v2: vector) -> float:
    return v1.distance_to(v2)