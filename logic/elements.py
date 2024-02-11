from styles.main_styles import *

import arcade
import random

# Elements
ELEMENTS_PATH = "art/elements/"


class Element:
    def __init__(self, name, is_unlocked=None, position_x=None, position_y=None):
        self.name = name
        self.radius = 50
        self.position_x = position_x if position_x is not None else random.randint(self.radius,
                                                                                   SCREEN_WIDTH - self.radius)
        self.position_y = position_y if position_y is not None else random.randint(self.radius,
                                                                                   SCREEN_HEIGHT - self.radius)
        self.dragging = False

        self.texture = arcade.load_texture(f"{ELEMENTS_PATH}{name}.png")
        self.scale = 2 * 50 / self.texture.width

    def draw(self):
        arcade.draw_texture_rectangle(self.position_x, self.position_y, self.texture.width * self.scale,
                                      self.texture.height * self.scale, self.texture)
        arcade.draw_text(self.name, self.position_x, self.position_y - 75, arcade.color.WHITE, 20, anchor_x="center")

    def check_mouse_press(self, x, y):
        distance = ((x - self.position_x) ** 2 + (y - self.position_y) ** 2) ** 0.5
        if distance <= self.radius:
            self.dragging = True
            return True
        return False

    def check_mouse_release(self):
        self.dragging = False

    def on_mouse_motion(self, x, y):
        if self.dragging:
            new_x = max(self.radius, min(SCREEN_WIDTH - self.radius, x))
            new_y = max(self.radius, min(SCREEN_HEIGHT - self.radius, y))
            self.position_x = new_x
            self.position_y = new_y

    def collides_with(self, other_element):
        distance = ((self.position_x - other_element.position_x) ** 2 + (
                self.position_y - other_element.position_y) ** 2) ** 0.5
        return distance < self.radius + other_element.radius
