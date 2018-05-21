import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, position, speed = [0, 0], bg_size = [0, 0]):
        pygame.sprite.Sprite.__init__(self)
        pygame.init()
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.center = position
        self.bg_size = bg_size

    def move(self):
        self.rect = self.rect.move(self.speed)

        if self.rect.top < 0 or self.rect.top > self.bg_size[1] - self.rect.height:
            return False
        else:
            return True



