from ..helpers import *

__all__ = ["convert_beam_direction_to_vector", "get_beam_positions", "ray_vs_rect"]

EPSILON = 1e-6

def convert_beam_direction_to_vector(beam_direction: float) -> vector:
    angle_radians = math.radians(beam_direction)
    dir_x, dir_y = math.cos(angle_radians), math.sin(angle_radians)
    return vector(dir_x, dir_y)


def beam_collides_with_rect(
    start_pos: vector, direction: vector, target_rect: pygame.Rect
) -> bool:
    corners = [
        vector(target_rect.topleft),
        vector(target_rect.topright),
        vector(target_rect.bottomright),
        vector(target_rect.bottomleft),
    ]

    if target_rect.collidepoint(start_pos.x, start_pos.y):
        return True

    for i in range(4):
        p1 = corners[i]
        p2 = corners[(i + 1) % 4]

        if line_intersects(start_pos, start_pos + direction * 10000, p1, p2):
            return True

    return False


def line_intersects(p1: vector, p2: vector, p3: vector, p4: vector) -> bool:
    def ccw(A: vector, B: vector, C: vector) -> bool:
        return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

    return (ccw(p1, p3, p4) != ccw(p2, p3, p4)) and (ccw(p1, p2, p3) != ccw(p1, p2, p4))

def ray_vs_rect(origin: vector, direction: vector, rect: pygame.Rect) -> tuple[float, vector] | None:
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
    mirror_positions: list[pygame.Rect],
    bounds: pygame.Rect | None = None,
) -> list[vector]:
    if bounds is None:
        bounds = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    origin = vector(beam_origin)
    direction = vector(beam_direction)
    dots = [vector(origin)]

    if direction.length() == 0:
        return dots
    direction = direction.normalize()

    seen = set()

    while True:
        nearest = None
        for rect in mirror_positions:
            hit = ray_vs_rect(origin, direction, rect)
            if hit and (nearest is None or hit[0] < nearest[0]):
                nearest = hit

        wall_hit = ray_vs_rect(origin, direction, bounds)

        if nearest is None or (wall_hit and wall_hit[0] < nearest[0]):
            if wall_hit:
                dots.append(origin + direction * wall_hit[0])
            break

        distance, normal = nearest
        hit_point = origin + direction * distance

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
        direction = direction.reflect(normal)
        origin = hit_point + direction * 0.01

    return dots
