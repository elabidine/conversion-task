"""
python manage.py test utils.tests.print_utils.TestPrintObject
"""
from django.test import TestCase
from io import StringIO
from unittest import TestCase
from unittest.mock import patch
from utils.print_object import _print_object


class TestSimpleObject:
    def __init__(self):
        self.name = "Test"
        self.value = 42
    def __str__(self):
        return "TestObject"


class TestPrintObject(TestCase):
    def setUp(self):
        self.test_obj = TestSimpleObject()
        self.output = StringIO()
        self.patcher = patch('sys.stdout', self.output)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_basic_property(self):
        _print_object(self.test_obj, "name")
        expected = "  - TestObject = TestObject\n    - name: Test\n"
        self.assertEqual(self.output.getvalue(), expected)

    def test_multiple_properties(self):
        _print_object(self.test_obj, "name", "value")
        expected = "  - TestObject = TestObject\n    - name: Test, value: 42\n"
        self.assertEqual(self.output.getvalue(), expected)

    def test_literal_string(self):
        _print_object(self.test_obj, "-Hello")
        expected = "  - TestObject = TestObject\n    - Hello\n"
        self.assertEqual(self.output.getvalue(), expected)

    def test_missing_property(self):
        _print_object(self.test_obj, "missing_prop")
        expected = "  - TestObject = TestObject\n    - missing_prop: not found\n"
        self.assertEqual(self.output.getvalue(), expected)

    def test_mixed_content(self):
        _print_object(self.test_obj, "name", "-> ", "value")
        expected = "  - TestObject = TestObject\n    - name: Test\n    - > value: 42\n"
        self.assertEqual(self.output.getvalue(), expected)

    def test_no_properties(self):
        _print_object(self.test_obj)
        expected = "  - TestObject = TestObject\n"
        self.assertEqual(self.output.getvalue(), expected)

    def test_none_object(self):
        _print_object(None)
        expected = "  - NoneType = None\n"
        self.assertEqual(self.output.getvalue(), expected)
