import pygame, sys


class TurretSprite( pygame.sprite.Sprite ):
    # type of invader

    TURR_IMG = 'resources/turret.png'
    TURR_WIDTH = 38
    TURR_SPEED = 2

    def __init__( self, start_pos, win_dim):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load( self.TURR_IMG )
        self.rect = self.src_image.get_rect()
        self.image = self.src_image
        self.rect.x = start_pos[0]
        self.turr_x = start_pos[0]
        self.rect.y = start_pos[1]
        self.turr_y = start_pos[1]
        self.win_dim = win_dim

    def update(self, direction):
        self.rect = self.image.get_rect()
        if direction == -1 and self.turr_x > 1:
            self.rect.x = self.turr_x - 2
            self.turr_x = self.rect.x
        elif direction == 1 and self.turr_x < self.win_dim[0] - self.TURR_SPEED - self.TURR_WIDTH:
            self.rect.x = self.turr_x + 2
            self.turr_x = self.rect.x
        else: # else player not pressing keypad keys 
            self.rect.x = self.turr_x
        
        self.rect.y = self.turr_y
