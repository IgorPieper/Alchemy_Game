import arcade


class AssetManager:
    element_textures = {}
    icons = {}

    @staticmethod
    def get_element(name):
        if name not in AssetManager.element_textures:
            try:
                AssetManager.element_textures[name] = arcade.load_texture(f"art/elements/{name}.png")
            except FileNotFoundError:
                AssetManager.element_textures[name] = arcade.load_texture("art/functional/element_not_found.png")
        return AssetManager.element_textures[name]

    @staticmethod
    def get_icon(path):
        if path not in AssetManager.icons:
            AssetManager.icons[path] = arcade.load_texture(path)
        return AssetManager.icons[path]
