from . import JsonDataObject, JsonIntegerRange, JsonFileReference

class EntityStats(JsonDataObject):
    """Entity default stats object"""
    default_data={
        "health": 100,
        "armor": 0,
        "strength": 20,
        "magic": 0,
        "luck": 0,
        "agility": 20,
        "awareness": 20
    }

    @staticmethod
    def get_default_data():
        """Gets the default stats for the entity."""
        return EntityStats.default_data

    def decode(self, data):
        if not isinstance(data, dict):
            raise NotImplementedError()
        self._health = JsonIntegerRange.get_int_from_data(data, "health", EntityStats.default_data["health"])
        self._armor = JsonIntegerRange.get_int_from_data(data, "armor", EntityStats.default_data["armor"])
        self._strength = JsonIntegerRange.get_int_from_data(data, "strength", EntityStats.default_data["strength"])
        self._magic = JsonIntegerRange.get_int_from_data(data, "magic", EntityStats.default_data["magic"])
        self._luck = JsonIntegerRange.get_int_from_data(data, "luck", EntityStats.default_data["luck"])
        self._agility = JsonIntegerRange.get_int_from_data(data, "agility", EntityStats.default_data["agility"])
        self._awareness = JsonIntegerRange.get_int_from_data(data, "awareness", EntityStats.default_data["awareness"])

    def encode(self):
        return {
            "health": self._health,
            "armor": self._armor,
            "strength": self._strength,
            "magic": self._magic,
            "luck": self._luck,
            "agility": self._agility,
            "awareness":self._awareness
        }

    @property
    def Health(self):
        return self._health
    
    @Health.setter
    def Health(self, value):
        self._health = value

    @property
    def Armor(self):
        return self._armor
    
    @Armor.setter
    def Armor(self, value):
        self._armor = value

    @property
    def Strength(self):
        return self._strength
    
    @Strength.setter
    def Strength(self, value):
        self._strength = value

    @property
    def Magic(self):
        return self._magic
    
    @Magic.setter
    def Magic(self, value):
        self._magic = value

    @property
    def Luck(self):
        return self._luck
    
    @Luck.setter
    def Luck(self, value):
        self._luck = value

    @property
    def Agility(self):
        return self._agility
    
    @Agility.setter
    def Agility(self, value):
        self._agility = value

    @property
    def Awareness(self):
        return self._awareness
    
    @Awareness.setter
    def Awareness(self, value):
        self._awareness = value


class AdventurerType(JsonDataObject):
    
    default_data = {
        "name":"class.noname",
        "description":"class.nodescription",
        "gold":0
    }

    @staticmethod
    def get_default_data():
        return AdventurerType.default_stats

    def decode(self, data):
        if not isinstance(data, dict):
            raise NotImplementedError()
        
        

    def encode(self):
        return super().encode()