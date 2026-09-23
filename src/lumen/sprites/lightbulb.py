from ..helpers import *

__all__ = ["LightBulbSprite"]


class LightBulbSprite(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], *group: pygame.sprite.Group) -> None:
        super().__init__(*group)
        self.screen = pygame.display.get_surface()

        self.sprites: dict[str, list[pygame.Surface]] = {
            "off": [load_sprite(LIGHTBULB_OFF, scale = SPRITE_SCALE)],
            "on": [load_sprite(LIGHTBULB_ON, scale = SPRITE_SCALE)],
            "animation": load_sprites(LIGHTBULB_ANIMATION, 32, 32, 9, scale = SPRITE_SCALE)
        }
        self.current_state = "off"
        self.bulb_activated = False

        self.frame_index = 0.0
        self.animation_speed = 10

        self.image = self.sprites[self.current_state][int(self.frame_index)]
        self.rect = self.image.get_frect(center = position)
    
    def check_animation(self, dt: float) -> None:
        if self.bulb_activated:
            self.frame_index += self.animation_speed * dt

            if int(self.frame_index) >= len(self.sprites["animation"]):
                self.bulb_activated = False
                self.current_state = "on"
                self.frame_index = 0

    def draw(self) -> None:
        self.image = self.sprites[self.current_state][int(self.frame_index)]
        self.screen.blit(self.image, self.rect)

    def activate_bulb(self) -> None:
        self.bulb_activated = True
        self.current_state = "animation"
    
    def beam_latched(self, latched: bool) -> None:
        if latched:
            if not self.bulb_activated:
                self.activate_bulb()

        else:
            self.current_state = "off"
            self.frame_index = 0

    def update(self, dt: float) -> None:
        self.check_animation(dt)