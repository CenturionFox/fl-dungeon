import json
import pkgutil
from ..util import is_int, class_for_name
from abc import ABC, abstractmethod
from json import JSONEncoder, JSONDecodeError
from random import Random
from sys import stderr

class JsonDataObjectEncoder(JSONEncoder):
    """JSON utility class to encode the object from the encode() method"""
    def default(self, o):
        if(isinstance(o, JsonDataObject)):
            return o.encode()
        return super(JsonDataObjectEncoder, self).default(o)

class JsonDataObject(ABC):
    """Abstract base class for JSON-encoded objects"""
    def __init__(self, data=None):
        """Calls the abstract method decode(), passing the json data."""
        self.decode(JsonDataObject.get_raw_data(data, self.__class__.get_default_data()))

    @staticmethod
    def get_raw_data(data, default):
        """Gets the raw data dict for decode()"""
        if isinstance(data, str, bytes, bytearray):
            try:
                return json.loads(data)
            except JSONDecodeError as ex:
                print("An error occurred while decoding the JSON string: %s" % str(ex), file=stderr)
        if getattr(data, 'read') is not None:
            try:
                return dict(json.load(data))
            except JSONDecodeError as ex:
                print("An error occurred while decoding the JSON file: %s" % str(ex), file=stderr)
        return data if data is not None else default

    @staticmethod
    @abstractmethod
    def get_default_data():
        pass

    def dump(self, file):
        """Dumps the JSON data to a file-like object `file`"""
        return json.dump(self, file, cls=JsonDataObjectEncoder)

    def dumps(self):
        """Dumps the JSON data to a str."""
        return json.dumps(self, cls=JsonDataObjectEncoder)

    @abstractmethod
    def decode(self, data):
        """Decodes the object from the given data type."""
        pass

    @abstractmethod
    def encode(self):
        """Encodes the object in JSON."""
        pass

class JsonIntegerRange(JsonDataObject):
    """Represents a json-serializable integer range."""
    def __init__(self, data=None):
        self._random = Random()
        super(JsonIntegerRange, self).__init__(data)

    def __int__(self):
        return self.getRandomIntFromRange()

    @staticmethod
    def get_default_data():
        """Returns the integer value "0\""""
        return 0

    def getRandomIntFromRange(self):
        if self._min == self._max:
            return self._min
        return self._random.randint(self._min, self._max)

    def decode(self, data):
        """Decodes the integer range from an int value, a list or tuple of values, or a dict."""
        if is_int(data):
            self._min = self._max = int(data)
        elif isinstance(data, list, tuple):
            if len(data) == 0:
                self._min = self._max = 0
            elif len(data) == 1:
                if not is_int(0 if data[0] is None else data[0]): 
                    raise NotImplementedError("The list contained invalid data at position 0: %s" % data[0])
                else:
                    self._min = self._max = int(0 if data[0] is None else data[0])
            else:
                pData = (0 if data[0] is None else data[0], 0 if data[1] is None else data[1])
                self._min = min(pData)
                self._max = max(pData)
        elif isinstance(data, dict):
            pData = (data.get("min", 0), data.get("max", 0))
            self._min = min(pData)
            self._max = max(pData)
        else:
            raise NotImplementedError("The type %s cannot be used to initialize a JsonIntegerRange." % data.__class__)

    def encode(self):
        """Encodes the range as a JSON formatted list.  For zero-length ranges, encodes the int value."""
        if self._min == self._max:
            return self._min
        return [self._min, self._max]

class JsonFileReference(JsonDataObject):
    """Represents a JSON file data object reference."""
    
    cached_entries = {}

    @staticmethod
    def get_default_data():
        """Gets an empty json file reference data."""
        return {
            "id": None,
            "name": None,
            "package": None,
            "resource": None
        }

    @staticmethod
    def get_json_file_reference(data):
        """Gets and/or caches a JsonFileReference instance from the object data."""
        rawData = JsonDataObject.get_raw_data(data)
        if not isinstance(rawData, dict):
            raise NotImplementedError("The type %s cannot be used as data to initialize a JsonFileReference" % rawData.__class__)
        id = rawData.get('id')
        if id is None:
            raise JSONDecodeError("\"id\" is a required field.")
        cachedEntry = JsonFileReference.cached_entries.get(id)
        if cachedEntry is None:
            cachedEntry = JsonFileReference(rawData)
            JsonFileReference.cached_entries[id] = cachedEntry
        return cachedEntry

    def getJsonData(self):
        """Gets the JSON data."""
        return pkgutil.get_data(self._package, self._resourcePath)

    def construct(self):
        """Instantiates the class that is described by this json object."""
        if self._class is None:
            raise TypeError("The class is not specified.")
        class_ = class_for_name(self._class)
        if class_ == JsonDataObject or not issubclass(class_, JsonDataObject):
            raise TypeError("Cannot construct a non-JsonDataObject-derived class.")
        return class_.__init__(object(), self.getJsonData())

    def decode(self, data):
        if not isinstance(data, dict):
            raise NotImplementedError("The type %s cannot be used as data to initialize a JsonFileReference" % data.__class__)
        self._id = data['id']
        self._name = data['name']
        self._package = data['package']
        self._resourcePath = data['resource']
        self._class = data.get('class')

    def encode(self):
        return {
            'id': self._id,
            'name': self._name,
            'package': self._package,
            'resource': self._resourcePath,
            'class': self._class
        }
