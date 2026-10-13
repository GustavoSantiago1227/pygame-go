import pygame


class BasicMoviment:
    def moveX(self, vel):
        """"Move o quadrado para os lados"""
        self.rect.x += vel

    def moveY(self, vel):
        """Move o quadradao para cima""""
        self.rect.y += vel

    def _corresponding_keys(self, keys, key_list):
        """Verifica se as teclas pressionadas correspondem à lista"""
        return any(keys[k] for k in key_list)

    def pressed_keys(self, keys):
        """Método base para sobrescrita"""
        pass


class Plataform(BasicMoviment):
    def __init__(self, left=None, right=None, jump=None,
                 speed=1, jump_force=1, gravity=False):
        super().__init__()

        def _parse_key(k, default):
            if k is None:
                return default
            return [k] if isinstance(k, int) else k

        # Teclas de ação
        self.k_left = _parse_key(left, [pygame.K_a, pygame.K_LEFT])
        self.k_right = _parse_key(right, [pygame.K_d, pygame.K_RIGHT])
        self.k_jump = _parse_key(jump, [pygame.K_SPACE])

        self.speed = speed
        self.jump_force = jump_force
        self.gravity_current = 0
        self.jump_current = jump_force
        self.fly = False
        self.in_jump = False

        if gravity:
            self.fly = True

    def pressed_keys(self, keys):
        """Recebe o keys do pygame.key.get_pressed()"""
        if self._corresponding_keys(keys, self.k_left):
            self.moveX(-self.speed)

        if self._corresponding_keys(keys, self.k_right):
            self.moveX(self.speed)

        if self._corresponding_keys(keys, self.k_jump) and not self.fly:
            self.in_jump = True

    def onFloor(self):
        """Está no chão"""
        self.fly = False
        self.in_jump = False
        self.jump_current = self.jump_force
        self.gravity_current = 0

    def onAir(self):
        """Está no ar"""
        self.fly = True

    def _updateMoviment(self):
        """Atualiza a movimentação física (gravidade/pulo)"""

        if self.fly:
            self.rect.y += self.gravity_current
            self.gravity_current += 1

        elif self.in_jump:
            if self.jump_current > 0:
                self.rect.y -= self.jump_current
                self.jump_current -= 1
            else:
                self.onAir()


class TopDown(BasicMoviment):
    def __init__(self, left=None, right=None, top=None, down=None, speed=1):
        super().__init__()

        def _parse_key(k, default):
            if k is None:
                return default
            return [k] if isinstance(k, int) else k

        self.k_left = _parse_key(left, [pygame.K_a, pygame.K_LEFT])
        self.k_right = _parse_key(right, [pygame.K_d, pygame.K_RIGHT])
        self.k_top = _parse_key(top, [pygame.K_w, pygame.K_UP])
        self.k_down = _parse_key(down, [pygame.K_s, pygame.K_DOWN])

        self.speed = speed

    def pressed_keys(self, keys):
        """Recebe o keys do pygame.key.get_pressed() com correção de velocidade diagonal"""
        dir_x = 0
        dir_y = 0

        # Coleta as direções (-1 para esquerda/cima, 1 para direita/baixo)
        if self._corresponding_keys(keys, self.k_left):
            dir_x -= 1
        if self._corresponding_keys(keys, self.k_right):
            dir_x += 1
        if self._corresponding_keys(keys, self.k_top):
            dir_y -= 1
        if self._corresponding_keys(keys, self.k_down):
            dir_y += 1

        # Se houver alguma tecla pressionada
        if dir_x != 0 or dir_y != 0:
            # Cria um vetor 2D com as direções
            movement = pygame.math.Vector2(dir_x, dir_y)

            # Normaliza o vetor (transforma o comprimento em 1, mantendo a proporção do ângulo)
            movement.normalize_ip()

            # Multiplica pela velocidade desejada
            movement *= self.speed

            # Aplica o movimento nos eixos
            self.moveX(movement.x)
            self.moveY(movement.y)

    def _updateMoviment(self):
        """Jogos Top-Down geralmente não precisam de lógica de gravidade por frame aqui"""
        pass