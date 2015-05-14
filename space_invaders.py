'''
Charles Sedgwick
Invaders From Space
This script implements a game similar to space invaders
'''

import pygame, sys, random
# import user defined classes
import invadersClass, turretClass, mothershipClass, shelterClass
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

# width of the turret image
TURR_WIDTH = 64

# event definitions
USEREVENT_INV_DOWN = USEREVENT + 1
USEREVENT_MOTHERSHIP = USEREVENT_INV_DOWN + 1

# Main program

# initiliaze pygame
pygame.init()

# Set window size, title, and frame delay
surfaceSize = (WIN_X, WIN_Y)
windowTitle = 'Invaders From Space'
frameDelay = 0.02

# create window
windowSurface = pygame.display.set_mode( surfaceSize, 0, 32)
pygame.display.set_caption( windowTitle )

# set up font and text
basicFont = pygame.font.SysFont( None, 25 )
text = basicFont.render( 'LIVES', True, WHITE, BLACK )
textRect = text.get_rect()
textRect.topleft = windowSurface.get_rect().topleft

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
inv_spr = invaders.sprites()

# create turret
turret_grp = pygame.sprite.Group()
turret = turretClass.TurretSprite(TURR_X, TURR_Y)
turret_grp.add( turret )
turr_pos = TURR_X
moveRight = False
moveLeft = False

# create mothership
mothership_grp = pygame.sprite.Group()
mothership = mothershipClass.MothershipSprite( 0, 30 )
mothership_grp.add( mothership )
mother_pos = 0
mothership = False

# create timers that govern when invaders move and mothership appears
pygame.time.set_timer( USEREVENT_INV_DOWN, 1000 )
pygame.time.set_timer( USEREVENT_MOTHERSHIP, random.randint(5000, 10000) )

game_over = False

# run the game loop
while not game_over:
    
    inv_y = INV_LEFT
    
    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            game_over = True
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moveRight = True
                moveLeft = False
            if event.key == K_LEFT:
                moveRight = False
                moveLeft = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moveRight = False
            if event.key == K_LEFT:
                moveLeft = False
        if event.type == USEREVENT_INV_DOWN:
            moveInv = True
        if event.type == USEREVENT_MOTHERSHIP:
            mothership = True
    
    if moveLeft and turr_pos > 0:
        turr_pos -= 2
        turret_grp.update( turr_pos )
    if moveRight and turr_pos < WIN_X - TURR_WIDTH:
        turr_pos += 2
        turret_grp.update( turr_pos )
    
    if moveInv == True: 
        for i in range( 0, INV_MAX ):
            inv_spr[i].rect.y += 5
        moveInv = False

    if mothership == True:
        mother_pos += 1
        mothership_grp.update( mother_pos )
        if mother_pos >= WIN_X:
            mother_pos = 0
            mothership = False
   
    # draw frame
    windowSurface.fill( BLACK )
    windowSurface.blit( text, textRect )
    shelters.draw( windowSurface )
    invaders.draw( windowSurface )
    turret_grp.draw( windowSurface )
    if mothership == True:
        mothership_grp.draw( windowSurface )

    # refresh display with new frame
    pygame.display.update()

pygame.quit()
sys.exit()
