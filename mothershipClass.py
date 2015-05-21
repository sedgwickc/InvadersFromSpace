import pygame, sys

MOTHER_IMG = 'resources/mothership.png'

class MothershipSprite( pygame.sprite.Sprite ):
    # type of invader

    START_Y = 30
    START_X = 0
    damage = 100

    def __init__( self, start_x, start_y):
        pygame.sprite.Sprite.__init__(self)
        # expand types
        self.src_image = pygame.image.load( MOTHER_IMG )
        self.rect = self.src_image.get_rect()
        self.image = self.src_image
        self.rect.x = start_x
        self.START_X = start_x
        self.rect.y = start_y
        self.START_Y = start_y

    def update(self, new_x):
        self.rect = self.image.get_rect()
        self.rect.x = new_x
        self.rect.y = self.START_Y
