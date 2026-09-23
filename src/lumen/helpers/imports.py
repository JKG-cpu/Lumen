import sys
from os import name, system
from pathlib import Path

import pygame

# Consts
WINDOW_WIDTH, WINDOW_HEIGHT = 900, 750


# Functions
def cc():
    system("cls" if name == "nt" else "clear")
