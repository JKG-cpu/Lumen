from .imports import Path

__all__ = ["LIGHTBULB_ANIMATION", "LIGHTBULB_OFF", "LIGHTBULB_ON"]


# Assets
ASSETS_DIR = Path("src", "lumen", "assets")

BEAM_DIR = ASSETS_DIR / "beam"

LIGHTBULB_DIR = ASSETS_DIR / "lightbulb"
LIGHTBULB_OFF = LIGHTBULB_DIR / "off.png"
LIGHTBULB_ON = LIGHTBULB_DIR / "on.png"
LIGHTBULB_ANIMATION = LIGHTBULB_DIR / "animation.png"

MIRROR_DIR = ASSETS_DIR / "mirror"
