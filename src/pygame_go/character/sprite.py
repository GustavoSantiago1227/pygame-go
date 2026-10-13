import pygame
from pygame_go.manager.asset import asset
from pygame_go.time.for_update import Timeout


class Image(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.image = None
        self.rect = None
        self.updateImage(name)
        self.image = asset.static.get(name)
        self.rect = self.image.get_rect()

    def updateImage(self, name):
        self.image = asset.static.get(name)


class Flip(pygame.sprite.Sprite):
    def __init__(self, name, tick=10):
        """Criação de um sprite animado simples de poing"""
        super().__init__()
        self.image = None
        self.rect = None
        self._sprites = []
        self.indexSprite = 0
        self.time = Timeout(start=tick, loop=True)
        self.updateImage(name)
        self._updateAnimation()
        self.rect = self.image.get_rect()

    def updateImage(self, name):
        imageOrigin = asset.static.get(name)

        # Cria a imagem achatada
        imageSmall = pygame.transform.scale(
            imageOrigin, (imageOrigin.get_width(), imageOrigin.get_height() - 3))

        imageSmallSurface = pygame.Surface(imageOrigin.get_size(), pygame.SRCALPHA)
        imageSmallSurface.blit(imageSmall, (0, 3))

        # Prepara a imagem normal e achatada
        self._sprites = [imageOrigin, imageSmallSurface]
        self.image = self._sprites[self.indexSprite]

    def _updateAnimation(self):
        """Atualizadno as imagens"""
        if self.time.update():
            if self.indexSprite == 0:
                self.indexSprite = 1
            else:
                self.indexSprite = 0

            self.image = self._sprites[self.indexSprite]
