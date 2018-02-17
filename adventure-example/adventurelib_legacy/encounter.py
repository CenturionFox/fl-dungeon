import adventurelib_legacy.util as autil
from adventurelib_legacy.classes import PlayerCharacter, Entity

def tryNoticeAll(entities, enemies, player, isPlayerFriendly=False):
    obliviousEntities = [entity for entity in entities if isinstance(entity, Entity) and not entity.IsDead and entity.Target is None]
    validEnemies = [enemy for enemy in enemies if isinstance(enemy, Entity) and not enemy.IsDead]

    noticed = 0

    for entity in obliviousEntities:
        if not isPlayerFriendly and entity.tryNotice(player):
            print("")
            print("The %s noticed you!" % entity.Name)
            noticed = noticed + 1
        else:
            for enemy in validEnemies:
                if entity.tryNotice(enemy):
                    print("")
                    print("The %s noticed %s!" % entity.Name, enemy.Name)
                    noticed = noticed + 1
                    break

    awareEnemies = [entity for entity in entities if isinstance(entity, Entity) and not entity.IsDead and entity.Target is not None]
    obliviousEnemies = [entity for entity in entities if isinstance(entity, Entity) and not entity.IsDead and entity.Target is None]

    if(noticed > 0):
        print("")
        input("Press ENTER to continue...")

    return (awareEnemies,obliviousEnemies)

def battleLoop(player, playerTeam=[], enemies=[]):
    while True:
        autil.clear()

        print("Your HP is %s" % player.HP)
        print("")

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
            print("")
        
        awareTeammates,obliviousTeammates=tryNoticeAll(livingTeammates, enemies, player, True)

        #player moves first

        while True:
            playerMove = input("You stand ready.\n(1) Attack\n(2) Stay your Blade\n(3) Flee!\n\nWhat will you do? ")

            if playerMove == "1":
                # The player valiantly attacks the enemy!
                if len(livingEnemies) > 1:
                    while True:
                        playerAttack = input("Which enemy? (number): ")
                        if autil.isInt(playerAttack) and 0 < int(playerAttack) <= len(livingEnemies):
                            target = livingEnemies[int(playerAttack) - 1]
                            player.attack(target)
                            if target.IsDead:
                                if target.HP * -1 >= target.MaxHealth:
                                    print("The %(target)s has been slain with prejudice." % {"target": target.Name})
                                else:
                                    print("The %(target)s has been slain." % {"target": target.Name})
                            break;
                        print('"%(that)s" is not a valid choice.' % {'that':playerMove})
                        awareEnemies,obliviousEnemies=tryNoticeAll(livingEnemies, livingTeammates, player)
                        if len(awareEnemies) > 0:
                            staggered = False
                            for enemy in awareEnemies:
                                if autil.randomWithMod(enemy.Random, enemy.Luck) > autil.randomWithMod(player.Random, player.Luck) / (2 + len(livingTeammates)):
                                    print("As you hesitate, the %s attempts to attack!" % enemy.Name)
                                    if(enemy.attack(player)[0]):
                                        print("The %s's attack staggers you! Your turn ends." % enemy.Name)
                                        staggered = True
                                        break
                            if staggered: break
                elif len(livingEnemies) == 1:
                    target = livingEnemies[0]
                    player.attack(target)
                    if target.IsDead:
                        print("The %(target)s has been slain." % {"target": target.Name})
                    break;
                break
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
                            autil.clear()
                            print("The %s blocked your escape!" % enemy.Name)
                            escapeBlocked = True
                            break;
                    if not escapeBlocked:
                        print("You escape!")
                        input("Press ENTER to continue...")
                        return True
                else:
                    print("You make a stealthy escape!")
                    input("Press ENTER to continue...")
                    return True
            else:
                print('"%(that)s" is not a valid choice.' % {'that':playerMove})
                awareEnemies,obliviousEnemies=tryNoticeAll(livingEnemies, livingTeammates, player)
                staggered = False
                if len(awareEnemies) > 0:
                    for enemy in awareEnemies:
                        if autil.randomWithMod(enemy.Random, enemy.Luck) > autil.randomWithMod(player.Random, player.Luck) / (2 + len(livingTeammates)):
                            print("As you hesitate, the %s attempts to attack!" % enemy.Name)
                            if(enemy.attack(player)[0]):
                                print("The %s's attack staggers you! Your turn ends." % enemy.Name)
                                staggered = True
                                break;
                if staggered: break
                continue;
            break
        print("")

        livingEnemies = [enemy for enemy in validEnemies if not enemy.IsDead]
        defeatedEnemies = [enemy for enemy in validEnemies if enemy.IsDead]

        if player.IsDead:
            print("\nYou are slain...\n")
            input("Press ENTER to continue...")
            return False

        if len(livingEnemies) == 0:
            print("The battle ends! All enemies lay slain.")
            input("Press ENTER to continue...")
            break;

        input("Press ENTER to continue...")

        awareEnemies,obliviousEnemies=tryNoticeAll(livingEnemies, playerTeam, player)

        #TODO Player team

        livingEnemies = [enemy for enemy in validEnemies if not enemy.IsDead]
        defeatedEnemies = [enemy for enemy in validEnemies if enemy.IsDead]

        if player.IsDead:
            print("\nYou are slain...\n")
            input("Press ENTER to continue...")
            return False

        if len(livingEnemies) == 0:
            print("The battle ends! All enemies lay slain.")
            input("Press ENTER to continue...")
            break;

        awareEnemies,obliviousEnemies=tryNoticeAll(livingEnemies, playerTeam, player)

        #TODO Enemy team
                
        for enemy in awareEnemies:
            autil.clear()
            print("The %s attacks!" % enemy.Name)
            print("")
            enemy.attack(player)
            if player.IsDead:
                print("\nYou are slain...\n")
                input("Press ENTER to continue...")
                return False
            print("")
            input("Press ENTER to continue...")

        if player.IsDead:
            print("\nYou are slain...\n")
            input("Press ENTER to continue...")
            return False

        player.setSteadfast(False)

        if len(livingEnemies) == 0:
            print("The battle ends! All enemies lay slain.")
            input("Press ENTER to continue...")
            break;
    return True


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
