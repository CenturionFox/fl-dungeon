import adventurelib_legacy.util as autil
from adventurelib_legacy.classes import PlayerCharacter, Entity

def tryNoticeAll(entities, enemies, player, isPlayerFriendly=False):
    obliviousEntities = [entity for entity in entities if isinstance(entity, Entity) and not entity.IsDead and entity.Target is None]
    validEnemies = [enemy for enemy in enemies if isinstance(enemy, Entity) and not enemy.IsDead]
    for entity in obliviousEntities:
        if not isPlayerFriendly and entity.tryNotice(player):
            print("The %s noticed you!" % entity.Name)
        else:
            for enemy in validEnemies:
                if entity.tryNotice(enemy):
                    print("The %s noticed %s!" % entity.Name, enemy.Name)
                    break

    return ([entity for entity in entities if isinstance(entity, Entity) and not entity.IsDead and entity.Target is not None],
            [entity for entity in entities if isinstance(entity, Entity) and not entity.IsDead and entity.Target is None])

def battleLoop(player, playerTeam=[], enemies=[]):
    while True:
        autil.clear()
        validEnemies = [enemy for enemy in enemies if isinstance(enemy, Entity)]
        validTeammates = [member for member in playerTeam if isinstance(member, Entity)]

        if(len(validEnemies) < 1):
            return

        livingEnemies = [enemy for enemy in validEnemies if not enemy.IsDead]
        defeatedEnemies = [enemy for enemy in validEnemies if enemy.IsDead]

        livingTeammates = [member for member in validTeammates if not member.IsDead]
    
        listEnemies(livingEnemies)

        if len(defeatedEnemies) > 0:
            print("%s enemies lay slain." % len(defeatedEnemies))
        
        awareTeammates,obliviousTeammates=tryNoticeAll(livingTeammates, enemies, player, True)

        #player moves first

        while True:
            playerMove = input("You stand ready.\n(1) Attack\n(2) Stay your Blade\n(3) Flee!\n\nWhat will you do? ")

            if playerMove == "1":
                # The player valiantly attacks the enemy!
                pass
            elif playerMove == "2":
                # The player stands at the ready
                player.setSteadfast(True)
                break
            elif playerMove == "3":
                escapeBlocked = False
                awareEnemies,obliviousEnemies=tryNoticeAll(livingEnemies, livingTeammates, player)
                if len(awareEnemies) > 0:
                    for enemy in awareEnemies:
                        if autil.randomWithMod(enemy.Random, enemy.Luck) > autil.randomWithMod(player.Random, player.Luck) / (2 + len(livingTeammates)):
                            print("The %s blocked your escape!" % enemy.Name)
                            escapeBlocked = True
                            break;
                    if not escapeBlocked:
                        print("You escape!")
                        return True
                else:
                    print("You make a stealthy escape!")
                    return True
            else:
                pass
            break

        awareEnemies,obliviousEnemies=tryNoticeAll(livingEnemies, playerTeam, player)

        #TODO Player attack type selection; as of now, classes are meaningless beyond stats

        #TODO Player team

        #TODO Enemy team
                
        for enemy in awareEnemies:
            print("The %s attacks!" % enemy.Name)

        if player.IsDead:
            print("You are slain...")
            return False

        if len(awareEnemies) == 0:
            print("\nNothing happens.\n")

        player.setSteadfast(False)
        input("Press ENTER to continue...")


def listEnemies(livingEnemies):
    if len(livingEnemies) == 0:
        print("No enemies remain.")
        print("")
    elif len(livingEnemies) == 1:
        print("Your path is blocked by a %s" % str(livingEnemies[0]))
    else:
        print("Your path is blocked by %s enemies:" % len(livingEnemies))
        index = 0
        for enemy in livingEnemies:
            index = index + 1
            print("(%s) %s" % (index, str(enemy)))
            enemy.setSteadfast(False)
        print("")
