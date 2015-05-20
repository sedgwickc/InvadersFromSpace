'''
Charles Sedgwick
Invaders From Space
This script implements a game similar to space invaders using the spaceInvClass
'''

import pygame, sys, random, time
# import user defined classes
import invGameClass
# allows the use of pygame functions without the module suffix
from pygame.locals import *

# Set colours
BLACK = ( 0, 0, 0 )
WHITE = ( 255, 255, 255 )
RED = ( 255, 0, 0, )
GREEN = ( 0, 255, 0 )
BLUE = ( 0, 0, 255 )

inv_game = invGameClass.InvadersGame()

windowTitle = 'Invaders From Space'

pygame.init()

# create window
surfaceSize = inv_game.getSurfDim()
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

invader_interval = inv_game.getInvInterval()
USEREVENT_INV_DOWN = USEREVENT + 1
USEREVENT_MOTHERSHIP = USEREVENT_INV_DOWN + 1

pygame.time.set_timer( USEREVENT_INV_DOWN, invader_interval )
pygame.time.set_timer( USEREVENT_MOTHERSHIP, random.randint(5000, 10000) )

# run the game loop
while True:

    # if all shelters destroyed then user is told game is over and script exits
    if len( inv_game.getShelters() ) == 0 or inv_game.getGameOver() == True:
        basicFont = pygame.font.SysFont( None, 55 )
        text_over = basicFont.render( 'GAME OVER', True, RED, BLACK )
        text_overRect = text_over.get_rect()
        text_overRect.center = windowSurface.get_rect().center
        windowSurface.blit( text_over, text_overRect )
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
                inv_game.moveTurretRight()
            if event.key == K_LEFT:
                inv_game.moveTurretLeft()
            if event.key == K_SPACE:
                inv_game.fireTurret()
        if event.type == KEYUP:
            if event.key == K_RIGHT and not inv_game.turretMovingLeft():
                inv_game.stopTurret()
            if event.key == K_LEFT and not inv_game.turretMovingRight():
                inv_game.stopTurret()
        if event.type == USEREVENT_INV_DOWN:
            inv_game.moveInvaders()
        if event.type == USEREVENT_MOTHERSHIP:
            inv_game.activateMothership()
    
    inv_game.update( windowSurface )

    # draw frame
    windowSurface.fill( BLACK )
    windowSurface.blit( text_lives, text_livesRect )
    windowSurface.blit( text_score, text_scoreRect )
    # DRAW SCORE!!
    inv_game.getShelters().draw( windowSurface )
    inv_game.getInvaders().draw( windowSurface )
    inv_game.getTurretBullets().draw( windowSurface )
    inv_game.getTurret().draw( windowSurface )
    if inv_game.motherActive():
        inv_game.getMothership().draw( windowSurface )

    time.sleep( inv_game.getFrameDelay() )
    # refresh display with new frame
    pygame.display.update()
