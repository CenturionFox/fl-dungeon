import unittest
from adventurelib.classes.jsonobj import *

class Test_JsonDataObject(unittest.TestCase):
    def test_AbstractClassInstantiation(self):
        """Make sure we can't instantiate the abstract base type."""
        with self.assertRaises(TypeError):
            JsonDataObject()

class EntityType_tests(unittest.TestCase):
    def test_defaultValues(self):
        """Make sure the default constructor loads the data correctly."""
        defaults = EntityStats.default_data
        entity = EntityStats()
        self.assertEqual(entity._health, defaults["health"])

    def test_healthProperty(self):
        """Make sure the Health property is working"""
        entity = EntityStats()
        expectedHealth = 512
        entity.Health = 512
        self.assertEqual(expectedHealth, entity._health)
        self.assertEqual(expectedHealth, entity.Health)

    def test_loadJsonData(self):
        data = pkgutil.get_data("adventurelib.tests","res/entityStatTest.json")
        entity = EntityStats(data=data)
        self.assertEqual(120, entity._health)
        self.assertEqual(25, entity._armor)
        self.assertEqual(44, entity._strength)
        self.assertEqual(12, entity._magic)
        self.assertEqual(33, entity._luck)
        self.assertEqual(12, entity._agility)
        self.assertEqual(24, entity._awareness)

    def test_loadJsonStream(self):
        d = os.path.dirname(sys.modules["adventurelib.tests"].__file__)
        with open(os.path.join(d, "res/entityStatTest.json"), 'rb') as data:
            entity = EntityStats(stream=data)
            self.assertEqual(120, entity._health)
            self.assertEqual(25, entity._armor)
            self.assertEqual(44, entity._strength)
            self.assertEqual(12, entity._magic)
            self.assertEqual(33, entity._luck)
            self.assertEqual(12, entity._agility)
            self.assertEqual(24, entity._awareness)

    def test_dumpJsonString(self):
        data = pkgutil.get_data("adventurelib.tests","res/entityStatTest.json")
        entity = EntityStats(data=data)
        strJson = entity.dumps()
        self.assertEqual(strJson, '{"health": 120, "armor": 25, "strength": 44, "magic": 12, "luck": 33, "agility": 12, "awareness": 24}')

    def test_entityStatRanges(self):
        data = pkgutil.get_data("adventurelib.tests","res/entityStatRangeTest.json")
        entity = EntityStats(data=data)
        self.assertTrue(10 <= entity._health <= 50);
        self.assertTrue(10 <= entity._armor <= 50);
        self.assertTrue(10 <= entity._strength <= 50);
        self.assertTrue(10 <= entity._magic <= 50);
        self.assertTrue(10 <= entity._luck <= 50);
        self.assertTrue(10 <= entity._agility <= 50);
        self.assertTrue(10 <= entity._awareness <= 50);

class JsonRangeType_tests(unittest.TestCase):
    def test_initilizeEmpty(self):
        range = JsonIntegerRange();
        self.assertIsNotNone(range._random)
        self.assertEqual(0, range._min)
        self.assertEqual(0, range._max)
        self.assertEqual(0, int(range))

    def test_initilizeInteger(self):
        range = JsonIntegerRange(rawData=4)
        self.assertIsNotNone(range._random)
        self.assertEqual(range._min, range._max)
        self.assertEqual(4, range._min)
        self.assertEqual(4, range._max)
        self.assertEqual(4, int(range))

    def test_initializeSingleList(self):
        range = JsonIntegerRange(rawData=[6])
        self.assertIsNotNone(range._random)
        self.assertEqual(range._min, range._max)
        self.assertEqual(6, range._min)
        self.assertEqual(6, range._max)
        self.assertEqual(6, int(range))

    def test_initializeSingleTuple(self):
        range = JsonIntegerRange(rawData=(6))
        self.assertIsNotNone(range._random)
        self.assertEqual(range._min, range._max)
        self.assertEqual(6, range._min)
        self.assertEqual(6, range._max)
        self.assertEqual(6, int(range))

    def test_initializeMaxOnlyDict(self):
        range = JsonIntegerRange(rawData={"max":7})
        self.assertIsNotNone(range._random)
        self.assertEqual(range._min, range._max)
        self.assertEqual(7, range._min)
        self.assertEqual(7, range._max)
        self.assertEqual(7, int(range))

    def test_initializeMinOnlyDict(self):
        range = JsonIntegerRange(rawData={"min":2})
        self.assertIsNotNone(range._random)
        self.assertEqual(range._min, range._max)
        self.assertEqual(2, range._min)
        self.assertEqual(2, range._max)
        self.assertEqual(2, int(range))

    def test_initializeList(self):
        range = JsonIntegerRange(rawData=[1,6])
        self.assertIsNotNone(range._random)
        self.assertNotEqual(range._min, range._max)
        self.assertEqual(1, range._min)
        self.assertEqual(6, range._max)
        self.assertTrue(1 <= int(range) < 6)

    def test_initializeReversedList(self):
        range = JsonIntegerRange(rawData=[6,1])
        self.assertIsNotNone(range._random)
        self.assertNotEqual(range._min, range._max)
        self.assertEqual(1, range._min)
        self.assertEqual(6, range._max)
        self.assertTrue(1 <= int(range) < 6)

    def test_initializeTuple(self):
        range = JsonIntegerRange(rawData=(1,6))
        self.assertIsNotNone(range._random)
        self.assertNotEqual(range._min, range._max)
        self.assertEqual(1, range._min)
        self.assertEqual(6, range._max)
        self.assertTrue(1 <= int(range) < 6)

    def test_initializeReversedTuple(self):
        range = JsonIntegerRange(rawData=(6,1))
        self.assertIsNotNone(range._random)
        self.assertNotEqual(range._min, range._max)
        self.assertEqual(1, range._min)
        self.assertEqual(6, range._max)
        self.assertTrue(1 <= int(range) < 6)

    def test_initializeDict(self):
        range = JsonIntegerRange(rawData={"min":1,"max":6})
        self.assertIsNotNone(range._random)
        self.assertNotEqual(range._min, range._max)
        self.assertEqual(1, range._min)
        self.assertEqual(6, range._max)
        self.assertTrue(1 <= int(range) < 6)

    def test_initializeReversedDict(self):
        range = JsonIntegerRange(rawData={"min":6,"max":1})
        self.assertIsNotNone(range._random)
        self.assertNotEqual(range._min, range._max)
        self.assertEqual(1, range._min)
        self.assertEqual(6, range._max)
        self.assertTrue(1 <= int(range) < 6)

if __name__ == '__main__':
    unittest.main()
