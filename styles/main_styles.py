import arcade
from styles.preferences import *

# Windows Attributes
SCREEN_TITLE = "Alchemy"
BACKGROUND_IMAGE = arcade.load_texture(f"art/background/{background_image_name}.png")

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
SCREEN_MIDDLE_WIDTH = SCREEN_WIDTH // 2
SCREEN_MIDDLE_HEIGHT = SCREEN_HEIGHT // 2

BUTTON_IMAGE_PATH = "art/functional/"
LOG = "data/log.txt"

# Bottom Left Button
SETTING_ICON = arcade.load_texture(f"{BUTTON_IMAGE_PATH}power.png")
SETTING_BUTTON_X = 40
SETTING_BUTTON_Y = 40
SETTING_BUTTON_RADIUS = 25

# Right Panel
RIGHT_PANEL_SCALE = 7
TRANSPARENT_BLACK = (0, 0, 0, 150)

RIGHT_PANEL_WIDTH = SCREEN_WIDTH // RIGHT_PANEL_SCALE
RIGHT_PANEL_LEFT_BORDER = SCREEN_WIDTH - (SCREEN_WIDTH // RIGHT_PANEL_SCALE)
RIGHT_PANEL_MIDDLE_WIDTH = SCREEN_WIDTH - (SCREEN_WIDTH // RIGHT_PANEL_SCALE) / 2
RIGHT_PANEL_HEIGHT = SCREEN_HEIGHT * 2
RIGHT_PANEL_MIDDLE_HEIGHT = SCREEN_HEIGHT
RIGHT_PANEL_LEFT_EDGE = SCREEN_WIDTH - (SCREEN_WIDTH // RIGHT_PANEL_SCALE)

# Right Panel Art (50x50 px)
RECYCLE_ICON = arcade.load_texture(f"{BUTTON_IMAGE_PATH}clear.png")
ALL_ELEMENTS_ICON = arcade.load_texture(f"{BUTTON_IMAGE_PATH}endless.png")

# Right Panel Button
PADDING_WIDTH = RIGHT_PANEL_LEFT_BORDER + 50
PADDING_HEIGHT = 50

BUTTON_LEFT_WALL = RIGHT_PANEL_LEFT_BORDER
BUTTON_RIGHT_WALL = RIGHT_PANEL_LEFT_BORDER + 300
CLEAR_BUTTON_BOTTOM_WALL = RECYCLE_ICON.height - 40
CLEAR_BUTTON_TOP_WALL = RECYCLE_ICON.height + 40
ELEMENT_BUTTON_BOTTOM_WALL = (ALL_ELEMENTS_ICON.height - 40) + 82
ELEMENT_BUTTON_TOP_WALL = (ALL_ELEMENTS_ICON.height + 40) + 82

# Catalog View
BACK_BUTTON = arcade.load_texture(f"{BUTTON_IMAGE_PATH}back.png")

BACK_BUTTON_X = SCREEN_WIDTH - 40
BACK_BUTTON_Y = 40
BACK_BUTTON_RADIUS = 25
