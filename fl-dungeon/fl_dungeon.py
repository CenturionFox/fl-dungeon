#####################################################################
##                     created by centurionfox                     ##
##                                                                 ##
##           Special Thanks to Lunar_kitsune for the idea          ##
#####################################################################

import adventurelib
import pygame
import sys
import time
from adventurelib.localization import t

this = sys.modules[__name__]
this.gameRun = True

TICKS_PER_SECOND = 60
SKIP_TICKS = 1000 / 60
MAX_FRAMESKIP = 12

size = width,height = 640,480
this.screen = pygame.display.set_mode(size)

def main(*args):
    pygame.init()

    interpolation = 0.0

    nextTick = pygame.time.get_ticks()
    while this.gameRun:
        loops = 0
        
        while pygame.time.get_ticks() > nextTick and loops < MAX_FRAMESKIP:
            update()
            nextTick = nextTick + SKIP_TICKS
            loops = loops + 1
            pass

        interpolation = (pygame.time.get_ticks() + SKIP_TICKS - nextTick) / SKIP_TICKS
        render(interpolation)

def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    print("update")
    pass

def render(interpolation):
    print("display %f" % interpolation)
    screen.fill([0,0,0])

    pygame.display.flip()
    pass

if __name__ == "__main__":
    main(sys.argv)
