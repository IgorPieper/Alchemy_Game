import arcade

# Windows Attributes
SCREEN_TITLE = "Alchemy"
ELEMENTS_PATH = "art/elements/"

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
SCREEN_MIDDLE_WIDTH = SCREEN_WIDTH // 2
SCREEN_MIDDLE_HEIGHT = SCREEN_HEIGHT // 2

# Right Panel
RIGHT_PANEL_SCALE = 7

RIGHT_PANEL_WIDTH = SCREEN_WIDTH // RIGHT_PANEL_SCALE
RIGHT_PANEL_MIDDLE_WIDTH = SCREEN_WIDTH - (SCREEN_WIDTH // RIGHT_PANEL_SCALE) / 2
RIGHT_PANEL_HEIGHT = SCREEN_HEIGHT * 2
RIGHT_PANEL_MIDDLE_HEIGHT = SCREEN_HEIGHT
RIGHT_PANEL_LEFT_EDGE = SCREEN_WIDTH - (SCREEN_WIDTH // RIGHT_PANEL_SCALE)

# Right Panel Buttons
RIGHT_PANEL_IMAGE_SCALE = 7
