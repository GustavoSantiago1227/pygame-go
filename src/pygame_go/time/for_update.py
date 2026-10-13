class Timeout:
    def __init__(self, start=10, loop=False):
        """Configuração do temporizador"""
        self._start = start
        self.current = start
        self._loop = loop

    def update(self, callback=None, *args, **kwargs):
        """Atualização do temporizador"""

        #Verifica se o temporizador encerrou
        if self.current == 0:
            if self._loop:
                self.current = self._start

            if callback:
                callback(*args, **kwargs)
            return True
        else:
            self.current -= 1
        return False