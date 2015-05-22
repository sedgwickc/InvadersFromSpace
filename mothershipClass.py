import pygame, sys


class MothershipSprite( pygame.sprite.Sprite ):
    # type of invader

    MOTHER_IMG = 'resources/mothership.png'
    START_Y = 30
    START_X = 0
    DAMAGE = 100

    def __init__( self, start_x):
        pygame.sprite.Sprite.__init__(self)
        # expand types
        self.src_image = pygame.image.load( self.MOTHER_IMG )
        self.rect = self.src_image.get_rect()
        self.image = self.src_image
        self.rect.x = start_x
        self.rect.y = self.START_Y

    def setPosition(self, new_x):
        self.rect.x = new_x

    def update(self, new_x):
        self.rect = self.image.get_rect()
        self.rect.x = new_x
        self.rect.y = self.START_Y
