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

        # Calcula as penetrações nos quatro lados
        dx_left = sprite.body.right - self.body.left
        dx_right = self.body.right - sprite.body.left
        dy_top = sprite.body.bottom - self.body.top
        dy_bottom = self.body.bottom - sprite.body.top

        min_x = min(dx_left, dx_right)
        min_y = min(dy_top, dy_bottom)

        move_x, move_y = 0, 0

        # Decide se resolve no Eixo Vertical ou Horizontal com base na menor penetração
        if min_y < min_x:
            if dy_bottom < dy_top:
                # Bateu a cabeça por baixo
                sprite.body.top = self.body.bottom
                vertical = 'top'
                move_y = dy_top
            else:
                # Caiu em cima (chão)
                sprite.body.bottom = self.body.top
                vertical = 'bottom'
                move_y = -dy_bottom
            horizontal = None
        else:
            if dx_left < dx_right:
                # Bateu na lateral esquerda do bloco
                sprite.body.right = self.body.left
                horizontal = 'right'
                move_x = -dx_right
            else:
                # Bateu na lateral direita do bloco
                sprite.body.left = self.body.right
                horizontal = 'left'
                move_x = dx_left
            vertical = None

        #Move sprite
        sprite.rect.y += move_y
        sprite.rect.x += move_x

        return (horizontal, vertical)

