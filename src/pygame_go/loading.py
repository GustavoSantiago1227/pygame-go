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
        "fonts",
    ]
    packs = [
        'script',
        'scenes',
        'factory'
    ]
    create_file_and_folder(base_dir, directories, packs)

                                                        #CRIAR O MAIN


    create_archives(base_dir / 'main.py', """from pygame_go.game_loop.basic import Game
from game_asset import asset_init
from game_scenes import scenes_data
from game_fonts import fonts_init

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
asset_init() #Carrega as fonsts do jogo
game.set_scene(scenes_data) #Trás as cenas para dentro do jogo
game.load('exemple') #Carrega a cena de exemplo
game.run()
""")

                                                    #CRIAR O ASSET

    create_archives(base_dir / 'game_asset.py', """from pygame_go.manager.asset import asset

def asset_init():
    '''Instancia as imagens do jogo'''
    asset.set_image({})    #Carrega imagens unicas
    asset.set_frames({})   #Carrega uma lista de imagem
""")



                                                                #CRIAR O SCENES

    create_archives(base_dir / 'game_scenes.py', """from scenes.exemple import Exemple

scenes_data = {
    'exemple': Exemple,
}

""")


                                                                #CRIAR O EXEMPLO SCENES


    create_archives(base_dir / 'scenes' / 'exemple.py', """from pygame_go.scene import Scene

class Exemple(Scene):
    def preload(self):
        pass
""")


                                                                #CRIAR O FONTS

    create_archives(base_dir / 'game_fonts.py', """from pygame_go.manager.fonts import fonts

def fonts_init():
    '''Instancia as fonts de texto do jogo'''
    #Para adicionar uma fonte siga o modelo
    
    #Fonte do sistema
    # id {(nome_da_fonte, tamanho)}
    
    #Fonte externa
    # id {(arquivo_do_fonts, tamanho)}
    fonts.set_fonts({}) 
    """
)



    print(f"Projeto preparado em: {base_dir}")

    return base_dir


def main():
    loading()


if __name__ == "__main__":
    main()