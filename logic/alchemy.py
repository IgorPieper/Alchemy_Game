from logic.elements import *

import arcade
import time
import json
import os

# Starting position of elements:
ELEMENTS_SPACING = 200


class Alchemy(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.ASH_GREY)
        self.click_count = 0
        self.last_click_time = 0
        self.click_threshold = 0.25
        self.elements = []
        self.unlocked_elements = []
        self.elements_count = "4/33"
        self.every_element_count = sum(1 for item in os.listdir(ELEMENTS_PATH)
                                       if os.path.isfile(os.path.join(ELEMENTS_PATH, item)))
        self.spawn_default_elements(SCREEN_MIDDLE_WIDTH, SCREEN_MIDDLE_HEIGHT, ELEMENTS_SPACING)
        self.dragging_element = None

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
        for element in self.elements:
            element.draw()

        arcade.draw_rectangle_filled(RIGHT_PANEL_MIDDLE_WIDTH, RIGHT_PANEL_MIDDLE_HEIGHT,
                                     RIGHT_PANEL_WIDTH, RIGHT_PANEL_HEIGHT, TRANSPARENT_BLACK)

        self.draw_button(0, RECYCLE_ICON, "Clear")
        self.draw_button(1, ALL_ELEMENTS_ICON, "Elements")

        arcade.draw_text(self.elements_count, RIGHT_PANEL_MIDDLE_WIDTH, RIGHT_PANEL_MIDDLE_HEIGHT - 37,
                         arcade.color.WHITE, 20, anchor_x="center")

    def draw_button(self, modifier, icon, text):
        padding_width = RIGHT_PANEL_LEFT_BORDER + 50
        padding_height = 50 + 80 * modifier

        arcade.draw_texture_rectangle(padding_width, padding_height,
                                      icon.width,
                                      icon.height, icon)

        text_width = padding_width + 40
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
                break

        # Triple-click functionality
        if self.click_count == 3:
            if element_clicked:
                cloned_element = Element(element.name, True, element.position_x + 10, element.position_y + 10)
                self.elements.append(cloned_element)
            else:
                self.spawn_default_elements(x, y, ELEMENTS_SPACING)
            self.click_count = 0  # Reset click count after handling

        # Working clear button
        trash_icon_width_scaled = RECYCLE_ICON.width
        trash_icon_height_scaled = RECYCLE_ICON.height
        trash_button_x_start = RIGHT_PANEL_MIDDLE_WIDTH - 50 - trash_icon_width_scaled // 2
        trash_button_x_end = RIGHT_PANEL_MIDDLE_WIDTH + 20 + 40
        trash_button_y_start = 75 - trash_icon_height_scaled // 2
        trash_button_y_end = 75 + trash_icon_height_scaled // 2

        if trash_button_x_start < x < trash_button_x_end and trash_button_y_start < y < trash_button_y_end:
            self.elements.clear()

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
                        self.add_element(result_name, new_element_x, new_element_y)
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
        self.elements.append(Element(name, True, x, y))
        self.elements_count = f"{len(self.unlocked_elements)}/{self.every_element_count}"

    def spawn_default_elements(self, x, y, spacing):
        positions = {"north": (x, y + spacing // 2),
                     "east": (x + spacing // 2, y),
                     "west": (x - spacing // 2, y),
                     "south": (x, y - spacing // 2)}

        self.elements.append(Element("water", True, positions["east"][0], positions["east"][1]))
        self.elements.append(Element("fire", True, positions["west"][0], positions["west"][1]))
        self.elements.append(Element("dirt", True, positions["south"][0], positions["south"][1]))
        self.elements.append(Element("wind", True, positions["north"][0], positions["north"][1]))
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
