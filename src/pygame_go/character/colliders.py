import pygame

class Collider:
    def __init__(self, x=0, y=0):
        self.off_set = (x, y)
        self._body = self.rect.copy()
        self._update_collider()

    @property
    def body(self):
        """Retorna o corpo do colisor"""
        self._update_collider()
        return self._body

    @body.setter
    def body(self, rect):
        """Configura o tamanho do colisor"""
        x, y, w, h = rect
        self._body = pygame.Rect(0, 0, w, h)
        self.off_set = (x, y)


    def _update_collider(self):
        """Atualiza a posição do colisor"""
        self._body.topleft = (self.rect.x + self.off_set[0], self.rect.y + self.off_set[1])

    def collider(self, sprite):
        """Verifica a colisão"""
        if self.body.colliderect(sprite.body):
            return True
        else:
            return False


class Solid(Collider):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.body = self.rect.copy()

    def collider(self, sprite):
        """Verifica a colisão e expulsa o invasor do eixo correto"""
        # Pega a hitbox do sprite de forma segura

        # Verifica se há colisão com o body do Collider
        if not self.body.colliderect(sprite.body):
            return False

        horizontal, vertical = None, None
        if sprite.body.bottom > self.body.top:
            vertical = 'bottom'
            sprite.rect.bottom = self.body.top

        elif sprite.body.top < self.body.bottom:
            vertical = 'top'
            sprite.rect.top = self.body.bottom

        elif sprite.body.right > self.body.left:
            horizontal = 'right'
            sprite.rect.right = self.body.left

        elif sprite.body.left < self.body.right:
            horizontal = 'left'
            sprite.rect.left = self.body.right

        result = vertical if vertical else horizontal
        return result



