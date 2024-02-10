import arcade
import random

# Variables
SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
SCREEN_TITLE = "Alchemy"
ELEMENTS_PATH = "art/elements/"


class Element:
    def __init__(self, name):
        self.name = name
        self.radius = 50
        self.position_x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.position_y = random.randint(self.radius, SCREEN_HEIGHT - self.radius)
        self.texture = arcade.load_texture(f"{ELEMENTS_PATH}{name}.png")
        self.scale = 2 * 50 / self.texture.width
        self.dragging = False

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
        self.circles = []
        self.circles.append(Element("water"))
        self.circles.append(Element("fire"))
        self.circles.append(Element("dirt"))
        self.circles.append(Element("wind"))

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()
        for circle in self.circles:
            circle.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for circle in reversed(self.circles):
            if circle.check_mouse_press(x, y):
                self.circles.remove(circle)
                self.circles.append(circle)
                break

    def on_mouse_release(self, x, y, button, modifiers):
        for circle in self.circles:
            circle.check_mouse_release()

    def on_mouse_motion(self, x, y, dx, dy):
        for circle in self.circles:
            circle.on_mouse_motion(x, y)


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
