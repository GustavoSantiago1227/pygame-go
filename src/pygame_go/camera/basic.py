import pygame
import math
from pygame_go.group import tags, unique


class Camera:
    def __init__(self, width, height, target=None, smooth=0.1):
        """Camera básica do jogo (recomendado para jogos com poucos sprites)"""
        self.groups = []
        self.target = target
        self.smooth = smooth

        self.x = 0.0
        self.y = 0.0

        self.rect = pygame.Rect(0, 0, width, height)

        self.width = width
        self.height = height

    def add_tags(self, *args):
        """Adiciona as tags para desenha na camera"""
        for name in args:
            self.groups.append(tags.get(name))

    def add_unique(self, *args):
        """Adiciona as tags para desenha na camera"""
        for name in args:
            self.groups.append(unique.get_group(name))


    def update(self):
        """Atualiza a camera"""
        if self.target is None:
            return

        target_x = self.target.centerx - self.width / 2
        target_y = self.target.centery - self.height / 2

        self.x += (target_x - self.x) * self.smooth
        self.y += (target_y - self.y) * self.smooth

        self.rect.topleft = (round(self.x), round(self.y))

    def draw(self, screen):
        """Desenha os sprites"""
        for group in self.groups:
            for sprite in group:
                if not self.rect.colliderect(sprite.rect):
                    continue

                screen.blit(
                    sprite.image,
                    (
                        round(sprite.rect.x - self.x),
                        round(sprite.rect.y - self.y)
                    )
                )