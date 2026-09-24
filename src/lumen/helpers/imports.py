import math
import sys
from os import name, system
from pathlib import Path

import pygame
from pygame.math import Vector2 as vector

# Consts
WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 1000

SPRITE_SCALE = (4, 4)


# Functions
def cc():
    system("cls" if name == "nt" else "clear")
