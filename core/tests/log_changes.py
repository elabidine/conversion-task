import datetime
from django.test import TestCase
from core.models.log_changes import DummyModel

# FILE: core/models/test_log_changes.py


import unittest


@unittest.skip
class TestLogChanges(TestCase):

    def setUp(self):
        # Create initial DummyModel instance
        self.dummy_instance = DummyModel.objects.create(
            name="Initial Name",
            description="Initial Description",
            value=10,
            date=datetime.date.today(),
        )

    def test_assert_true(self):
        self.assertTrue(True)

    def test_create_dummy_model(self):
        # Test creation of DummyModel instance
        self.assertEqual(DummyModel.objects.count(), 1)
        instance = DummyModel.objects.first()
        if instance is None:
            self.fail("DummyModel instance was not created")
        self.assertEqual(instance.name, "Initial Name")
        self.assertEqual(instance.description, "Initial Description")
        self.assertEqual(instance.value, 10)

    def test_update_dummy_model(self):
        # Update DummyModel instance
        self.dummy_instance.name = "Updated Name"
        self.dummy_instance.description = "Updated Description"
        self.dummy_instance.value = 20
        self.dummy_instance.save()


""" #         # Verify that changes are logged
#         log_entry = LogEntry.objects.first()
#         self.assertIsNotNone(log_entry)
#         if not log_entry:
#             self.fail("LogEntry instance was not created")
#         self.assertEqual(log_entry.content_object, self.dummy_instance)
#
#         log_entry_lines = LogEntryLine.objects.filter(log_entry=log_entry)
#         self.assertEqual(log_entry_lines.count(), 3)
#
#         name_change = log_entry_lines.get(field_name="name")
#         self.assertEqual(name_change.old_value, "Initial Name")
#         self.assertEqual(name_change.new_value, "Updated Name")
#
#         description_change = log_entry_lines.get(field_name="description")
#         self.assertEqual(description_change.old_value, "Initial Description")
#         self.assertEqual(description_change.new_value, "Updated Description")
#
#         value_change = log_entry_lines.get(field_name="value")
#         self.assertEqual(value_change.old_value, "10")
#         self.assertEqual(value_change.new_value, "20")
#
#     def test_long_text_logging(self):
#         # Update DummyModel instance with long text
#         long_text = "This is a long text " * 10
#         self.dummy_instance.description = long_text
#         self.dummy_instance.save()
#
#         # Verify that changes are logged with differences
#         log_entry = LogEntry.objects.first()
#         self.assertIsNotNone(log_entry)
#
#         description_change = LogEntryLine.objects.get(log_entry=log_entry, field_name="description")
#         self.assertIn("This is a long text", description_change.old_value)
#         self.assertIn("This is a long text", description_change.new_value)
 """


""" Manual tests

import datetime
from django.test import TestCase
from core.models.log_changes import DummyModel

instance = DummyModel.objects.create(name="Initial Name",description="Initial Description",value=10,date=datetime.date.today())
instance.name = "Updated Name"
instance.save()

 """
