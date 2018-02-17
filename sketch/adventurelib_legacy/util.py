import os
from random import Random

def clear(printHeader = True):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("##################################################\n#            ADVENTURE EXAMPLE V1.0.0            #\n# Copyright (c) 2018 CenturionFox, Lunar_kitsune #\n##################################################\n")

def isInt(val):
    """We'll try to convert val to an int and if we fail it obviously isn't one"""
    try:
        int(val)
        return True
    except ValueError:
        return False

def getLuckStat(luckVal):
    if luckVal < 1:
        return "Unlucky"
    elif luckVal >= 1 and luckVal < 3:
        return "Lucky"
    elif luckVal >= 3:
        return "Very Lucky" 

def getMagicStat(magicVal):
    if(magicVal < 1):
        return "No Magical Ability"
    elif magicVal >= 1 and magicVal < 5:
        return "Standard Magical Ability"
    elif magicVal >= 5:
        return "Exceptional Magical Ability"

def getStrengthStat(strengthVal):
    if strengthVal <= 1:
        return "Very Weak"
    elif strengthVal == 2:
        return "Weak"
    elif strengthVal >= 3 and strengthVal < 5:
        return "Fairly Strong"
    elif strengthVal >= 5 and strengthVal < 7:
        return "Strong"
    elif strengthVal >= 7 and strengthVal < 9:
        return "Very Strong"
    elif strengthVal > 9:
        return "Extremely Strong"

def randomWithMod(random, mod, max = 10):
    if not isinstance(random, Random):
        return 0
    base = random.random()
    mod = random.random() * (mod/max)
    return base + mod