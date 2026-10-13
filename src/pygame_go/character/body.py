import pygame


class Body:
    def __init__(self, body=(0, 0), hit=(0, 0), hurt=(0, 0)):
        """Caixas de colisão ou o corpo do sprite"""
        self.off_set = {
            'body': body,
            'hit': hit,
            'hurt': hurt,
        }
        base_rect = self.rect.copy() if hasattr(self, 'rect') else pygame.Rect(0, 0, 32, 32)
        self._body = base_rect.copy()
        self._hit = base_rect.copy()
        self._hurt = base_rect.copy()

        self._update_body()

    @property
    def body(self):
        self._update_body()
        return self._body

    @body.setter
    def body(self, rect):
        """Configura um quadrado para o corpo"""
        x, y, w, h = rect
        self._body = pygame.Rect(0, 0, w, h)
        self.off_set['body'] = (x, y)

    @property
    def hit(self):
        """Retorna o ataque"""
        self._update_body()
        return self._hit
    @hit.setter
    def hit(self, rect):
        """Configura um quadrado para o hit"""
        x, y, w, h = rect
        self._hit = pygame.Rect(0, 0, w, h)
        self.off_set['hit'] = (x, y)

    @property
    def hurt(self):
        """Retorna o ataque"""
        self._update_body()
        return self._hurt

    @hurt.setter
    def hurt(self, rect):
        """Configura um quadrado para o ataque"""
        x, y, w, h = rect
        self._hurt = pygame.Rect(0, 0, w, h)
        self.off_set['hurt'] = (x, y)

    def _update_body(self):
        """Atualiza o corpo"""
        if not hasattr(self, 'rect'):
            return

        #Pega o off_set
        x, y = self.rect.topleft
        body_off = self.off_set.get('body', (0, 0))
        hit_off = self.off_set.get('hit', (0, 0))
        hurt_off = self.off_set.get('hurt', (0, 0))

        #Atualiza as posições
        self._body.topleft = (x + body_off[0], y + body_off[1])
        self._hit.topleft = (x + hit_off[0], y + hit_off[1])
        self._hurt.topleft = (x + hurt_off[0], y + hurt_off[1])