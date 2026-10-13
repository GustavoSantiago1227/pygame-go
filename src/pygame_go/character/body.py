import pygame


class Body:
    def __init__(self):
        """Caixas de colisão ou o corpo do sprite"""
        self.offSet = {
            'body': (0, 0),
            'hit': (0, 0),
            'hurt': (0, 0),
        }
        # Inicializa com rect padrão (caso a classe herdeira já tenha self.rect)
        base_rect = self.rect.copy()
        self.body = base_rect.copy()
        self.hit = base_rect.copy()
        self.hurt = base_rect.copy()
        self._updateBody()

    def setBody(self, x, y, w, h):
        """Define o retângulo e o deslocamento da caixa física principal"""
        self.body = pygame.Rect(0, 0, w, h)
        self.offSet['body'] = (x, y)

    def setHit(self, x, y, w, h):
        """Define o retângulo e o deslocamento da caixa de ataque (hitbox)"""
        self.hit = pygame.Rect(0, 0, w, h)
        self.offSet['hit'] = (x, y)

    def setHurt(self, x, y, w, h):
        """Define o retângulo e o deslocamento da caixa de dano (hurtbox)"""
        self.hurt = pygame.Rect(0, 0, w, h)
        self.offSet['hurt'] = (x, y)

    def _updateBody(self):
        """Atualiza as posições das caixas de colisão relativas ao topleft do sprite"""
        if not hasattr(self, 'rect'):
            return

        x, y = self.rect.topleft

        body_off = self.offSet.get('body', (0, 0))
        hit_off = self.offSet.get('hit', (0, 0))
        hurt_off = self.offSet.get('hurt', (0, 0))

        self.body.topleft = (x + body_off[0], y + body_off[1])
        self.hit.topleft = (x + hit_off[0], y + hit_off[1])
        self.hurt.topleft = (x + hurt_off[0], y + hurt_off[1])