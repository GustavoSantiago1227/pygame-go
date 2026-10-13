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

    def collider(self, sprite):
        """Resolve a colisão e retorna o lado do impacto."""

        body = self.body
        target = sprite.body

        if not body.colliderect(target):
            return False

        # Calcula a sobreposição nos dois eixos
        overlap_x = min(body.right, target.right) - max(body.left, target.left)
        overlap_y = min(body.bottom, target.bottom) - max(body.top, target.top)

        # Resolve a colisão pelo eixo de menor sobreposição
        if overlap_x < overlap_y:
            if target.centerx < body.centerx:
                sprite.rect.right = body.left
                result = 'right'
            else:
                sprite.rect.left = body.right
                result = 'left'

        else:
            if target.centery < body.centery:
                sprite.rect.bottom = body.top
                result = 'bottom'
            else:
                sprite.rect.top = body.bottom
                result = 'top'

        # Sincroniza a hitbox com o rect corrigido
        sprite.body.center = sprite.rect.center

        return result



class Floor(Solid):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)

    def collider(self, sprite):
        """Resolve a colisão e retorna o lado do impacto."""
        result = super().collider(sprite)
        if result == 'bottom' and hasattr(sprite, 'on_floor'):
            sprite.on_floor()
        return result



