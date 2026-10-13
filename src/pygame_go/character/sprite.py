import pygame
from pygame_go.manager.asset import asset
from pygame_go.time.for_update import Timeout


class Image(pygame.sprite.Sprite):
    def __init__(self, name, size=None, flip=None):
        super().__init__()
        self.image = None
        self.rect = None
        self.update_image(name, size, flip)

    def update_image(self, name=None, size=None, flip=None):
        """Atualiza a imagem do sprite"""

        #Pega a imagem do asset ou recebe a imagem
        image_origin = asset.static.get(name) if name else self.image

        #Verifica o tamanho
        if size:
            image_origin = pygame.transform.scale(image_origin, (size))

        #Verifica se precisa virar
        if flip:
            image_origin = pygame.transform.flip(image_origin, flip[0], flip[1])

        #insere no sprite
        self.image = image_origin

        #Verifica se o quadrado já possuia uma coordenada
        if self.rect:
            x, y = self.rect.topleft
        else:
            x, y = 0, 0
        self.rect = image_origin.get_rect()
        self.rect.topleft = (x, y)



class Flat(pygame.sprite.Sprite):
    def __init__(self, name, size=None, flip=None, tick=10, flattening=3):
        """Criação de um sprite animado simples de poing"""
        super().__init__()
        self.image = None
        self.rect = None
        self._sprites = []
        self.indexSprite = 0
        self.time = Timeout(start=tick, loop=True)
        self.flattening = flattening
        self.update_image(name, size, flip, flattening)
        self._updateAnimation()


    def update_image(self, name=None, size=None, flip=None, flattening=None):
        """Atualiza a imagem base"""

        #Verifica qual a origem da nova imagem
        image_origin = asset.static.get(name) if name else self._sprites[0]
        self.flattening = flattening if flattening else self.flattening

        # Verifica o tamanho
        if size:
            image_origin = pygame.transform.scale(image_origin, (size))

        # Verifica se precisa virar
        if flip:
                image_origin = pygame.transform.flip(image_origin, flip[0], flip[1])

        # Cria a imagem achatada
        image_small = pygame.transform.scale(
            image_origin, (image_origin.get_width(), image_origin.get_height() - self.flattening))

        surface_image_small = pygame.Surface(image_origin.get_size(), pygame.SRCALPHA)
        surface_image_small.blit(image_origin, (0, self.flattening))

        # Adiciona a image a uma coleção de animação
        self._sprites = [image_origin, surface_image_small]
        self.image = self._sprites[self.indexSprite]

        #Verifica se o quadrado possuia uma posição
        if self.rect:
            x, y = self.rect.topleft
        else:
            x, y = 0, 0
        self.rect = self._sprites[0].get_rect()
        self.rect.topleft = (x, y)



    def _updateAnimation(self):
        """Atualizadno as imagens"""
        if self.time.update():
            if self.indexSprite == 0:
                self.indexSprite = 1
            else:
                self.indexSprite = 0

            self.image = self._sprites[self.indexSprite]
