import pygame, sys


class ShelterSprite( pygame.sprite.Sprite ):
    # type of invader

    SHELT_IMG = 'resources/shelter.png'

    def __init__( self, start_x, start_y):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load( self.SHELT_IMG )
        self.rect = self.src_image.get_rect()
        self.image = self.src_image
        self.rect.x = start_x
        self.pos_x = start_x
        self.rect.y = start_y
        self.pos_y = start_y
        self.health = 100

    def update(self, damage):
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        self.health -= damage
