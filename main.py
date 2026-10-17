from pygame_go.game_loop.basic import Game
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
