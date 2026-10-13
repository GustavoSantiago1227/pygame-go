import pygame

class Tag:
    def __init__(self):
        self.tags = {}

    def add(self, name, sprite):
        """Adiciona o sprite a um group objetos"""
        if name not in self.tags:
            self.tags[name] = pygame.sprite.Group()
        self.tags[name].add(sprite)

    def update(self, *args, **kwargs):
        """Atualiza todos os grupos"""

        for group in self.tags.values():
            group.update(*args, **kwargs)

    def draw(self, surface):
        """Desenha todos os grupos na tela (útil para o seu método _draw do Game)"""
        for group in self.tags.values():
            group.draw(surface)

    def get(self, name):
        """Retorna o grupo (seja Single ou Tag) correspondente ao nome"""
        if name in self.tags:
            return self.tags[name]
        return None


class Unique:
    def __init__(self):
        self.tags = {}

    def add(self, name, sprite):
        """Adiciona o sprite a um group objetos"""
        if name not in self.tags:
            self.tags[name] = pygame.sprite.GroupSingle()
        self.tags[name].add(sprite)

    def update(self, *args, **kwargs):
        """Atualiza todos os grupos"""

        for group in self.tags.values():
            group.update(*args, **kwargs)

    def draw(self, surface):
        """Desenha todos os grupos na tela (útil para o seu método _draw do Game)"""
        for group in self.tags.values():
            group.draw(surface)

    def get(self, name):
        """Retorna o grupo (seja Single ou Tag) correspondente ao nome"""
        if name in self.tags:
            return self.tags[name]
        return None


tags = Tag()
unique = Unique()
