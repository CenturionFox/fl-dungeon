import time
import adventurelib_legacy as lib
import adventurelib_legacy.classes as cl
import adventurelib_legacy.encounter as enc
import adventurelib_legacy.util as autil
import random
autil.clear()
player = lib.characterSelection()
autil.clear()
print(player)
print("")
input("Press Enter for ADVENTURE... ")

monsters = [
    cl.Entity("Lucky Kobol").applyModifiers((-8,0,0,5,0,0)), 
    cl.Entity("Lesser Goblin").applyModifiers((-4,0,0,0,0,0))
]

enc.battleLoop(player, enemies=monsters)

print("GAME OVER")
