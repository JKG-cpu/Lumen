import pygame
import pytest

from src.lumen.logic import (
    convert_beam_direction_to_vector,
    get_beam_positions,
    ray_vs_rect,
)

vector = pygame.math.Vector2
BOUNDS = pygame.Rect(0, 0, 800, 600)


def close(v, x, y):
    return v.x == pytest.approx(x, abs=0.1) and v.y == pytest.approx(y, abs=0.1)


# ---------- direction conversion ----------

def test_direction_right():
    v = convert_beam_direction_to_vector(0)
    assert close(v, 1, 0)


def test_direction_down():
    # pygame's y axis points DOWN, so 90 degrees is down the screen
    v = convert_beam_direction_to_vector(90)
    assert close(v, 0, 1)


# ---------- ray_vs_rect ----------

def test_ray_hits_left_face_head_on():
    rect = pygame.Rect(200, 50, 100, 100)
    hit = ray_vs_rect(vector(0, 100), vector(1, 0), rect)
    assert hit is not None
    distance, normal = hit
    assert distance == pytest.approx(200)
    assert close(normal, -1, 0)


def test_ray_misses_rect():
    rect = pygame.Rect(200, 300, 100, 100)
    assert ray_vs_rect(vector(0, 100), vector(1, 0), rect) is None


def test_ray_pointing_away_misses_rect():
    rect = pygame.Rect(200, 50, 100, 100)
    assert ray_vs_rect(vector(0, 100), vector(-1, 0), rect) is None


# ---------- get_beam_positions ----------

def test_beam_with_no_obstacles_goes_to_screen_edge():
    dots = get_beam_positions(vector(0, 100), vector(1, 0), [], BOUNDS)
    assert len(dots) == 2
    assert close(dots[0], 0, 100)
    assert close(dots[-1], 800, 100)


def test_beam_stops_at_screen_edge_and_does_not_continue():
    dots = get_beam_positions(vector(400, 300), vector(0, -1), [], BOUNDS)
    assert len(dots) == 2
    assert close(dots[-1], 400, 0)


def test_head_on_bounce_returns_the_way_it_came():
    rect = pygame.Rect(200, 50, 100, 100)
    dots = get_beam_positions(vector(0, 100), vector(1, 0), [rect], BOUNDS)
    assert len(dots) == 3
    assert close(dots[1], 200, 100)  # hit the left face
    assert close(dots[2], 0, 100)    # came back to the left edge


def test_45_degree_bounce_off_top_face():
    rect = pygame.Rect(100, 200, 200, 100)
    dots = get_beam_positions(vector(150, 100), vector(1, 1), [rect], BOUNDS)
    assert len(dots) == 3
    assert close(dots[1], 250, 200)  # hit the top face
    assert close(dots[2], 450, 0)    # bounced up and to the right, off the top


def test_nearest_rect_wins():
    near = pygame.Rect(200, 50, 100, 100)
    far = pygame.Rect(400, 50, 100, 100)
    dots = get_beam_positions(vector(0, 100), vector(1, 0), [far, near], BOUNDS)
    assert close(dots[1], 200, 100)


def test_beam_trapped_between_two_facing_rects_does_not_hang():
    left = pygame.Rect(100, 50, 50, 100)
    right = pygame.Rect(300, 50, 50, 100)
    dots = get_beam_positions(vector(200, 100), vector(1, 0), [left, right], BOUNDS)
    assert len(dots) == 3  # start, right rect, left rect, then the loop is detected


def test_zero_direction_returns_just_the_origin():
    dots = get_beam_positions(vector(10, 10), vector(0, 0), [], BOUNDS)
    assert len(dots) == 1