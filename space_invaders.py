'''
Charles Sedgwick
Invaders From Space
This script implements a game similar to space invaders
'''

import pygame, sys, random, time
# import user defined classes
import invadersClass, turretClass, mothershipClass, shelterClass, bulletClass
# allows the use of pygame functions without the module suffix
from pygame.locals import *

# User defined classes
# see invadersClass.py, turretClass.py, and mothership.py

# User-defined functions

def update():
    print( 'update' )
    return False

# Window variables
WIN_X = 800
WIN_Y = 600

# Invader variables
INV_ROW = 5
INV_COL = 11
INV_LEFT = 175
INV_TOP = 50
INV_MAX = 55

# turrent variables
TURR_X = 400
TURR_Y = 550
TURR_RIGHT = 1
TURR_NULL = 0
TURR_LEFT = -1

# bunker variables
SHELT_NUM = 4
SHELT_X = 125
SHELT_Y = 475
SHELT_DST = 150

# Set colours
BLACK = ( 0, 0, 0 )
WHITE = ( 255, 255, 255 )
RED = ( 255, 0, 0, )
GREEN = ( 0, 255, 0 )
BLUE = ( 0, 0, 255 )

NO_COLLISION = -1

# event definitions
USEREVENT_INV_DOWN = USEREVENT + 1
USEREVENT_MOTHERSHIP = USEREVENT_INV_DOWN + 1

# Main program

# initiliaze pygame
pygame.init()

# Set window size, title, and frame delay
surfaceSize = (WIN_X, WIN_Y)
windowTitle = 'Invaders From Space'
frameDelay = 0.005

# create window
windowSurface = pygame.display.set_mode( surfaceSize, 0, 32)
pygame.display.set_caption( windowTitle )

# set up font and text for lives and score count
basicFont = pygame.font.SysFont( None, 25 )
text_lives = basicFont.render( 'LIVES', True, WHITE, BLACK )
text_livesRect = text_lives.get_rect()
text_livesRect.topright = windowSurface.get_rect().topright
text_score = basicFont.render( 'SCORE', True, WHITE, BLACK )
text_scoreRect = text_score.get_rect()
text_scoreRect.topleft = windowSurface.get_rect().topleft

# create bunkers
shelters = pygame.sprite.Group()
cur_x = SHELT_X
for i in range( 0, SHELT_NUM ):
    cur_shelt = shelterClass.ShelterSprite( cur_x, SHELT_Y )
    shelters.add( cur_shelt )
    cur_x += SHELT_DST

# create invader sprites
invaders = pygame.sprite.Group()
cur_top = INV_TOP
for j in range ( 0, INV_ROW ):
    cur_left = INV_LEFT
    inv_row = []
    for i in range( 0, INV_COL ):
        cur_sprite = invadersClass.InvadersSprite(j, cur_left, cur_top )
        invaders.add( cur_sprite )
        cur_left += 40
    cur_top += 30
moveInv = False

# create invader bullet group

# create turret sprite
turret_grp = pygame.sprite.Group()
turret = turretClass.TurretSprite( (TURR_X, TURR_Y), (WIN_X, WIN_Y) )
turret_grp.add( turret )
turr_pos = TURR_X
moveRight = False
moveLeft = False

# create turret bullet group
t_bullGrp = pygame.sprite.Group()

# create mothership sprite
mothership_grp = pygame.sprite.Group()
mothership = mothershipClass.MothershipSprite( 0, 30 )
mothership_grp.add( mothership )
mother_pos = 0
mothership = False

# create timers that govern when invaders move and mothership appears
# can use the pygame.time.get_ticks() instead of timers for invader and
# mothership movement 
pygame.time.set_timer( USEREVENT_INV_DOWN, 1000 )
pygame.time.set_timer( USEREVENT_MOTHERSHIP, random.randint(5000, 10000) )

player_score = 0
turr_dir = TURR_NULL

# run the game loop
while True:
    
    inv_y = INV_LEFT

    # add abstraction of multiple games
    # create game over function 
    # if all shelters destroyed then user is told game is over and script exits
    if len( shelters ) == 0:
        basicFont = pygame.font.SysFont( None, 55 )
        text_go = basicFont.render( 'GAME OVER', True, RED, BLACK )
        text_goRect = text_go.get_rect()
        text_goRect.center = windowSurface.get_rect().center
        windowSurface.blit( text_go, text_goRect )
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        sys.exit()
    
    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                turr_dir = TURR_RIGHT
            if event.key == K_LEFT:
                turr_dir = TURR_LEFT
            if event.key == K_SPACE:
                t_bull = bulletClass.BulletSprite( turret.rect.midtop[0], TURR_Y )
                t_bullGrp.add( t_bull )
        if event.type == KEYUP:
            if event.key == K_RIGHT and turr_dir != TURR_LEFT:
                turr_dir = TURR_NULL
            if event.key == K_LEFT and turr_dir != TURR_RIGHT:
                turr_dir = TURR_NULL
        if event.type == USEREVENT_INV_DOWN:
            moveInv = True
        if event.type == USEREVENT_MOTHERSHIP:
            mothership = True
    
    turret_grp.update( turr_dir )

    if moveInv == True: 
        for inv_spr in iter( invaders ):
            inv_spr.rect.y += 5
        moveInv = False 

    if mothership == True and len( mothership_grp ) > 0:
        mother_pos += 1
        mothership_grp.update( mother_pos )
        if mother_pos >= WIN_X:
            mother_pos = 0
            mothership = False

    # randomly select an invader index and have that invader fire

    # if there were bullets on screen in last frame by then remove the bullets
    # that have left the screen and call the update method of the others
    shelt_list = shelters.sprites()
    inv_list = invaders.sprites()
    mthr_list = mothership_grp.sprites()
    if len( t_bullGrp ) > 0:
        for bull in iter( t_bullGrp ):
            if not windowSurface.get_rect().contains( bull ):
                t_bullGrp.remove( bull )
            # check if any turret bullets intersect with invaders
            for idx in bull.rect.collidelistall( inv_list ):
                t_bullGrp.remove( bull )
                invaders.remove( inv_list[idx] )
                # UPDATE SCORE!!
            # check if bullet intersects with the mothership
            mthr_idx = bull.rect.collidelist( mothership_grp.sprites() )
            if mthr_idx != NO_COLLISION:
                t_bullGrp.remove( bull )
                mothership_grp.remove( mthr_list[mthr_idx] )
                # UPDATE SCORE!!
            # check if any turret bullets intersert with shelters
            for idx in bull.rect.collidelistall( shelt_list ): 
                t_bullGrp.remove( bull )
                shelt_list[idx].update(bull.DAMAGE)
                if shelt_list[idx].HEALTH == 0:
                    shelters.remove( shelt_list[idx] )
        t_bullGrp.update()
        
    # draw frame
    windowSurface.fill( BLACK )
    windowSurface.blit( text_lives, text_livesRect )
    windowSurface.blit( text_score, text_scoreRect )
    # DRAW SCORE!!
    shelters.draw( windowSurface )
    invaders.draw( windowSurface )
    t_bullGrp.draw( windowSurface )
    turret_grp.draw( windowSurface )
    if mothership == True:
        mothership_grp.draw( windowSurface )

    time.sleep( frameDelay )
    # refresh display with new frame
    pygame.display.update()
