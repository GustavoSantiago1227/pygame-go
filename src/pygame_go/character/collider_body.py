import pygame


class Body:
    def __init__(self):
        """Caixas de colisão ou o corpo do sprite"""
        self.off_set = {
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
        self.off_set['body'] = (x, y)

    def setHit(self, x, y, w, h):
        """Define o retângulo e o deslocamento da caixa de ataque (hitbox)"""
        self.hit = pygame.Rect(0, 0, w, h)
        self.off_set['hit'] = (x, y)

    def setHurt(self, x, y, w, h):
        """Define o retângulo e o deslocamento da caixa de dano (hurtbox)"""
        self.hurt = pygame.Rect(0, 0, w, h)
        self.off_set['hurt'] = (x, y)

    def _updateBody(self):
        """Atualiza as posições das caixas de colisão relativas ao topleft do sprite"""
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
    def __init__(self, x=0, y=0, w=0, h=0):
        self.off_set = (x, y)
        super().__init__(x, y, w, h)

        # Flags combináveis
        self.solid = True  # Lados sólidos e teto por padrão
        self.ceiling = True  # Funciona como chão no topo e avisa onFloor
        self.slab = False  # Permite atravessar de baixo para cima

    def config(self, solid=True, ceiling=True, slab=False):
        """Configura o comportamento misto/combinado do colisor."""
        self.solid = solid
        self.ceiling = ceiling
        self.slab = slab

    def collider_body(self, sprite):
        """
        Verifica a colisão usando o componente de corpo/colisor do sprite
        (ex: sprite.body ou sprite.collider) e ajusta a posição.
        """
        # Descobre qual retângulo do sprite usar para a colisão física
        # Prioriza sprite.body, depois sprite.collider, e por fim sprite.rect se não houver outro
        hit_box = getattr(sprite, 'body', getattr(sprite, 'collider', getattr(sprite, 'rect', None)))

        if hit_box is None:
            return

        # Se não há intersecção entre os retângulos, não faz nada
        if not self.colliderect(hit_box):
            return

        # Calcula as penetrações nos quatro lados usando o retângulo de colisão do sprite
        dx_left = hit_box.right - self.left
        dx_right = self.right - hit_box.left
        dy_top = hit_box.bottom - self.top
        dy_bottom = self.bottom - hit_box.top

        min_x = min(dx_left, dx_right)
        min_y = min(dy_top, dy_bottom)

        #Tratamento vertical
        if min_y < min_x:
            # Se bateu por baixo (tentando atravessar de baixo para cima)
            if dy_bottom < dy_top:
                # Se for slab e estiver subindo, ignora a colisão pelo fundo
                is_moving_up = getattr(sprite, 'in_jump', False)
                if self.slab and is_moving_up:
                    return

                # Se for sólido por baixo, bate a cabeça
                if self.solid:
                    hit_box.top = self.bottom

                    if hasattr(sprite, 'jump_current'):
                        sprite.jump_current = 0

            # Bateu por cima (caindo no topo)
            else:
                if self.ceiling or self.solid:
                    hit_box.bottom = self.top
                    if hasattr(sprite, 'onFloor'):
                        sprite.onFloor()
                    # Opcional: Se quiser que o rect principal acompanhe a hitbox
                    if hasattr(sprite, 'rect') and sprite.rect != hit_box:
                        sprite.rect.bottom = hit_box.bottom
                    return

        #Verificar horizontalmente
        else:
            if self.solid:
                if dx_left < dx_right:
                    hit_box.right = self.left  # Veio da esquerda
                else:
                    hit_box.left = self.right  # Veio da direita

        # Sincroniza o rect principal do sprite com o novo posicionamento da hitbox, se necessário
        if hasattr(sprite, 'rect') and sprite.rect != hit_box:
            # Mantém a proporção de centro ou alinha o topleft dependendo de como você estrutura
            sprite.rect.topleft = hit_box.topleft



class Collider(pygame.Rect): pass
