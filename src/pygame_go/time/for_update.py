class Timeout:
    def __init__(self, start=10, loop=False):
        """Configuração do temporizador"""
        self._start = start
        self.current = start
        self._loop = loop

    def set(self, start, loop, reset=False):
        self._start = start
        self._loop = loop
        if reset:
            self.current = self._start

    def update(self,):
        """Atualização do temporizador"""

        #Verifica se o temporizador encerrou
        if self.current == 0:
            if self._loop:
                self.current = self._start

            return True
        else:
            self.current -= 1
        return False