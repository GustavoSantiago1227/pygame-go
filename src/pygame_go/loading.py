from pathlib import Path

def loading(root_path=None):
    """Cria a estrutura inicial de um projeto Pygame."""


    base_dir = Path(root_path or Path.cwd()).resolve()

    # Pastas principais do projeto
    directories = [
        "asset",
        "sounds",
        "script",
        "factory",
    ]

    for directory in directories:
        (base_dir / directory).mkdir(parents=True, exist_ok=True)

    # Arquivo principal do jogo
    main_file = base_dir / "main.py"

    main_content = '''from pygame_go.game_loop.basic import Game
```
    
def main():
game = Game(
title="Meu Jogo",
width=1280,
height=720,
fullscreen=False,
fps=60,
debug=True,
screen_color=(30, 30, 40),
)


game.run()


if **name** == "**main**":
main()
    '''

    if not main_file.exists():
        main_file.write_text(main_content, encoding="utf-8")
        print("Arquivo criado: main.py")
    else:
        print("Arquivo já existe, mantido: main.py")

    print(f"Projeto preparado em: {base_dir}")

    return base_dir

def main():
    loading()

if __name__ == "__main__":
    main()
