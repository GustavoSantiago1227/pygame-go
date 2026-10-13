import pygame


class Collider(pygame.Rect):
    def __init__(self, x=0, y=0, w=0, h=0, rect=None):
        if rect:
            x, y, w, h = rect
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