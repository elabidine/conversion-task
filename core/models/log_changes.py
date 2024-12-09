from django.utils import timezone
from django.db import models
from core.utils.show_differences import show_differences_separate
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


def log_changes(instance, dummy_member, old_values, new_values):
    """A function to log changes to an object"""
    content_type = ContentType.objects.get_for_model(instance)
    log_entry = LogEntry.objects.create(
        dummy_member=dummy_member, content_type=content_type, object_id=instance.pk
    )

    for field, old_value in old_values.items():
        new_value = new_values.get(field)
        if old_value != new_value:
            # Use show_differences_separate for long texts
            if isinstance(old_value, str) and len(old_value.split()) > 10:
                old_diff, new_diff = show_differences_separate(old_value, new_value)
                old_value = old_diff
                new_value = new_diff
            log_line = LogEntryLine.objects.create(
                log_entry=log_entry,
                field_name=field,
                old_value=old_value,
                new_value=new_value,
            )
            print(log_line)


class LogEntry(models.Model):

    class Meta:
        app_label = "mvp_flexup.core"

    """ A log entry for a change to an object"""
    # member = models.ForeignKey('account.Member', on_delete=models.PROTECT)
    dummy_member = models.CharField(
        max_length=255, blank=True, null=True, default="temp_LogEntry"
    )
    datetime = models.DateTimeField(default=timezone.now)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.PROTECT, related_name="core_log_entries"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.datetime.strftime('%Y-%m-%d')} by {self.dummy_member}: {self.content_object}"


class LogEntryLine(models.Model):
    """A line in a log entry, representing a change to a specific field"""

    class Meta:
        app_label = "mvp_flexup.core"

    log_entry = models.ForeignKey(
        LogEntry, related_name="log_entry_lines", on_delete=models.PROTECT
    )
    field_name = models.CharField(max_length=255)
    old_value = models.TextField(_("Old value"), blank=True, null=True)
    new_value = models.TextField(_("New value"), blank=True, null=True)

    def __str__(self):
        return f"{self.field_name}: {self.old_value[:50] + '...' if self.old_value and len(self.old_value) > 50 else self.new_value} → {self.new_value[:50] + '...' if self.new_value and len(self.new_value) > 50 else self.new_value}"


class DummyModel(models.Model):
    """A dummy model for testing log changes"""

    name = models.CharField(
        max_length=255, blank=True, null=True, default="tempt_DummyModel"
    )
    description = models.TextField(blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "mvp_flexup.core"

    def __str__(self):
        return self.name

    def save(self, dummy_member="dummy_member", *args, **kwargs):
        if self.pk:
            old_instance = DummyModel.objects.get(pk=self.pk)
            old_values = {}
            new_values = {}
            for field in self._meta.fields:
                field_name = field.name
                old_value = getattr(old_instance, field_name)
                new_value = getattr(self, field_name)
                old_values[field_name] = old_value
                new_values[field_name] = new_value
            # Assuming 'modified_by' is a field storing the member
            dummy_member = getattr(self, "modified_by", None)
            log_changes(self, dummy_member, old_values, new_values)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


# This is old code
# class Log(models.Model):
#     ''' A log of changes to an object'''
#
#     def log_changes(self, instance, old_values, new_values, modified_by):
#         # Compare old_values and new_values, create LogEntry and LogEntryLines
#         changes = {}
#         for field in instance._meta.fields:
#             field_name = field.name
#             if field_name == 'id':
#                 continue  # Skip the ID field
#             old_value = old_values.get(field_name)
#             new_value = new_values.get(field_name)
#             if old_value != new_value:
#             # Handle long text fields
#                 if (isinstance(old_value, str) and len(old_value) > 50) or (isinstance(new_value, str) and len(new_value) > 50):
#                     old_value_abbreviated = show_differences(old_value, new_value)
#                     new_value_abbreviated = show_differences(new_value, old_value)
#                     changes[field_name] = (old_value_abbreviated, new_value_abbreviated)
#                 else:
#                     changes[field_name] = (old_value, new_value)
#
#         if changes:
#             log_entry = LogEntry(
#                 date=datetime.datetime.now(),
#                 modified_by_account_member=modified_by,
#                 model_name=instance.__class__.__name__,
#             )
#             log_entry.save()
#             for field_name, (old_value, new_value) in changes.items():
#                 log_entry_line = LogEntryLine(
#                     field_name=field_name,
#                     old_value=str(old_value),
#                     new_value=str(new_value)
#                 )
#                 log_entry_line.save()
#                 log_entry.log_entry_lines.add(log_entry_line)
#             self.log_entries.add(log_entry)
#             self.save()
#
#         # Fab→JB 202406-26: I have attempted to implement a logging features, but I'm not sure I'm doing this right. Can you please check it? Maybe we should move some of this logic to a parent class?
#
#     log = models.ForeignKey(Log, on_delete=models.SET_NULL, null=True, blank=True)
#
#     def __init__(self, *args, **kwargs):
#         super(OrderItem, self).__init__(*args, **kwargs)
#         # Store original field values
#         self._original_values = self._dict_values()
#
#     def _dict_values(self):
#         # Helper method to get a dictionary of field values
#         return {field.name: getattr(self, field.name) for field in self._meta.fields}
#
#     def save(self, *args, **kwargs):
#         # Determine if the object is new
#         is_new = self.pk is None
#         # Save the object first
#         super(OrderItem, self).save(*args, **kwargs)
#         if not is_new:
#             # Compare old and new values
#             new_values = self._dict_values()
#             old_values = self._original_values
#             self.log_changes(old_values, new_values)
#             # Update original values
#             self._original_values = new_values
#         else:
#             # Initialize the log for new objects
#             self.log = Log()
#             self.log.save()
#             self.save()
#
#     def log_changes(self, old_values, new_values):
#         modified_by = self.get_modified_by_account_member()
#         if self.log is None:
#             self.log = Log()
#             self.log.save()
#             self.save()
#         self.log.log_changes(self, old_values, new_values, modified_by)
#
#     def get_modified_by_account_member(self):
#         # Implement logic to retrieve the current member
#         # This may require access to the request object
#         return AccountMember.objects.get(member=self.modified_by)  # Placeholder implementation
#
#     def __str__(self):
#         return f"{self.product} x {self.quantity}"
