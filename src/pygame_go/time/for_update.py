class Timeout:
    def __init__(self, start=10, loop=False):
        """Configuração do temporizador"""
        self.start = start
        self.current = start
        self.loop = loop

    def set(self, start=None, loop=None, reset=False):
        self.start = start if start else self.start
        self.loop = loop if loop else self.loop
        if reset:
            self.current = self.start

    def update(self,):
        """Atualização do temporizador"""

        #Verifica se o temporizador encerrou
        if self.current == 0:
            if self.loop:
                self.current = self.start

            return True
        else:
            self.current -= 1
        return False