from pyglet.math import Vec2

from logic.elements import *
from styles.preferences import *

import arcade
import time
import json
import os
from datetime import datetime

# Starting position of elements:
ELEMENTS_SPACING = 200


class Alchemy(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=fullscreen)
        arcade.set_background_color(arcade.color.ASH_GREY)
        self.camera = arcade.Camera(self.width, self.height)
        self.clear_log()
        self.click_count = 0
        self.last_click_time = 0
        self.click_threshold = 0.25
        self.elements = []
        self.unlocked_elements = []
        self.button_placement = 1
        self.every_element_count = sum(1 for item in os.listdir(ELEMENTS_PATH)
                                       if os.path.isfile(os.path.join(ELEMENTS_PATH, item)))
        self.spawn_default_elements(SCREEN_MIDDLE_WIDTH, SCREEN_MIDDLE_HEIGHT, ELEMENTS_SPACING)
        self.elements_count = f"Progress: {len(self.unlocked_elements)}/{self.every_element_count}"
        self.dragging_element = None
        self.history = []
        self.current_screen_view = 0

        self.combinations_data = self.load_combinations_data("data/combinations.json")

    @staticmethod
    def load_combinations_data(file_path):
        with open(file_path, "r") as json_file:
            return json.load(json_file)

    def update(self, delta_time):
        self.elements[:] = [element for element in self.elements if element.position_x < RIGHT_PANEL_LEFT_EDGE]

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            BACKGROUND_IMAGE.width,
                                            BACKGROUND_IMAGE.height,
                                            BACKGROUND_IMAGE)

        arcade.draw_texture_rectangle(40, 40,
                                      SETTING_ICON.width,
                                      SETTING_ICON.height, SETTING_ICON)

        for element in self.elements:
            element.draw()

        arcade.draw_rectangle_filled(RIGHT_PANEL_MIDDLE_WIDTH, RIGHT_PANEL_MIDDLE_HEIGHT,
                                     RIGHT_PANEL_WIDTH, RIGHT_PANEL_HEIGHT, TRANSPARENT_BLACK)

        arcade.draw_text(self.elements_count, RIGHT_PANEL_MIDDLE_WIDTH, RIGHT_PANEL_MIDDLE_HEIGHT - 37,
                         arcade.color.WHITE, 18, anchor_x="center")

        arcade.draw_text("------------------------", RIGHT_PANEL_MIDDLE_WIDTH, RIGHT_PANEL_MIDDLE_HEIGHT - 37 - 17,
                         arcade.color.WHITE, 18, anchor_x="center")

        # arcade.draw_text("History:", RIGHT_PANEL_MIDDLE_WIDTH, RIGHT_PANEL_MIDDLE_HEIGHT - 37 - 40,
        #                  arcade.color.WHITE, 15, anchor_x="center")

        self.draw_button(1, ALL_ELEMENTS_ICON, "Catalog")
        self.draw_button(0, RECYCLE_ICON, "Clear")

        # arcade.draw_lrtb_rectangle_filled(left=BUTTON_LEFT_WALL,
        #                                   right=BUTTON_RIGHT_WALL,
        #                                   top=ELEMENT_BUTTON_TOP_WALL,
        #                                   bottom=ELEMENT_BUTTON_BOTTOM_WALL,
        #                                   color=arcade.color.RED)

        # Catalog View
        arcade.draw_lrwh_rectangle_textured(0, 2000,
                                            BACKGROUND_IMAGE.width,
                                            BACKGROUND_IMAGE.height,
                                            BACKGROUND_IMAGE)

        arcade.draw_texture_rectangle(40, 2040,
                                      SETTING_ICON.width,
                                      SETTING_ICON.height, SETTING_ICON)

        arcade.draw_texture_rectangle(BACK_BUTTON_X, BACK_BUTTON_Y + 2000,
                                      SETTING_ICON.width,
                                      SETTING_ICON.height, BACK_BUTTON)

    def draw_button(self, modifier, icon, text):
        padding_height = PADDING_HEIGHT + 80 * modifier

        arcade.draw_texture_rectangle(PADDING_WIDTH, padding_height,
                                      icon.width,
                                      icon.height, icon)

        text_width = PADDING_WIDTH + 40
        text_height = padding_height - 8

        arcade.draw_text(text, text_width, text_height, arcade.color.WHITE, 20, anchor_x="left")

    def on_mouse_press(self, x, y, button, modifiers):
        current_time = time.time()

        # Moving elements
        if button == arcade.MOUSE_BUTTON_LEFT:
            if current_time - self.last_click_time < self.click_threshold:
                self.click_count += 1
            else:
                self.click_count = 1
            self.last_click_time = current_time
        element_clicked = False

        for element in reversed(self.elements):
            if element.check_mouse_press(x, y):
                element_clicked = True
                self.elements.remove(element)
                self.elements.append(element)
                self.dragging_element = element
                self.add_to_history(f"Moving {element.name}", element)
                break

        # Triple-click functionality
        if self.click_count == 3:
            if element_clicked:
                cloned_element = Element(element.name, element.position_x + 75, element.position_y + 75)
                self.elements.append(cloned_element)
            else:
                self.spawn_default_elements(x, y, ELEMENTS_SPACING)
            self.click_count = 0

        # Working clear button
        if ((RIGHT_PANEL_LEFT_BORDER < x < BUTTON_RIGHT_WALL and
                CLEAR_BUTTON_BOTTOM_WALL < y < CLEAR_BUTTON_TOP_WALL) and self.current_screen_view == 0):
            self.elements.clear()

        if ((RIGHT_PANEL_LEFT_BORDER < x < BUTTON_RIGHT_WALL and
                ELEMENT_BUTTON_BOTTOM_WALL < y < ELEMENT_BUTTON_TOP_WALL) and self.current_screen_view == 0):
            self.current_screen_view = 1
            self.camera.move(Vec2(0, 2000))
            self.camera.use()

        if self.click_count == 2:
            if (x - SETTING_BUTTON_X)**2 + (y - SETTING_BUTTON_Y)**2 < SETTING_BUTTON_RADIUS**2:
                self.close()

        # Catalog View
        if (x - BACK_BUTTON_X)**2 + (y - BACK_BUTTON_Y)**2 < BACK_BUTTON_RADIUS**2 and self.current_screen_view == 1:
            self.current_screen_view = 0
            self.camera.move(Vec2(0, 0))
            self.camera.use()


        # Elements fusion
        if not self.click_count == 3 and element_clicked:
            for element in reversed(self.elements):
                if element.check_mouse_press(x, y):
                    self.elements.remove(element)
                    self.elements.append(element)
                    self.dragging_element = element
                    break

    def on_mouse_release(self, x, y, button, modifiers):
        if self.dragging_element:
            for element in self.elements:
                if element != self.dragging_element and self.dragging_element.collides_with(element):
                    result_name = self.check_and_combine_elements(self.dragging_element.name, element.name)
                    if result_name:
                        new_element_x = (self.dragging_element.position_x + element.position_x) / 2
                        new_element_y = (self.dragging_element.position_y + element.position_y) / 2

                        if isinstance(result_name, list):
                            for name in result_name:
                                self.add_element(name, new_element_x, new_element_y)
                                new_element_x += 80
                                new_element_y += 80
                        else:
                            self.add_element(result_name, new_element_x, new_element_y)

                        self.add_to_history(f"Used {element.name}", element)
                        self.add_to_history(f"Used {self.dragging_element.name}", self.dragging_element)
                        self.elements.remove(self.dragging_element)
                        self.elements.remove(element)
                        break
            self.dragging_element = None
        else:
            for element in self.elements:
                if element.dragging:
                    element.check_mouse_release()
                    break

    def on_mouse_motion(self, x, y, dx, dy):
        if self.dragging_element:
            self.dragging_element.position_x += dx
            self.dragging_element.position_y += dy

    def add_element(self, name,  x, y):
        self.elements.append(Element(name, x, y))
        self.elements_count = f"Progress: {len(self.unlocked_elements)}/{self.every_element_count}"

    def spawn_default_elements(self, x, y, spacing):
        positions = {"north": (x, y + spacing // 2),
                     "east": (x + spacing // 2, y),
                     "west": (x - spacing // 2, y),
                     "south": (x, y - spacing // 2)}

        self.elements.append(Element("water", positions["east"][0], positions["east"][1]))
        self.elements.append(Element("fire", positions["west"][0], positions["west"][1]))
        self.elements.append(Element("dirt", positions["south"][0], positions["south"][1]))
        self.elements.append(Element("wind", positions["north"][0], positions["north"][1]))
        if "water" not in self.unlocked_elements:
            self.unlocked_elements.append("water")
            self.unlocked_elements.append("fire")
            self.unlocked_elements.append("dirt")
            self.unlocked_elements.append("wind")

    def check_and_combine_elements(self, element1_name, element2_name):
        for combo in self.combinations_data:
            if {combo["element1"], combo["element2"]} == {element1_name, element2_name}:
                if combo["result"] not in self.unlocked_elements:
                    self.unlocked_elements.append(combo["result"])
                return combo["result"]
        return None

    def clear_log(self):
        with open(LOG, 'w') as file:
            pass

    def add_to_history(self, sentence, element):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        with open(LOG, 'a') as file:
            file.write(f"{current_time} | {sentence}\n")

        if len(self.history) >= 9:
            self.history.pop()
        self.history.insert(0, (sentence, element))

