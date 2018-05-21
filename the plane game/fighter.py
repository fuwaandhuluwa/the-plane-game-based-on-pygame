import pygame

class Fighter(pygame.sprite.Sprite):
    collide_count = 0
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        pygame.init()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

pygame.quit()