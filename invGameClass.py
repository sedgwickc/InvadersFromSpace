import pygame, sys
# import user defined classes
import invadersClass, turretClass, mothershipClass, shelterClass, bulletClass
# allows the use of pygame functions without the module suffix
from pygame.locals import *

class InvadersGame( ):
    # Window variables
    WIN_X = 800
    WIN_Y = 600

    # Invader variables
    INV_ROW = 5
    INV_COL = 11
    INV_LEFT = 175
    INV_TOP = 50
    INV_MAX = 55
    INV_INTERVAL = 1000

    # turrent variables
    TURR_X = 400
    TURR_Y = 550
    TURR_RIGHT = 1
    TURR_STOP = 0
    TURR_LEFT = -1

    # bunker variables
    SHELT_NUM = 4
    SHELT_X = 125
    SHELT_Y = 475
    SHELT_DST = 150

    # Mothership constants
    MTHR_MIN = 5000
    MTHR_MAX = 10000

    NO_COLLISION = -1

    # Set window size, title, and frame delay
    surfaceSize = (WIN_X, WIN_Y)
    frameDelay = 0.005

    shelters = []
    invaders = []
    turret_grp = []
    t_bullGrp = []
    mothership_grp = []

    moveInv = False

    turret = 0

    turr_pos = TURR_X
    turr_dir = TURR_STOP
    moveRight = False
    moveLeft = False

    mother_pos = 0
    mothership = False
    
    player_score = 0
    game_over = False

    def __init__( self ):
        # create bunkers
        self.shelters = pygame.sprite.Group()
        cur_x = self.SHELT_X
        for i in range( 0, self.SHELT_NUM ):
            cur_shelt = shelterClass.ShelterSprite( cur_x, self.SHELT_Y )
            self.shelters.add( cur_shelt )
            cur_x += self.SHELT_DST

        # create invader sprites
        self.invaders = pygame.sprite.Group()
        cur_top = self.INV_TOP
        for j in range ( 0, self.INV_ROW ):
            cur_left = self.INV_LEFT
            inv_row = []
            for i in range( 0, self.INV_COL ):
                cur_sprite = invadersClass.InvadersSprite(j, cur_left, cur_top )
                self.invaders.add( cur_sprite )
                cur_left += 40
            cur_top += 30
        self.moveInv = False

        # create invader bullet group

        # create turret sprite
        self.turret_grp = pygame.sprite.Group()
        self.turret = turretClass.TurretSprite( (self.TURR_X, self.TURR_Y), (self.WIN_X, self.WIN_Y) )
        self.turret_grp.add( self.turret )
        self.turr_pos = self.TURR_X
        self.moveRight = False
        self.moveLeft = False

        # create turret bullet group
        self.t_bullGrp = pygame.sprite.Group()

        # create mothership sprite
        self.mothership_grp = pygame.sprite.Group()
        mothership = mothershipClass.MothershipSprite( 0, 30 )
        self.mothership_grp.add( mothership )
        self.mother_pos = 0
        self.mothership = False

    def moveTurretRight(self):
        self.turr_dir = self.TURR_RIGHT

    def moveTurretLeft(self):
        self.turr_dir = self.TURR_LEFT

    def stopTurret(self):
        self.turr_dir = self.TURR_STOP

    def turretMovingRight(self):
        if self.turr_dir == self.TURR_RIGHT:
            return True
        else:
            return False

    def turretMovingLeft(self):
        if self.turr_dir == self.TURR_LEFT:
            return True
        else:
            return False

    def turretStopped(self):
        if self.turr_dir == self.TURR_STOP:
            return True
        else:
            return False

    def getSurfDim(self):
        return self.surfaceSize

    def getInvInterval(self):
        return self.INV_INTERVAL

    def getTurret(self):
        return self.turret_grp

    def getInvaders(self):
        return self.invaders

    def getShelters(self):
        return self.shelters

    def getTurretBullets(self):
        return self.t_bullGrp

    def getMothership(self):
        return self.mothership_grp

    def getGameOver(self):
        return self.game_over

    def getFrameDelay(self):
        return self.frameDelay

    def fireTurret(self):
        t_bull = bulletClass.BulletSprite( self.turret.rect.midtop[0], self.TURR_Y )
        self.t_bullGrp.add( t_bull )

    def activateMothership(self):
        self.mothership == True

    def moveInvaders(self):
        self.moveInv = True

    def motherActive(self):
        return self.mothership

    def update(self, surface):
        
        # if all shelters destroyed then user is told game is over and update
        # returns
        if len( self.shelters ) == 0:
            text_overRect.center = self.winSurface.get_rect().center
            self.game_over = True

        self.turret_grp.update( self.turr_dir )

        if self.moveInv == True: 
            for inv_spr in iter( self.invaders ):
                inv_spr.rect.y += 5
            self.moveInv = False 

        if self.mothership == True and len( self.mothership_grp ) > 0:
            self.mother_pos += 1
            self.mothership_grp.update( self.mother_pos )
            if mother_pos >= WIN_X:
                self.mother_pos = 0
                self.mothership = False

        # randomly select an invader index and have that invader fire

        # if there were bullets on screen in last frame by then remove the bullets
        # that have left the screen and call the update method of the others
        shelt_list = self.shelters.sprites()
        inv_list = self.invaders.sprites()
        mthr_list = self.mothership_grp.sprites()
        winSurface = surface
        if len( self.t_bullGrp ) > 0:
            for bull in iter( self.t_bullGrp ):
                if not winSurface.get_rect().contains( bull ):
                    self.t_bullGrp.remove( bull )
                # check if any turret bullets intersect with invaders
                for idx in bull.rect.collidelistall( inv_list ):
                    self.t_bullGrp.remove( bull )
                    self.invaders.remove( inv_list[idx] )
                    self.player_score += 10
                # check if bullet intersects with the mothership
                mthr_idx = bull.rect.collidelist( mthr_list )
                if mthr_idx != self.NO_COLLISION:
                    self.t_bullGrp.remove( bull )
                    self.mothership_grp.remove( mthr_list[mthr_idx] )
                    self.player_score += 100
                # check if any turret bullets intersert with shelters
                for idx in bull.rect.collidelistall( shelt_list ): 
                    self.t_bullGrp.remove( bull )
                    shelt_list[idx].update(bull.DAMAGE)
                    if shelt_list[idx].HEALTH == 0:
                        self.shelters.remove( shelt_list[idx] )
            self.t_bullGrp.update()
