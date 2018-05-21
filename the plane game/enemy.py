import pygame
class Enemy(pygame.sprite.Sprite):
    collide_count = 0
    def __init__(self, image, position, speed, bgsize):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.position = position
        self.speed = speed
        self.rect = image.get_rect()
        self.rect.center = position
        self.bgsize = bgsize

    def move(self):
        self.rect = self.rect.move(self.speed)

        if self.rect.top > self.bgsize[1]:
            return False
        else:
            return True

pygame.quit()