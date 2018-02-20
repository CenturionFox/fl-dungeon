from random import Random
from adventurelib.jsonobj import *

class Entity(object):
    """Base entity type"""
    def __init__(self, name, stats=EntityStats()):
        self._baseStats = stats
        self.initStats(stats)
        self.initializeFields()

    def initStats(self, stats):
        self._health = stats.Health
        
    def initializeFields(self):
        self._steadfast = False
        self._healthModifier = 1.0
        self._armorModifier = 1.0
        self._strengthModifier = 1.0
        self._magicModifier = 1.0
        self._luckModifier = 1.0
        self._agilityModifier = 1.0
        self._agilityModifier = 1.0

    @property
    def BaseStats(self):
        return self._baseStats

    @property
    def IsSteadfast(self):
        return self._steadfast