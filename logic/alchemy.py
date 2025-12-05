import arcade
import json
import os
import time
from datetime import datetime
from pyglet.math import Vec2

from logic.elements import Element, ELEMENTS_PATH
from styles.main_styles import *
from styles.preferences import *


class Alchemy(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=fullscreen)
        arcade.set_background_color(arcade.color.ASH_GREY)
        self.camera = arcade.Camera(self.width, self.height)
        self.clear_log()
        self.elements = []
        self.unlocked_elements = []
        self.history = []
        self.dragging_element = None
        self.click_count = 0
        self.last_click_time = 0
        self.click_threshold = 0.25
        self.current_screen_view = 0
        self.button_placement = 1
        self.every_element_count = sum(
            1 for item in os.listdir(ELEMENTS_PATH)
            if os.path.isfile(os.path.join(ELEMENTS_PATH, item))
        )
        self.elements_count = ""
        self.spawn_default_elements(SCREEN_MIDDLE_WIDTH, SCREEN_MIDDLE_HEIGHT, ELEMENTS_SPACING)
        self.update_progress_text()
        self.combinations_data = self.load_combinations_data("data/combinations.json")
        if debugging_mode:
            self.debugging_unlock_all()

    @staticmethod
    def load_combinations_data(path):
        with open(path, "r") as file:
            return json.load(file)

    def update_progress_text(self):
        self.elements_count = f"Progress: {len(self.unlocked_elements)}/{self.every_element_count}"

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, BACKGROUND_IMAGE.width, BACKGROUND_IMAGE.height, BACKGROUND_IMAGE)
        arcade.draw_texture_rectangle(SETTING_BUTTON_X, SETTING_BUTTON_Y, SETTING_ICON.width, SETTING_ICON.height, SETTING_ICON)
        for element in self.elements:
            element.draw()
        arcade.draw_rectangle_filled(RIGHT_PANEL_MIDDLE_WIDTH, RIGHT_PANEL_MIDDLE_HEIGHT, RIGHT_PANEL_WIDTH, RIGHT_PANEL_HEIGHT, TRANSPARENT_BLACK)
        arcade.draw_text(self.elements_count, RIGHT_PANEL_MIDDLE_WIDTH, RIGHT_PANEL_MIDDLE_HEIGHT - 37, arcade.color.WHITE, 18, anchor_x="center")
        arcade.draw_text("------------------------", RIGHT_PANEL_MIDDLE_WIDTH, RIGHT_PANEL_MIDDLE_HEIGHT - 54, arcade.color.WHITE, 18, anchor_x="center")
        self.draw_button(1, ALL_ELEMENTS_ICON, "Catalog")
        self.draw_button(0, RECYCLE_ICON, "Clear")
        self.draw_catalog()

    def draw_button(self, modifier, icon, text):
        padding_height = PADDING_HEIGHT + 80 * modifier
        arcade.draw_texture_rectangle(PADDING_WIDTH, padding_height, icon.width, icon.height, icon)
        arcade.draw_text(text, PADDING_WIDTH + 40, padding_height - 8, arcade.color.WHITE, 20, anchor_x="left")

    def draw_catalog(self):
        offset = -2000
        arcade.draw_lrwh_rectangle_textured(0, offset, BACKGROUND_IMAGE.width, BACKGROUND_IMAGE.height, BACKGROUND_IMAGE)
        arcade.draw_texture_rectangle(BACK_BUTTON_X, BACK_BUTTON_Y + offset, BACK_BUTTON.width, BACK_BUTTON.height, BACK_BUTTON)
        x = 0
        y = 775
        for name in self.unlocked_elements:
            x += 120
            texture = arcade.load_texture(f"art/elements/{name}.png")
            arcade.draw_texture_rectangle(x, y + offset, texture.width, texture.height, texture)
            if x >= 1440:
                x = 0
                y -= 120

    def update(self, delta_time):
        self.elements[:] = [e for e in self.elements if e.position_x < RIGHT_PANEL_LEFT_BORDER]

    def on_mouse_press(self, x, y, button, modifiers):
        current_time = time.time()
        if button == arcade.MOUSE_BUTTON_LEFT:
            if current_time - self.last_click_time < self.click_threshold:
                self.click_count += 1
            else:
                self.click_count = 1
            self.last_click_time = current_time

        element_clicked, element = self.handle_element_mouse_press(x, y)

        if self.click_count == 3:
            self.handle_triple_click(x, y, element_clicked, element)
            self.click_count = 0
            return

        if self.click_count == 2:
            if (x - SETTING_BUTTON_X) ** 2 + (y - SETTING_BUTTON_Y) ** 2 < SETTING_BUTTON_RADIUS ** 2:
                self.log_action("The game has been turned off")
                self.close()

        if self.current_screen_view == 0:
            self.handle_panel_click(x, y)

        if self.current_screen_view == 1:
            if (x - BACK_BUTTON_X) ** 2 + (y - BACK_BUTTON_Y) ** 2 < BACK_BUTTON_RADIUS ** 2:
                self.current_screen_view = 0
                self.camera.move(Vec2(0, 0))
                self.camera.use()

    def handle_element_mouse_press(self, x, y):
        for element in reversed(self.elements):
            if element.check_mouse_press(x, y):
                self.elements.remove(element)
                self.elements.append(element)
                self.dragging_element = element
                self.log_action(f"Moving {element.name}")
                return True, element
        return False, None

    def handle_triple_click(self, x, y, clicked, element):
        if clicked:
            clone = Element(element.name, element.position_x + 75, element.position_y + 75)
            self.elements.append(clone)
        else:
            self.spawn_default_elements(x, y, ELEMENTS_SPACING)

    def handle_panel_click(self, x, y):
        if BUTTON_LEFT_WALL < x < BUTTON_RIGHT_WALL and CLEAR_BUTTON_BOTTOM_WALL < y < CLEAR_BUTTON_TOP_WALL:
            self.log_action(f"The user deleted {len(self.elements)} elements")
            self.elements.clear()

        if BUTTON_LEFT_WALL < x < BUTTON_RIGHT_WALL and ELEMENT_BUTTON_BOTTOM_WALL < y < ELEMENT_BUTTON_TOP_WALL:
            self.current_screen_view = 1
            self.camera.move(Vec2(0, -2000))
            self.camera.use()

    def on_mouse_release(self, x, y, button, modifiers):
        if self.dragging_element:
            self.handle_drop_collision()
        else:
            for element in self.elements:
                if element.dragging:
                    element.check_mouse_release()
        self.dragging_element = None

    def handle_drop_collision(self):
        for element in self.elements:
            if element != self.dragging_element and self.dragging_element.collides_with(element):
                result = self.combine_elements(self.dragging_element, element)
                if result:
                    x = (self.dragging_element.center_x + element.center_x) / 2
                    y = (self.dragging_element.center_y + element.center_y) / 2
                    if isinstance(result, list):
                        for name in result:
                            self.add_element(name, x, y)
                            x += 80
                            y += 80
                    else:
                        self.add_element(result, x, y)
                    self.log_action(f"Used {element.name}")
                    self.log_action(f"Used {self.dragging_element.name}")
                    self.elements.remove(self.dragging_element)
                    self.elements.remove(element)
                    break

    def on_mouse_motion(self, x, y, dx, dy):
        if self.dragging_element:
            self.dragging_element.center_x += dx
            self.dragging_element.center_y += dy

    def add_element(self, name, x, y):
        self.elements.append(Element(name, x, y))
        if name not in self.unlocked_elements:
            self.unlocked_elements.append(name)
        self.unlocked_elements.sort()
        self.update_progress_text()
        self.log_action(f"{name} has been made")

    def spawn_default_elements(self, x, y, spacing):
        positions = {
            "north": (x, y + spacing // 2),
            "east": (x + spacing // 2, y),
            "west": (x - spacing // 2, y),
            "south": (x, y - spacing // 2)
        }
        names = ["water", "fire", "dirt", "wind"]
        keys = ["east", "west", "south", "north"]
        for name, key in zip(names, keys):
            self.elements.append(Element(name, *positions[key]))
            if name not in self.unlocked_elements:
                self.unlocked_elements.append(name)
        self.log_action("Water, Fire, Dirt and Wind have been unlocked")
        self.update_progress_text()

    def combine_elements(self, e1, e2):
        for combo in self.combinations_data:
            if {combo["element1"], combo["element2"]} == {e1.name, e2.name}:
                result = combo["result"]
                if isinstance(result, list):
                    for r in result:
                        if r not in self.unlocked_elements:
                            self.unlocked_elements.append(r)
                            self.log_action(f"{r} has been unlocked")
                else:
                    if result not in self.unlocked_elements:
                        self.unlocked_elements.append(result)
                        self.log_action(f"{result} has been unlocked")
                self.unlocked_elements.sort()
                self.update_progress_text()
                return result
        return None

    def clear_log(self):
        with open(LOG, "w"):
            pass
        self.log_action("The game has been launched")

    def log_action(self, message):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG, "a") as f:
            f.write(f"{current_time} | {message}\n")

    def debugging_unlock_all(self):
        for file in os.listdir(ELEMENTS_PATH):
            if os.path.isfile(os.path.join(ELEMENTS_PATH, file)):
                name = os.path.splitext(file)[0]
                if name not in self.unlocked_elements:
                    self.unlocked_elements.append(name)
