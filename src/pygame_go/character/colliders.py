import pygame

class Collider:
    def __init__(self, x=0, y=0, floor=False):
        self.off_set = (x, y)
        self._body = self.rect.copy()
        self.floor = floor
        self._update_collider()

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, rect):
        x, y, w, h = rect
        self._body = pygame.Rect(0, 0, w, h)
        self.off_set = (x, y)


    def _update_collider(self):
        self._body.topleft = (self.rect.x + self.off_set[0], self.rect.y + self.off_set[1])

    def collider(self, sprite):
        if self._body.colliderect(sprite.body):
            if self.floor:
                if hasattr(sprite, 'on_floor'):
                    sprite.on_floor()
            return True
        else:
            return False

"""
class Block(Collider):
    def collider(self, sprite):
        if self.body.colliderect(sprite.body):
            if self.floor:
                if hasattr(sprite, 'on_floor'):
                    sprite.on_floor()
                    
            #Verifica colisão vertical
            if sprite.body.bottom >= self.body.top:
                sprite.rect.top = self.body.top
            
            if sprite bod
            return True
        else:
            return False
"""
