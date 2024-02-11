from logic.alchemy import Alchemy

import arcade


def main():
    game = Alchemy()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
