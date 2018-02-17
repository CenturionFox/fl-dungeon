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

if enc.battleLoop(player, enemies=monsters):
    autil.clear()
    print("You have been healed.")
    player.HP = player.MaxHealth
    print(player)
    print("")
    input("press ENTER to continue...")

    monsters = [
        cl.Entity("Greater Angelic Force").applyModifiers((12,6,8,10,8,-20)),
        cl.Entity("Angelic Force").applyModifiers((0,1,0,10,0,-10)),
        cl.Entity("Lesser Seraph 1").applyModifiers((-6,0,0,10,0,-5)),
        cl.Entity("Lesser Seraph 2").applyModifiers((-6,0,0,10,0,-5)),
        cl.Entity("Pitiful Frantic Seraph 1").applyModifiers((-9,-2,0,10,0,20)),
        cl.Entity("Pitiful Frantic Seraph 2").applyModifiers((-9,-2,0,10,0,20)),
        cl.Entity("Pitiful Frantic Seraph 3").applyModifiers((-9,-2,0,10,0,20)),
        cl.Entity("Pitiful Frantic Seraph 4").applyModifiers((-9,-2,0,10,0,20))
    ]

    enc.battleLoop(player, enemies=monsters)

autil.clear()
print("")
print("GAME OVER")
print("")
