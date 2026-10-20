from pathlib import Path
import pygame


class Sound:

  def __init__(self):
    if not pygame.mixer.get_init():
      pygame.mixer.init()

    # Sua base configurada com pathlib
    self.base_directory = (Path.cwd() / "sound").resolve()
    self.base_directory.mkdir(parents=True, exist_ok=True)

    self.unique = {}
    self.group = {}

    self.vol = 1

  def set_vol(self, vol=1):
    """Seta o volume geral de todos os sons"""
    self.vol = vol

  def set_sound(self, data):
    """Recebe um dicionário com nome e o caminho do arquivo.

    Exemplo: {"tiro": "player/tiro.mp3", "pulo": "pulo.wav"}
    """
    for name, file in data.items():
      # Monta o caminho a partir da base_directory
      path = self.base_directory / file
      self.unique[name] = pygame.mixer.Sound(str(path))

    self.set_vol(self.vol)



  def set_group(self, data):
    """Recebe um dicionário onde a chave é o grupo e o valor é

    outro dicionário com os nomes e caminhos dos sons.
    Exemplo:
    {
        "passos": {
            "passo_1": "player/passo1.wav",
            "passo_2": "player/passo2.wav"
        }
    }
    """
    for name_group, sounds_group in data.items():
      if name_group not in self.group:
        self.group[name_group] = {}

      for name_sound, file in sounds_group.items():
        path = self.base_directory /  file
        self.group[name_group][name_sound] = pygame.mixer.Sound(str(path))

    for group in self.group.keys():
      self.set_vol_group(group, self.vol)


  def set_vol(self, sound, vol=1):
    """Seta o volume do som para o grupo"""
    if sound in self.unique:
      self.unique[sound].set_volume(vol)


  def play_sound(self, sound):
    """Toca um som individual pelo nome."""
    if sound in self.unique:
      self.unique[sound].play()


  def set_vol_group(self, group, vol=1):
    """Seta o volume do som para o grupo"""
    if group in self.group:
      for sound in self.group[group]:
        sound.set_volume(vol)

  def play_group(self, group, sound):
    """Escolhe e toca aleatoriamente um som de dentro do grupo."""
    if group in self.group:
      sounds = self.group[group]
      sounds[sound].play()

class Music:

  def __init__(self):
    if not pygame.mixer.get_init():
      pygame.mixer.init()

    # Sua base configurada com pathlib
    self.base_directory = (Path.cwd() / "sound").resolve()
    self.base_directory.mkdir(parents=True, exist_ok=True)

    self.playlist = {}
    self.vol = 1

  def set_vol(self, vol=1):
    """salva o volume padrão"""
    self.vol = 1

  def set(self, data):
    """Recebe um dicionário com nome e o caminho do arquivo.
    """
    for name, file in data.items():
      # Monta o caminho a partir da base_directory
      path = self.base_directory / file
      self.playlist[name] = path

  def play(self,name, loops=-1, vol=None):
    vol = vol if vol else self.vol
    pygame.mixer.music.load(str(self.playlist[name]))
    pygame.mixer.music.play(loops=loops)
    pygame.mixer.music.set_volume(vol)


sound = Sound()
music = Music()
