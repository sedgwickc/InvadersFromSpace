import pygame, sys


class BulletSprite( pygame.sprite.Sprite ):
    
    TURR_IMG = 'resources/bullet.png'
    INV_IMG = 'resources/bullet_alien.png'
    DAMAGE = 10

    def __init__( self, start_x, start_y, shooter):
        pygame.sprite.Sprite.__init__(self)
        if shooter == 'inv':
            self.src_image = pygame.image.load( self.INV_IMG )
        else:
            self.src_image = pygame.image.load( self.TURR_IMG )
        self.rect = self.src_image.get_rect()
        self.image = self.src_image
        self.rect.x = start_x
        self.cur_x = start_x
        self.rect.y = start_y
        self.cur_y = start_y
        self.shooter = shooter

    def update(self):
        self.rect = self.image.get_rect()
        if self.shooter == 'inv':
            self.cur_y += 4
        else:
            self.cur_y -= 8
        self.rect.y = self.cur_y
        self.rect.x = self.cur_x
