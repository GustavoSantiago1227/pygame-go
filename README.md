# pygame-go

Biblioteca Python criada para facilitar o desenvolvimento de jogos utilizando Pygame.

## Requisitos

* Python 3.10 ou superior.

## Instalação

```bash
python -m pip install .
```

## Inicializar um projeto

Na pasta em que deseja criar seu projeto, execute:

```bash
pygame-go-init
```

O comando cria as pastas básicas e um arquivo `main.py` inicial.

## Exemplo de uso

```python
from pygame_go.game_loop.basic import Game

game = Game(
    title="Meu Jogo",
    width=800,
    height=600,
    fps=60,
)

game.run()
```
