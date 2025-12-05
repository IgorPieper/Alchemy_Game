import arcade
import random
import json

from styles.main_styles import *
from utils.asset_manager import AssetManager


ELEMENTS_PATH = "art/elements/"


class Element(arcade.Sprite):
    def __init__(self, name, position_x=None, position_y=None):
        self.name = name

        texture = AssetManager.get_element(name)

        super().__init__(
            texture=texture,
            center_x=position_x if position_x is not None else random.randint(50, SCREEN_WIDTH - 50),
            center_y=position_y if position_y is not None else random.randint(50, SCREEN_HEIGHT - 50),
            scale=1
        )

        self.dragging = False
        self.radius = 50

    # --------------------
    # POSITION ALIASES
    # --------------------
    @property
    def position_x(self):
        return self.center_x

    @position_x.setter
    def position_x(self, value):
        self.center_x = value

    @property
    def position_y(self):
        return self.center_y

    @position_y.setter
    def position_y(self, value):
        self.center_y = value

    # --------------------
    # TRANSLATION
    # --------------------
    @staticmethod
    def translation(name):
        file_name = f"language/{language}.json"
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            return name
        return data.get(name, name)

    # --------------------
    # DRAW
    # --------------------
    def draw(self):
        super().draw()
        self.draw_label()

    def draw_label(self):
        arcade.draw_text(
            self.translation(self.name),
            self.center_x,
            self.center_y - 75,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

    # --------------------
    # INPUT
    # --------------------
    def check_mouse_press(self, x, y):
        if self.collides_with_point((x, y)):
            self.dragging = True
            return True
        return False

    def check_mouse_release(self):
        self.dragging = False

    def on_mouse_motion(self, x, y):
        if self.dragging:
            self.center_x = max(50, min(SCREEN_WIDTH - 50, x))
            self.center_y = max(50, min(SCREEN_HEIGHT - 50, y))

    # --------------------
    # COLLISION
    # --------------------
    def collides_with(self, other_element):
        return arcade.check_for_collision(self, other_element)
