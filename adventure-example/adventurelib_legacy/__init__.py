#Adventure values module!
import sys
import time
import adventurelib_legacy.util as autil
from adventurelib_legacy.classes import PlayerCharacter

__this__ = sys.modules[__name__]

###Character Class Stats###
CharacterClasses = [
#Class name, HP mod, magic mod, strength mod, armor class mod, luck mod, gold mod
    ("Magician",-1,5,-1,0,0,20),
    ("Vampire",1,3,0,0,1,0),
    ("Hunter",1,0,1,0,1,0),
    ("Fighter",2,0,2,0,0,-20),
    ("Jester",1,0,0,-1,3,-40),
    ("Civilian",0,0,0,0,0,40),
    ("Necromancer",-4,5,0,0,0,-20),
    ("Paladin",6,2,2,3,1,-70)
]
###Character Class Stats End###

def characterSelection():
    player = PlayerCharacter()
    player.Name = input("My name is: ")
    while True:
        """We'll loop here just in case the user enters something cheeky"""
        print("Please choose your character class:")
        index = 1
        for classMod in __this__.CharacterClasses:
            """This loop will print all of the available classes in the list, plus the index the user can type (1-based)"""
            print("(%s) %s" % (index, classMod[0])) # (1) Magician (and so on)
            index = index + 1
        print("")
        charChoice = input("I am a: ")
                
        if autil.isInt(charChoice) and int(charChoice) > 0 and int(charChoice) <= len(__this__.CharacterClasses): #charChoice is an integer and within range
            """The user entered something sensible, like a 1"""
            choice = __this__.CharacterClasses[int(charChoice) - 1]
            player.applyModifiers(choice)
            break
        else:
            """ The user probably entered a cuss word or something else hilarious """
            #echo the choice so they can giggle about the fact that the program said "poop" to them
            print("'%s' is not a valid choice!" % charChoice) 
            print("")
    return player