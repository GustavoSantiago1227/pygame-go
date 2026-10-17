import pygame


class _BaseGroupManager:
    """Classe base genérica para gerenciar coleções de grupos do Pygame."""
    def __init__(self, group_type):
        self.tags = {}
        self._group_type = group_type  # pygame.sprite.Group ou GroupSingle

    def add(self, name, sprite):
        """Adiciona o sprite a um grupo com base no nome."""
        if name not in self.tags:
            self.tags[name] = self._group_type()
        self.tags[name]._add_internal_font(sprite)

    def update(self, *args, **kwargs):
        """Atualiza todos os grupos gerenciados."""
        for group in self.tags.values():
            group.update(*args, **kwargs)

    def draw(self, surface):
        """Desenha todos os grupos na tela."""
        for group in self.tags.values():
            group.draw(surface)

    def get(self, name):
        """Retorna o grupo correspondente ao nome."""
        return self.tags.get(name)

    def reset(self, name=None):
        """
        Esvazia os sprites dos grupos, mantendo as tags no dicionário.
        - Se passar um 'name', esvazia apenas os sprites daquele grupo específico.
        - Se não passar nada, esvazia os sprites de todos os grupos, mas preserva as chaves.
        """
        if name:
            if name in self.tags:
                self.tags[name].empty()
        else:
            for group in self.tags.values():
                group.empty()


class Tag(_BaseGroupManager):
    def __init__(self):
        super().__init__(pygame.sprite.Group)


class Unique(_BaseGroupManager):
    def __init__(self):
        super().__init__(pygame.sprite.GroupSingle)

    def get(self, name):
        """Retorna o sprite do grupo."""
        return list(self.tags.get(name))[0]

    def get_group(self, name):
        """Retorna grupo do sprite"""
        return self.tags.get(name)


# Instâncias globais prontas para uso
tags = Tag()
unique = Unique()


