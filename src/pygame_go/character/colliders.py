import pygame

class Collider:
    def __init__(self, x, y, w, h, floor=False):
        super().__init__(x, y, w, h)
        self.off_set = (0, 0)
        self.body = self.rect.copy()
        self.floor = floor

    def _updateCollider(self):
        self.body.topleft = (self.body.x + self.off_set[0], self.body.y + self.off_set[1])

    def collider(self, sprite):
        if self.body.colliderect(sprite.body):
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
