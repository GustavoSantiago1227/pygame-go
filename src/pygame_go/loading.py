from pathlib import Path






def create_archives(file_dir, content=''):
    # Arquivo principal do jogo

    if not file_dir.exists():
        file_dir.write_text(content, encoding="utf-8")

def create_file_and_folder(base_dir, directories=None, packs=None):
    """Cria pastas e arquivos """
    for directory in directories:
        path = base_dir / directory
        path.mkdir(parents=True, exist_ok=True)

        # Cria o __init__.py dentro da pasta script
        if directory in packs:
            init_file = path / "__init__.py"

            if not init_file.exists():
                init_file.write_text("", encoding="utf-8")


def loading(root_path=None):
    """Cria a estrutura inicial de um projeto Pygame."""
    base_dir = Path(root_path or Path.cwd()).resolve()
    directories = [
        "asset",
        "sounds",
        "script",
        "factory",
        "scenes",
    ]
    packs = [
        'script',
        'scene',
    ]
    create_file_and_folder(base_dir, directories, packs)

    #Cria o main
    create_archives(base_dir / 'main.py', """
from pygame_go.game_loop.basic import Game
from game_asset import asset_init
from game_scenes import scenes_load

game = Game(
    title="Meu Jogo",
    width=1280,
    height=720,
    fullscreen=False,
    fps=60,
    debug=True,
    screen_color=(30, 30, 40),
)
asset_init() #Carrega as imagens do jogo


game.run()
""")
    create_archives(base_dir / 'game_asset.py', """
from pygame_go.manager.asset import Asset

asset = Asset()

def asset_init():
    #Instancia as imagens do jogo
    asset.set_image({})    #Carrega imagens unicas
    asset.set_frames({})   #Carrega uma lista de imagem
""")



    create_archives(base_dir / 'game_scenes.py', """
from scenes.exemple import Exemple

def scenes_load():
    scenes_data = {
        'exemple': Exemple,
    }
    return scenes_data

""")

    create_archives(base_dir / 'scenes' / 'exemple.py', """
from pygame_go.scene import Scene

class Exemple(Scene):
    def preload(self):
        pass
""")


    print(f"Projeto preparado em: {base_dir}")

    return base_dir


def main():
    loading()


if __name__ == "__main__":
    main()