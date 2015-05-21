import pygame, sys

RES_DIR = 'resources/'
ALIEN_IMGS = [ 'alien_5.png', 'alien_4.png', 'alien_3.png', 'alien_1.png', 'alien_1.png' ]
DAMAGE = [ 40, 30, 20, 10, 10 ]
EXPLODE_IMG = 'explosion_inv.jpg'

class InvadersSprite( pygame.sprite.Sprite ):
    
    alien_type = 0    
    damage = 0
    alive = True

    def __init__( self, inv_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.alien_type = inv_type
        # set type and damage 
        if inv_type <= len( ALIEN_IMGS ):
            self.src_image = pygame.image.load( RES_DIR + ALIEN_IMGS[inv_type] )
            self.damage = DAMAGE[ inv_type ]
        else:
            self.src_image = pygame.image.load( RES_DIR + ALIEN_IMGS[0] ) 
            self.damage = DAMAGE[0]

        self.rect = self.src_image.get_rect()
        self.image = self.src_image
        self.rect.x = x
        self.rect.y = y
        self.alive = True
    
    def isAlive(self):
        return self.alive

    def explode(self):
        self.image = pygame.image.load( RES_DIR + EXPLODE_IMG )
        self.alive = False

    def update(self):
        self.rect = self.image.get_rect()
