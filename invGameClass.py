import pygame, sys, random
# import user defined classes
import invadersClass, turretClass, mothershipClass, shelterClass, bulletClass
# allows the use of pygame functions without the module suffix
from pygame.locals import *

class InvadersGame():
    #  class attributes

    # Window variables
    WIN_X = 800
    WIN_Y = 600

    # Invader variables
    INV_ROW = 5
    INV_COL = 11
    INV_LEFT = 175
    INV_TOP = 75
    INV_MAX = 55
    INV_MOVE_INTERVAL = 1000
    INV_FIRE_INTERVAL = 500
    INV_ALL = 55
    INV_MOST = 41
    INV_HALF = 26
    INV_SOME = 13
    INV_FEW = 5
    INV_X_MAX = 100
    INV_X_MIN = 700

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

    def __init__( self ):
        # intialize instance attributes

        # Set window size, title, and frame delay
        self.surfaceSize = (self.WIN_X, self.WIN_Y)
        self.frameDelay = 0.005

        self.inv_fire_interval = self.INV_FIRE_INTERVAL
        self.inv_move_interval = self.INV_MOVE_INTERVAL
        self.inv_right = True
        self.inv_left = False
        self.inv_down = False
        self.num_inv = 0
        self.inv_x = 50

        self.turr_pos = self.TURR_X
        self.turr_dir = self.TURR_STOP

        self.mother_x = 0
        self.motherActive = False
        
        self.player_lives = 3
        self.player_score = 0
        self.game_over = False
        self.player_win = False
        
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
        self.num_inv = self.INV_ALL

        # create invader bullet group
        self.inv_bullGrp = pygame.sprite.Group()

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
        self.mother_x = 0
        self.mothership = mothershipClass.MothershipSprite( self.mother_x )
        self.mothership_grp.add( self.mothership )
        self.motherActive = False

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

    def fireTurret(self):
        t_bull = bulletClass.BulletSprite( self.turret.rect.midtop[0], self.TURR_Y, 'tur' )
        self.t_bullGrp.add( t_bull )

    def fireInvader( self ):
        # randomly select an invader index and have that invader fire
        inv_list = self.invaders.sprites()
        inv_idx = random.randint( 0, len( inv_list ) - 1 )
        inv_bull = bulletClass.BulletSprite( inv_list[inv_idx].rect.x, inv_list[inv_idx].rect.y, 'inv' )
        self.inv_bullGrp.add( inv_bull )
    
    def getInvFireInterval(self):
        return self.inv_fire_interval

    def setInvFireInterval(self, new_interval):
        self.inv_fire_interval = new_interval

    def moveInvaders(self):
        self.moveInv = True

    def mothershipActivate(self):
        self.motherActive = True

    def mothershipStatus(self):
        return self.motherActive

    def update(self, surface):
        shelt_list = self.shelters.sprites()
        inv_list = self.invaders.sprites()
        mthr_list = self.mothership_grp.sprites()
        turret_list = self.turret_grp.sprites()
        winSurface = surface
        inv_count = len( inv_list )
        # if all shelters destroyed then user is told game is over and update
        # returns
        if len( self.shelters ) == 0:
            self.game_over = True
            self.player_win = False
            return

        # remove dead invaders and check if any have reached the shelters
        if inv_count > 0:
            for inv in inv_list:
                if inv.isAlive() == False:
                    self.invaders.remove( inv )
                    continue
                inv_idx = inv.rect.collidelist( shelt_list )
                if inv_idx != self.NO_COLLISION:
                    self.game_over = True
                    self.player_win = False
                    return
        else:
            self.game_over = True
            self.player_win = True
            return

        self.turret_grp.update( self.turr_dir )

        if inv_count < self.num_inv:
            # update interval between invader moves
            if inv_count <= self.INV_MOST and inv_count > self.INV_HALF:
                self.inv_move_interval = 500
            elif inv_count <= self.INV_HALF and inv_count > self.INV_SOME:
                self.inv_move_interval = 400
            elif inv_count <= self.INV_SOME and inv_count > self.INV_FEW:
                self.inv_move_interval = 200
            elif inv_count <= self.INV_FEW and inv_count > 5:
                self.inv_move_interval = 100
            elif inv_count <= 5:
                self.inv_move_interval = 50
            self.num_inv = inv_count

        # move invaders
        if self.moveInv == True: 
            if self.inv_down == True:
                for inv_spr in iter( self.invaders ):
                    inv_spr.rect.y += 10
                self.inv_down = False
                if self.inv_x  > 0:
                    self.inv_right = True
                    self.inv_left = False
                if self.inv_x <= 0:
                    self.inv_right = False
                    self.inv_left = True
            elif self.inv_left == True:
                for inv_spr in iter( self.invaders ):
                    inv_spr.rect.x -= 10
                self.inv_x -= 10
                if self.inv_x < -100:
                    self.inv_left = False
                    self.inv_right = False
                    self.inv_down = True
                    self.inv_x = 1
            elif self.inv_right == True:
                for inv_spr in iter( self.invaders ):
                    inv_spr.rect.x += 10
                self.inv_x += 10
                if self.inv_x > 100:
                    self.inv_left = False
                    self.inv_right = False
                    self.inv_down = True
                    self.inv_x = 0
            self.moveInv = False 

        # move mothership if it is still in window
        if self.motherActive == True :
            if len( self.mothership_grp ) == 0:
                self.mother_x = 0
                self.mothership.setPosition( self.mother_x )
                self.mothership_grp.add( self.mothership )
            else:
                self.mother_x += 3
                self.mothership_grp.update( self.mother_x )
                if self.mother_x >= self.WIN_X:
                    self.mother_x = 0
                    self.motherActive = False

        # if there were bullets on screen in last frame by then remove the bullets
        # that have left the screen and call the update method of the others
        if len( self.t_bullGrp ) > 0:
            for bull in iter( self.t_bullGrp ):
                if not winSurface.get_rect().contains( bull ):
                    self.t_bullGrp.remove( bull )
                # check if any turret bullets intersect with invaders
                for idx in bull.rect.collidelistall( inv_list ):
                    self.t_bullGrp.remove( bull )
                    inv_list[idx].explode()
                    self.player_score += inv_list[idx].damage
                # check if bullet intersects with the mothership
                mthr_idx = bull.rect.collidelist( mthr_list )
                if mthr_idx != self.NO_COLLISION:
                    self.t_bullGrp.remove( bull )
                    self.mothership_grp.remove( mthr_list[mthr_idx] )
                    self.motherActive = False
                    self.player_score += mothershipClass.MothershipSprite.DAMAGE
                # check if any turret bullets intersert with shelters
                for idx in bull.rect.collidelistall( shelt_list ): 
                    self.t_bullGrp.remove( bull )
                    shelt_list[idx].update(bull.DAMAGE)
                    if shelt_list[idx].health == 0:
                        self.shelters.remove( shelt_list[idx] )
            self.t_bullGrp.update()
        
        # check state of bullets fired by invaders and update them
        if len( self.inv_bullGrp ) > 0:
            for bull in iter( self.inv_bullGrp ):
                if not winSurface.get_rect().contains( bull ):
                    self.inv_bullGrp.remove( bull )
                # check if any invader bullets intersect with the turret
                for idx in bull.rect.collidelistall( turret_list ):
                    self.inv_bullGrp.remove( bull )
                    self.player_lives -= 1
                    if self.player_lives == 0:
                        self.game_over = True
                        self.player_win = False
                        return
                # check if any invader bullets intersert with shelters
                for idx in bull.rect.collidelistall( shelt_list ): 
                    self.inv_bullGrp.remove( bull )
                    shelt_list[idx].update(bull.DAMAGE)
                    if shelt_list[idx].health == 0:
                        self.shelters.remove( shelt_list[idx] )
            self.inv_bullGrp.update()
        
    def getSurfDim(self):
        return self.surfaceSize

    def getInvMoveInterval(self):
        return self.INV_MOVE_INTERVAL

    def getTurret(self):
        return self.turret_grp

    def getInvaders(self):
        return self.invaders

    def getShelters(self):
        return self.shelters

    def getTurretBullets(self):
        return self.t_bullGrp

    def getInvBullets(self):
        return self.inv_bullGrp

    def getMothership(self):
        return self.mothership_grp

    def getGameOver(self):
        return self.game_over

    def playerWon(self):
        return self.player_win

    def getFrameDelay(self):
        return self.frameDelay

    def getScore(self):
        return self.player_score

    def getLives(self):
        return self.player_lives
