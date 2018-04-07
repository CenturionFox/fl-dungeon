#####################################################################
##                     created by centurionfox                     ##
##                                                                 ##
##           Special Thanks to Lunar_kitsune for the idea          ##
#####################################################################

import adventurelib
import pygame
import sys
from adventurelib.localization import t

this = sys.modules[__name__]
this.gameRun = True

MS_PER_UPDATE = 16.67

def main(*args):
    pygame.init()

    screen = pygame.display.set_mode((640,480))
    lagTime = 0

    last = pygame.time.get_ticks()
    while this.gameRun:
        current = pygame.time.get_ticks()
        elapsed = current - last
        last = current
        lagTime += elapsed

        processInput()

        while lagTime >= MS_PER_UPDATE:
            update()
            lagTime -= MS_PER_UPDATE

        render(screen, lagTime/MS_PER_UPDATE)

def processInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            this.gameRun = False

def update():
    print('update')
    pass

def render(screen, percent):
    print("draw: %f" % percent)
    pass

if __name__ == "__main__":
    main(sys.argv)
