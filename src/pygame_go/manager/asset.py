
from pathlib import Path
import pygame


class Asset:
    def __init__(self):
        """Gerencia imagens e animações do jogo."""

        self.static = {}
        self.animation = {}

        self._cache = {}

        # Diretório asset na raiz do projeto.
        self.base_directory = (Path.cwd() / "asset").resolve()
        self.base_directory.mkdir(parents=True, exist_ok=True)

    def _get_path(self, relative_path):
        """Retorna o caminho validado de um arquivo dentro de asset/."""

        path = (self.base_directory / relative_path).resolve()

        try:
            path.relative_to(self.base_directory)
        except ValueError:
            raise ValueError(
                f"O arquivo precisa estar dentro de asset/: {relative_path}"
            ) from None

        return path

    def _load_image(self, relative_path):
        """Carrega uma imagem uma única vez e reutiliza o cache."""

        path = self._get_path(relative_path)
        cache_key = str(path)

        # Reutiliza a imagem caso já tenha sido carregada.
        if cache_key in self._cache:
            return self._cache[cache_key]

        if not pygame.display.get_init() or pygame.display.get_surface() is None:
            raise RuntimeError(
                "Inicialize a janela do Pygame antes de carregar imagens."
            )

        if not path.is_file():
            raise FileNotFoundError(
                f"Arquivo de imagem não encontrado: {path}"
            )

        try:
            image = pygame.image.load(str(path)).convert_alpha()
        except pygame.error as error:
            raise RuntimeError(
                f"Não foi possível carregar a imagem: {path}"
            ) from error

        self._cache[cache_key] = image

        return image

    def set_image(self, data: dict):
        """
        Registra imagens estáticas.

        Exemplo:
        {
            "player": "images/player.png",
            "enemy": "images/enemy.png"
        }
        """

        for name, relative_path in data.items():
            self.static[name] = self._load_image(relative_path)

    def set_frames(self, data: dict):
        """
        Registra sequências de imagens para animações.

        Exemplo:
        {
            "run": [
                "animations/run_1.png",
                "animations/run_2.png"
            ]
        }
        """

        for name, path_list in data.items():
            self.animation[name] = [
                self._load_image(path)
                for path in path_list
            ]

    def get_image(self, name):
        """Retorna uma imagem estática registrada."""

        try:
            return self.static[name]
        except KeyError:
            raise KeyError(
                f"Imagem estática não registrada: {name}"
            ) from None

    def get_frames(self, name):
        """Retorna os quadros de uma animação registrada."""

        try:
            return self.animation[name]
        except KeyError:
            raise KeyError(
                f"Animação não registrada: {name}"
            ) from None

    def clear(self):
        """Limpa os registros e o cache de imagens."""

        self.static.clear()
        self.animation.clear()
        self._cache.clear()
