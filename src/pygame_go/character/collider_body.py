import pygame


class Body:
    def __init__(self):
        """Caixas de colisão ou o corpo do sprite"""
        self.off_set = {
            'body': (0, 0),
            'hit': (0, 0),
            'hurt': (0, 0),
        }
        base_rect = self.rect.copy() if hasattr(self, 'rect') else pygame.Rect(0, 0, 32, 32)
        self.body = base_rect.copy()
        self.hit = base_rect.copy()
        self.hurt = base_rect.copy()
        self._updateBody()

    def setBody(self, x, y, w, h):
        self.body = pygame.Rect(0, 0, w, h)
        self.off_set['body'] = (x, y)

    def setHit(self, x, y, w, h):
        self.hit = pygame.Rect(0, 0, w, h)
        self.off_set['hit'] = (x, y)

    def setHurt(self, x, y, w, h):
        self.hurt = pygame.Rect(0, 0, w, h)
        self.off_set['hurt'] = (x, y)

    def _updateBody(self):
        if not hasattr(self, 'rect'):
            return

        x, y = self.rect.topleft
        body_off = self.off_set.get('body', (0, 0))
        hit_off = self.off_set.get('hit', (0, 0))
        hurt_off = self.off_set.get('hurt', (0, 0))

        self.body.topleft = (x + body_off[0], y + body_off[1])
        self.hit.topleft = (x + hit_off[0], y + hit_off[1])
        self.hurt.topleft = (x + hurt_off[0], y + hurt_off[1])


class BodyCollider(pygame.Rect):
    """
    Representa um bloco do cenário onde o retângulo visual (heridado de pygame.Rect)
    pode ser maior, mas possui uma sub-área de colisão (self.collider) deslocada por offset.
    """

    def __init__(self, x=0, y=0, w=0, h=0):
        super().__init__(x, y, w, h)

        # O offset e o retângulo interno de colisão
        self.off_set = (0, 0)
        self.collider = pygame.Rect(x, y, w, h)

        # Flags combináveis
        self.solid = True
        self.ceiling = True
        self.slab = False

    def setCollider(self, x, y, w, h):
        """Define o tamanho e o offset do colisor interno em relação ao rect principal do bloco"""
        self.off_set = (x, y)
        self.collider = pygame.Rect(self.x + x, self.y + y, w, h)

    def config(self, solid=True, ceiling=True, slab=False):
        """Configura o comportamento físico do colisor."""
        self.solid = solid
        self.ceiling = ceiling
        self.slab = slab

    def collider_body(self, sprite):
        """Verifica a colisão usando a sub-área `self.collider` do bloco."""
        hit_box = getattr(sprite, 'body', getattr(sprite, 'collider', getattr(sprite, 'rect', None)))

        if hit_box is None:
            return

        # Usa o `self.collider` (que tem o offset aplicado) para testar a colisão
        if not self.collider.colliderect(hit_box):
            return

        # Calcula as penetrações usando o `self.collider` do bloco
        dx_left = hit_box.right - self.collider.left
        dx_right = self.collider.right - hit_box.left
        dy_top = hit_box.bottom - self.collider.top
        dy_bottom = self.collider.bottom - self.collider.top

        min_x = min(dx_left, dx_right)
        min_y = min(dy_top, dy_bottom)

        # Tratamento vertical
        if min_y < min_x:
            if dy_bottom < dy_top:
                is_moving_up = getattr(sprite, 'in_jump', False) or getattr(sprite, 'gravity_current', 0) < 0
                if self.slab and is_moving_up:
                    return

                if self.solid:
                    hit_box.top = self.collider.bottom
                    if hasattr(sprite, 'jump_current'):
                        sprite.jump_current = 0
            else:
                if self.ceiling or self.solid:
                    hit_box.bottom = self.collider.top
                    if hasattr(sprite, 'onFloor'):
                        sprite.onFloor()
        else:
            # Tratamento horizontal
            if self.solid:
                if dx_left < dx_right:
                    hit_box.right = self.collider.left
                else:
                    hit_box.left = self.collider.right

        # Sincroniza o rect principal do sprite se ele usar Body com offset
        if hasattr(sprite, 'rect') and hasattr(sprite, 'off_set'):
            body_off = sprite.off_set.get('body', (0, 0))
            sprite.rect.topleft = (hit_box.x - body_off[0], hit_box.y - body_off[1])
            if hasattr(sprite, '_updateBody'):
                sprite._updateBody()
        elif hasattr(sprite, 'rect') and sprite.rect != hit_box:
            sprite.rect.topleft = hit_box.topleft

    def _updateCollider(self):
        """Atualiza a posição do colisor interno caso o bloco do cenário se mova"""
        self.collider.topleft = (self.x + self.off_set[0], self.y + self.off_set[1])


class Collider(pygame.Rect):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.off_set = (0, 0)
        self.collider = pygame.Rect(x, y, w, h)

    def _updateCollider(self):
        self.collider.topleft = (self.x + self.off_set[0], self.y + self.off_set[1])