# from styles.main_styles import *
#
# import arcade
#
# BUTTON_IMAGE_PATH = "art/functional/"
#
#
# class Clear_Button:
#     def __init__(self):
#         self.trash_icon = arcade.load_texture(f"{BUTTON_IMAGE_PATH}clear.png")
#
#     def draw_trash_icon(self, x, y, scale=1):
#         arcade.draw_texture_rectangle(x, y,
#                                       self.trash_icon.width // scale,
#                                       self.trash_icon.height // scale,
#                                       self.trash_icon)
#         arcade.draw_text("Clear", RIGHT_PANEL_MIDDLE_WIDTH + 20, 67, arcade.color.WHITE, 20, anchor_x="center")
