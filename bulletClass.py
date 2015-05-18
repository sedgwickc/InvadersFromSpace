import pygame, sys

BULLET_IMG = 'resources/bullet.png'

class BulletSprite( pygame.sprite.Sprite ):
    # type of invader

    CUR_X = 0
    CUR_Y = 0
    DAMAGE = 10

    def __init__( self, start_x, start_y):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load( BULLET_IMG )
        self.rect = self.src_image.get_rect()
        self.image = self.src_image
        self.rect.x = start_x
        self.CUR_X = start_x
        self.rect.y = start_y
        self.CUR_Y = start_y

    def update(self):
        self.rect = self.image.get_rect()
        self.CUR_Y -= 3
        self.rect.y = self.CUR_Y
        self.rect.x = self.CUR_X
