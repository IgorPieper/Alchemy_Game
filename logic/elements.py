from styles.main_styles import *
from styles.preferences import *

from utils.asset_manager import AssetManager

import arcade
import random
import json

ELEMENTS_PATH = "art/elements/"


class Element:
    def __init__(self, name, position_x=None, position_y=None):
        self.name = name
        self.radius = 50

        self.position_x = position_x if position_x is not None else random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.position_y = position_y if position_y is not None else random.randint(self.radius, SCREEN_HEIGHT - self.radius)

        self.dragging = False

        try:
            self.texture = AssetManager.get_element(name)
        except FileNotFoundError:
            self.texture = AssetManager.get_icon(f"{BUTTON_IMAGE_PATH}element_not_found.png")

    @staticmethod
    def translation(name):
        file_name = f"language/{language}.json"
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            return name
        return data.get(name, name)

    def draw(self):
        arcade.draw_texture_rectangle(
            self.position_x,
            self.position_y,
            self.texture.width,
            self.texture.height,
            self.texture
        )
        arcade.draw_text(
            self.translation(self.name),
            self.position_x,
            self.position_y - 75,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

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
        distance = ((self.position_x - other_element.position_x) ** 2 +
                    (self.position_y - other_element.position_y) ** 2) ** 0.5
        return distance < self.radius + other_element.radius
