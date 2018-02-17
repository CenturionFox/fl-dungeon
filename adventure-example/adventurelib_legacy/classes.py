import random
import math
import adventurelib_legacy.util as autil

class Entity(object):

    def __init__(self, name):
        self._hp = 10
        self._maxHP = 10
        self._steadfast = False
        self._random = random.Random()
        self._strength = 2
        self._armor = 1
        self._luck = 0
        self._name = name
        self._target = None
        self._magik = 0
        self._lastDamage = 0
        self._awareness = 2

    def tryNotice(self, target):
        if not isinstance(target, Entity):
            return False
        if autil.randomWithMod(self._random, self._awareness) > 0.5 + autil.randomWithMod(target.Random, target.Luck):
            self._target = target
        return self._target is not None

    def applyModifiers(self, modifiers):
        self._hp = self._hp + modifiers[0]
        self._maxHP = self._hp
        self._strength = self._strength + modifiers[1]
        self._armor = self._armor + modifiers[2]
        self._luck = self._luck + modifiers[3]
        self._magik = self._magik + modifiers[4]
        self._awareness = self._awareness + modifiers[5]
        return self

    def __str__(self):
        return("%s (HP: %s; AC: %s; %s; %s)" % (self._name, self._hp, self._armor, autil.getStrengthStat(self._strength), autil.getLuckStat(self._luck)))

    def getStats(self):
        return ("HP: %s" )

    def damage(self, atk, critical=False, miss=False):
        if critical:
            self.HP = self.HP - atk
            return (True,atk)
        elif miss or atk < (self.Armor / 2):
            return (False,0)
        damage = math.ceil(atk / (1.0 + self.Armor))
        self.HP = self.HP - damage
        return (True,damage)

    def attack(self, target):
        if not isinstance(target, Entity):
            return (False,0)
        
        target.alertAttacker(self, self._strength)

        if autil.randomWithMod(self._random, self._luck) > 0.9:
            print("Critical hit!")
            return target.damage(self._strength, critical=True)
        
        elif autil.randomWithMod(self._random, target.Luck) > 0.9:
            if isinstance(target, PlayerCharacter):
                print("The attack misses!")
            return target.damage(self._strength, miss=True)

        return target.damage(self.Strength)

    def alertAttacker(self, attacker, attackStrength):
        if self._target is None or attackStrength > self._lastDamage:
            self._target = attacker

    def setSteadfast(self, value):
        if isinstance(value, bool):
            self._steadfast = value

    @property
    def Awareness(self):
        return self._awareness
    
    @Awareness.setter
    def Awareness(self, value):
        self._awareness = value

    @property
    def HP(self):
        return self._hp
    
    @HP.setter
    def HP(self, value):
        self._hp = value

    @property
    def MaxHealth(self):
        return self._maxHP
    
    @property
    def Strength(self):
        return self._strength
    
    @Strength.setter
    def Strength(self, value):
        self._strength = value
        
    @property
    def IsSteadfast(self):
        return self._steadfast

    @property
    def Armor(self):
        if(self._steadfast):
            return self._armor + 1
        return self._armor
    
    @Armor.setter
    def Armor(self, value):
        self._armor = value
        
    @property
    def Luck(self):
        return self._luck
    
    @Luck.setter
    def Luck(self, value):
        self._luck = value

    @property
    def Name(self):
        return self._name
    
    @Name.setter
    def Name(self, value):
        self._name = value

    @property
    def Magik(self):
        return self._magik
    
    @Magik.setter
    def Magik(self, value):
        self._magik = value

    @property
    def Random(self):
        return self._random

    @property
    def Target(self):
        return self._target

    @property
    def IsDead(self):
        return self._hp <= 0

## Player Character ##

class PlayerCharacter(Entity):

    def __init__(self):
        """Sets player base stats"""
        Entity.__init__(self, "Player")
        self._magik = 0
        self._gold = 100
        self._class="Default"
        
    def __str__(self):
        return "Your name is %s.\n\tYou are a %s.\n\tYour HP is %s.\n\tYour AC is %s.\n\tYou have %s.\n\tYou are %s.\n\tYou are %s.\n\tYou have %s gold on hand." % (self.Name, self.Class, self.HP, self.Armor, autil.getMagicStat(self.Magik), autil.getStrengthStat(self.Strength), autil.getLuckStat(self.Luck), self.Gold)

    def applyModifiers(self, modifiers):
        Entity.applyModifiers(self, (modifiers[1], modifiers[3], modifiers[4], modifiers[5], modifiers[2], -2))
        self._class = modifiers[0]
        self._gold = self._gold + modifiers[6]
        return self
        
    def damage(self, atk, critical=False, miss=False):
        result = Entity.damage(self, atk, critical, miss)
        if(result[0]):
            print("You were attacked for %s damage! Your HP is now %s." % (result[1], self._hp))
        else:
            print("You block the attack.")
        return result

    def attack(self, target):
        if not isinstance(target, Entity):
            print("You cannot attack that.")
            return (False,0)
        print("You attack the %s!" % target.Name)
        result = Entity.attack(self, target)
        if result[0]:
            print("You land the attack, dealing %s damage!" % (result[1]))
        else:
            print("Your attack misses...")
        return result

    def setSteadfast(self, value):
        if isinstance(value, bool):
            if value:
                print("You steel yourself against attacks. (AC + 1)")
            elif self.IsSteadfast:
                print("You relax your guard. (AC - 1)")
        Entity.setSteadfast(self, value)
            
    @property
    def Gold(self):
        return self._gold
    
    @Gold.setter
    def Gold(self, value):
        self._gold = value
        
    @property
    def Class(self):
        return self._class
        
    @Class.setter
    def Class(self, value):
        self._class = value
