import unittest
from adventurelib.util import *

class util_test(unittest.TestCase):

    def test_class_for_name_failOnNoModuleSpecified(self):
        with self.assertRaises(TypeError):
            class_for_name("invalidName")

    def test_class_for_name_failOnInvalidClassName(self):
        with self.assertRaises(TypeError):
            class_for_name("package.but not/a/class name though")

    def test_class_for_name_failOnEndWithDot(self):
        with self.assertRaises(TypeError):
            class_for_name("package.")

    def test_class_for_name_successForExistingClass(self):
        class_ = class_for_name("adventurelib.classes.jsonobj.EntityStats")
        self.assertIsNotNone(class_)

    def test_class_for_name_classIsSuccessfulAndMatches(self):
        class_ = class_for_name("__main__.util_test")
        self.assertEqual(self.__class__, class_)
    
if __name__ == '__main__':
    unittest.main()