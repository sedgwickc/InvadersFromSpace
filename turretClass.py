import pygame, sys

TURR_IMG = 'resources/turret.png'

class TurretSprite( pygame.sprite.Sprite ):
    # type of invader

    START_Y = 0
    START_X = 0
    WIN_DIM = ( 0, 0 )
    TURR_WIDTH = 38
    TURR_X = 0
    TURR_SPEED = 2

    def __init__( self, start_pos, win_dim):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load( TURR_IMG )
        self.rect = self.src_image.get_rect()
        self.image = self.src_image
        self.rect.x = start_pos[0]
        self.START_X = start_pos[0]
        self.TURR_X = self.START_X
        self.rect.y = start_pos[1]
        self.START_Y = start_pos[1]
        self.WIN_DIM = win_dim

    def update(self, direction):
        self.rect = self.image.get_rect()
        if direction == -1 and self.TURR_X > 1:
            self.rect.x = self.TURR_X - 2
            self.TURR_X = self.rect.x
        elif direction == 1 and self.TURR_X < self.WIN_DIM[0] - self.TURR_SPEED - self.TURR_WIDTH:
            self.rect.x = self.TURR_X + 2
            self.TURR_X = self.rect.x
        else: # else player not pressing keypad keys 
            self.rect.x = self.TURR_X
        
        self.rect.y = self.START_Y
