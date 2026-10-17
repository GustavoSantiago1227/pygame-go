import pygame
from pathlib import Path



class Font:
    def __init__(self):
        self._data = {}
        self._id_defualt = 'defualt'

        self.base_directory = (Path.cwd() / "fonts").resolve()
        self.base_directory.mkdir(parents=True, exist_ok=True)

    def defualts(self):
        """Retorna as fontes existentes"""
        for font in pygame.font.get_fonts():
            print(font)


    def _add_internal_font(self, id_font='defualt', name_font=None, size=36):
        """Adiciona uma fonte do proprio sistema"""
        self._data[id_font] = pygame.font.SysFont(name_font, size)

    def _add_external_font(self, id_font='defualt', file_font=None, size=36):
        """Adiciona uma fonte externa"""
        self._data[id_font] = pygame.font.Font(str(self.base_directory / file_font), size)

    def set_fonts(self, data):
        """Configura as fonsts do jogo"""
        for key, value in data.items():
            font, size = value
            try:

                self._add_external_font(key,font, size)
            except:
                try:
                    self._add_external_font(key, font, size)
                except:
                    print(f"Falha ao carregar a fonte [{key}]")



    def set_id_defualt(self, id_font='defualt'):
        """Seta uma fonte padrão para desenhar"""
        self._id_defualt = id_font

    def get(self, id_font):
        """Retorna uma fonte já pronta"""
        return self._data.get(id_font)

    def write(self, text, color, id_font=None):
        """Esceve uma fonte e retorna o arquivo"""
        id_font = id_font if id_font else self._id_defualt
        return self._data[id_font].render(text, True, color)


    def draw_text(self, screen, pos, text, color, id_font):
        """Já desenha o texto na tela automaticamente"""
        text = self.write(text.text, color, id_font)
        screen.blit(text, pos)

fonts = Font()


