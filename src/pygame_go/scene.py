import pygame
from pygame_go.group import tags, unique

class Scene:
    def __init__(self, load, close, width, height):
        self.load = load
        self.close = close
        self.screen_width = width
        self.screen_height = height

        self.preload()

    def preload(self):
        """Atualiza apenas na iniciação da cena"""
        pass

    def update(self):
        """Atualiza a todo instante"""
        pass

    def keyboard_mouse(self, key, mouse_pos, mouse_press):
        """
        - Captura teclas precionadas
        - Captura posição do mouse
        - Captura qual tecla foi pressionada
        """
        pass


    def events(self, events):
        """Captura de eventos do jogo"""
        pass

    def draw(self, screen):
        """Desenha os objetos no jogo"""
        pass

