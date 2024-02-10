import arcade
import random
import time

# Variables (easy to change)
SCREEN_TITLE = "Alchemy"
ELEMENTS_PATH = "art/elements/"

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
SCREEN_MIDDLE_WIDTH = SCREEN_WIDTH // 2
SCREEN_MIDDLE_HEIGHT = SCREEN_HEIGHT // 2

# Right Panel -------------------------------------------------------------------------------------------

# Np. 7 = 1:7 window scale
RIGHT_PANEL_SCALE = 7

RIGHT_PANEL_WIDTH = SCREEN_WIDTH // RIGHT_PANEL_SCALE
RIGHT_PANEL_MIDDLE_WIDTH = SCREEN_WIDTH - (SCREEN_WIDTH // RIGHT_PANEL_SCALE) / 2
RIGHT_PANEL_HEIGHT = SCREEN_HEIGHT * 2
RIGHT_PANEL_MIDDLE_HEIGHT = SCREEN_HEIGHT
RIGHT_PANEL_LEFT_EDGE = SCREEN_WIDTH - (SCREEN_WIDTH // RIGHT_PANEL_SCALE)

# Starting position of elements:
ELEMENTS_SPACING = 200


class Element:
    def __init__(self, name, is_unlocked=None, position_x=None, position_y=None):
        self.name = name
        self.radius = 50
        self.position_x = position_x if position_x is not None else random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.position_y = position_y if position_y is not None else random.randint(self.radius, SCREEN_HEIGHT - self.radius)
        self.texture = arcade.load_texture(f"{ELEMENTS_PATH}{name}.png")
        self.scale = 2 * 50 / self.texture.width
        self.dragging = False
        self.is_unlocked = is_unlocked if is_unlocked is not None else False

    def draw(self):
        arcade.draw_texture_rectangle(self.position_x, self.position_y, self.texture.width * self.scale, self.texture.height * self.scale, self.texture)
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


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.ASH_GREY)

        self.click_count = 0
        self.last_click_time = 0
        self.click_threshold = 0.25

        self.elements = []
        self.spawn_default_elements(SCREEN_MIDDLE_WIDTH, SCREEN_MIDDLE_HEIGHT, ELEMENTS_SPACING)

    def update(self, delta_time):
        self.elements[:] = [element for element in self.elements if element.position_x < RIGHT_PANEL_LEFT_EDGE]

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()
        for element in self.elements:
            element.draw()

        arcade.draw_rectangle_filled(RIGHT_PANEL_MIDDLE_WIDTH, RIGHT_PANEL_MIDDLE_HEIGHT,
                                     RIGHT_PANEL_WIDTH, RIGHT_PANEL_HEIGHT, arcade.color.GRAY)

    def on_mouse_press(self, x, y, button, modifiers):
        for element in reversed(self.elements):
            if element.check_mouse_press(x, y):
                self.elements.remove(element)
                self.elements.append(element)
                break

        current_time = time.time()
        if button == arcade.MOUSE_BUTTON_LEFT:
            if current_time - self.last_click_time < self.click_threshold:
                self.click_count += 1
            else:
                self.click_count = 1
            if self.click_count == 3:
                self.spawn_default_elements(x, y, ELEMENTS_SPACING)
                self.click_count = 0

            self.last_click_time = current_time

    def on_mouse_release(self, x, y, button, modifiers):
        for element in self.elements:
            element.check_mouse_release()

    def on_mouse_motion(self, x, y, dx, dy):
        for element in self.elements:
            element.on_mouse_motion(x, y)

    def add_element(self, x, y):
        new_element = Element("water", True, x, y)
        self.elements.append(new_element)

    def spawn_default_elements(self, x, y, spacing):
        positions = {"north": (x, y + spacing // 2),
                     "east": (x + spacing // 2, y),
                     "west": (x - spacing // 2, y),
                     "south": (x, y - spacing // 2)}

        self.elements.append(Element("water", True, positions["east"][0], positions["east"][1]))
        self.elements.append(Element("fire", True, positions["west"][0], positions["west"][1]))
        self.elements.append(Element("dirt", True, positions["south"][0], positions["south"][1]))
        self.elements.append(Element("wind", True, positions["north"][0], positions["north"][1]))


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
