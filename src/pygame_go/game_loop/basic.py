import pygame


class Game:
    def __init__(
        self,
        title="game",
        width=800,
        height=600,
        fullscreen=False,
        fps=30,
        debug=True,
        screen_color=(0, 0, 0)
    ):
        """Inicializa o jogo."""

        if fps <= 0:
            raise ValueError("FPS deve ser maior que zero.")

        if not fullscreen and (width <= 0 or height <= 0):
            raise ValueError(
                "A largura e a altura devem ser maiores que zero."
            )

        pygame.init()

        if fullscreen:
            self.screen = pygame.display.set_mode(
                (0, 0),
                pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode((width, height))

        self.WIDTH, self.HEIGHT = self.screen.get_size()

        pygame.display.set_caption(title)

        # Controle de FPS
        self.clock = pygame.time.Clock()
        self.FPS = fps

        # Cenas
        self._scenes = {}
        self._current = None

        # Configurações
        self.debug = debug
        self.screen_color = screen_color

        # Estado do jogo
        self.running = False

    def set_scene(self, scenes: dict):
        """Registra as cenas disponíveis."""

        self._scenes.update(scenes)

    def load(self, name):
        """Carrega uma cena registrada."""

        if name not in self._scenes:
            raise ValueError(f"Cena não registrada: {name}")

        scene = self._scenes[name](
            self.load,
            self.close,
            self.WIDTH,
            self.HEIGHT
        )

        self._current = scene

    def _update(self):
        """Atualiza a cena atual."""

        if self._current:
            self._current.update()

    def _keyboard_mouse(self):
        """Envia o estado do teclado e do mouse à cena."""

        if self._current:
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()

            self._current.keyboard_mouse(
                keys,
                mouse_pos,
                mouse_buttons
            )

    def _events(self):
        """Processa os eventos do Pygame."""

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.close()
                break

            if (
                self.debug
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                self.close()
                break

            if self._current:
                self._current.events(event)

            if not self.running:
                break
    def _draw(self):
        """Desenha a cena atual."""

        self.screen.fill(self.screen_color)

        if self._current:
            self._current.draw(self.screen)

    def close(self):
        """Solicita o encerramento do jogo."""

        self.running = False

    def run(self):
        """Executa o loop principal."""

        if self.running:
            raise RuntimeError("O jogo já está em execução.")

        self.running = True

        try:
            while self.running:
                self._keyboard_mouse()
                self._events()

                if not self.running:
                    break

                self._update()
                self._draw()

                pygame.display.flip()
                self.clock.tick(self.FPS)

        finally:
            self.running = False
            pygame.quit()
