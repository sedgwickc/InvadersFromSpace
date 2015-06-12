import pygame, sys


class ShelterSprite( pygame.sprite.Sprite ):
    # type of invader

    SHELT_IMG = 'resources/shelter.png'
    SHELT_IMG_DAM = 'resources/shelter_damage.png'

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
        self.is_hit = False

    def hit(self, damage):
        self.image = pygame.image.load( ShelterSprite.SHELT_IMG_DAM )
        self.is_hit = True
        self.health -= damage

    def update(self):
        if self.is_hit == True:
            self.image = pygame.image.load( ShelterSprite.SHELT_IMG )
            self.is_hit = False
        
        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
