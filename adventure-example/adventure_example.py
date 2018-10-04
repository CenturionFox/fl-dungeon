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
    cl.Entity("Lesser Kobol").applyModifiers((-8,0,0,0,0,0)), 
    cl.Entity("Lesser Kobol").applyModifiers((-8,0,0,0,0,0)),
    cl.Entity("Lesser Kobol").applyModifiers((-8,0,0,0,0,0))
]

if enc.battleLoop(player, enemies=monsters):
    autil.clear()
    print(player)
    print("")
    input("press ENTER to continue...")

    monsters = [
        cl.Entity("Lucky Kobol").applyModifiers((-8,0,0,5,0,0)), 
        cl.Entity("Lesser Goblin").applyModifiers((-4,0,0,0,0,0))
    ]

    if enc.battleLoop(player, enemies=monsters):
        autil.clear()
        print("Your patron heals you for your bravery.")
        player.HP = player.MaxHealth
        print(player)
        print("")
        input("press ENTER to continue...")

        monsters = [
            cl.Entity("Goblin Fighter").applyModifiers((-4,2,1,1,0,2)), 
            cl.Entity("Kobol Shaman").applyModifiers((-9,0,0,2,3,0)),
            cl.Entity("Kobol Fighter").applyModifiers((-6,1,0,0,0,0)),
            cl.Entity("Lesser Goblin").applyModifiers((-4,0,0,0,0,0))
        ]
        if enc.battleLoop(player, enemies=monsters):
            autil.clear()
            print("A voice echoes in your head:\n\tO, hero, beware; ahead is a dangerous enemy.  Be steadfast!")
            print("Your armor class has been boosted!")
            player.Armor = player.Armor + 1
            print("Your health has been boosted!")
            player.MaxHealth = player.MaxHealth + 2
            player.HP = player.MaxHealth
            print(player)
            print("")
            input("press ENTER to continue...")
            
            monsters = [
                cl.Entity("Orcish Paladin").applyModifiers((0,2,4,3,3,8))
            ]

            if enc.battleLoop(player, enemies=monsters):
                autil.clear()
                print("Your patron heals you for your bravery.")
                player.HP = player.MaxHealth
                print(player)
                print("")
                input("press ENTER to continue...")

                monsters = [
                    cl.Entity("Lesser Diety (Ky'Resh Unborn)").applyModifiers((10,5,5,8,10,-1))
                ]

                if enc.battleLoop(player, enemies=monsters):
                    autil.clear()
                    print("")
                    print("YOU WIN!")
                    print("")
                    input("press ENTER to continue...")

autil.clear()
print("")
print("GAME OVER")
print("")
