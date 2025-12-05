from utils.asset_manager import AssetManager
from styles.preferences import background_image_name
from styles.constants import BUTTON_IMAGE_PATH

BACKGROUND_IMAGE = AssetManager.get_icon(f"art/background/{background_image_name}.png")

SETTING_ICON = AssetManager.get_icon(f"{BUTTON_IMAGE_PATH}power.png")
RECYCLE_ICON = AssetManager.get_icon(f"{BUTTON_IMAGE_PATH}clear.png")
ALL_ELEMENTS_ICON = AssetManager.get_icon(f"{BUTTON_IMAGE_PATH}endless.png")
BACK_BUTTON = AssetManager.get_icon(f"{BUTTON_IMAGE_PATH}back.png")
