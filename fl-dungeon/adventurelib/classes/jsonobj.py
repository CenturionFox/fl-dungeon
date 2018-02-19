import abc
import json
import math
import os
import pkgutil
import sys
from random import Random
from ..util import is_int

class JsonDataObjectEncoder(json.JSONEncoder):
    """JSON utility class to encode the object as a dictionary"""
    def default(self, o):
        if isinstance(o, JsonDataObject):
            return o.encode()
        return json.JSONEncoder.default(self, o)

class JsonDataObject(abc.ABC):
    """Base type for json-defined objects"""

    def __init__(self, data=None, stream=None, rawData=None):
        self.decode(JsonDataObject.get_raw_data(data, stream, rawData, self.__class__.get_default_data()))
    
    @staticmethod
    def get_raw_data(data, stream, rawData, default):
        """Gets a dict from json data"""
        if data is not None:
            try:
                return dict(json.loads(data))
            except json.JSONDecodeError as ex:
                print(str(ex), file=sys.stderr)

        if stream is not None:
            try:
                return dict(json.load(stream))
            except json.JSONDecodeError as ex:
                print(str(ex), file=sys.stderr)

        return (rawData if rawData is not None else default)


    def dump(self, outputStream):
        """Writes the object to a stream as json."""
        return json.dump(self, outputStream, cls=JsonDataObjectEncoder)

    def dumps(self):
        """Writes the object as a json-formatted string."""
        return json.dumps(self, cls=JsonDataObjectEncoder)

    @staticmethod
    @abc.abstractmethod
    def get_default_data():
        pass

    @abc.abstractmethod
    def decode(self, data):
        pass

    @abc.abstractmethod
    def encode(self):
        pass

class JsonIntegerRange(JsonDataObject):
    
    def __init__(self, data=None, stream=None, rawData=None):
        self._random = Random()
        return super(JsonIntegerRange, self).__init__(data, stream, rawData)

    @staticmethod
    def get_default_data():
        return 0

    @staticmethod
    def get_int_from_data(data, statName, defaultValue):
        return int(JsonIntegerRange(rawData=data.get(statName,defaultValue)))

    def decode(self, data):
        if is_int(data):
            self._min = self._max = int(data)
        elif isinstance(data, list) or isinstance(data, tuple):
            if len(data) == 0:
                self._min = self._max = 0
            elif len(data) == 1:
                self._min = self._max = data[0]
            else:
                self._min = min(data[0],data[1])
                self._max = max(data[0],data[1])
        elif isinstance(data, dict):
            self._min = min(data.get("min",data.get("max",0)),data.get("max",data.get("min",0)))
            self._max = max(data.get("min",data.get("max",0)),data.get("max",data.get("min",0)))
        else:
            self._min = self._max = 0

    def encode(self):
        if self._min == self._max:
            return self._min;
        return [self._min, self._max]

    def __int__(self):
        if self._min == self._max:
            return self._min
        percent = self._random.random()
        dist = self._max - self._min;
        offset = math.floor(dist * percent)
        return self._min + offset

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
        
        self._starterKits = []
        starterKitEntries = data.get("starterkits",[])
        for kit in starterKitEntries:
            fileReference = JsonFileReference.get_json_file_reference(rawData=kit)
            starterKitEntries.append(InventoryType(data=fileReference.getJsonData()))

    def encode(self):
        return super().encode()

class JsonFileReference(JsonDataObject):

    default_data = {}
    cached_entries = {}

    @staticmethod
    def get_default_data():
        return JsonFileReference.default_data

    @staticmethod
    def get_json_file_reference(data = None, stream = None, rawData = None):
        raw_data = JsonDataObject.get_raw_data(data, stream, rawData, None)
        if not isinstance(raw_data, dict):
            raise NotImplementedError()

        if JsonFileReference.cached_entries.get(raw_data["id"]) is None:
            fileReference = JsonFileReference(rawData = raw_data)
            cached_entries[fileReference._id] = fileReference
            return fileReference

        return cached_entries[raw_data["id"]]
    

    def decode(self, data):
        if not isinstance(data, dict):
            raise NotImplementedError()
        self._id = data["id"]
        self._name = data["name"]
        self._package = data["package"]
        self._resourcePath = data["resource"]

    def encode(self):
        return {
            "id": self._id,
            "name": self._name,
            "package": self._package,
            "resource": self._resourcePath
        }

    def getJsonData(self):
        return pkgutil.get_data(self._package, self._resourcePath)

    def getJsonStream(self):
        d = os.path.dirname(sys.modules[self._package].__file__)
        return open(os.path.join(d, self._resourcePath), 'rb')

    def getJsonRawData(self):
        return json.loads(self.getJsonData())
