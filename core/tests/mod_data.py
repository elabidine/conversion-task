from django.test import TestCase
from core.utils.mod_data import mod_data

class TestModData(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.data = {'a': 1, 'b': "hello"}

    def test_updating_keys(self):
        self.assertEqual(mod_data(self.data, a=10), {'a': 10, 'b': "hello"})
        self.assertEqual(mod_data(self.data, b="world"), {'a': 1, 'b': "world"})
        self.assertEqual(mod_data(self.data, c="new"), {'a': 1, 'b': "hello", 'c': "new"})
        self.assertEqual(mod_data(self.data), {'a': 1, 'b': "hello"})
        self.assertEqual(mod_data(self.data, a=None), {'a': None, 'b': "hello"})

    def test_new_instance_returned(self):
        new_data = mod_data(self.data)
        self.assertEqual(new_data, {'a': 1, 'b': "hello"})
        self.assertIsNot(new_data, self.data)
