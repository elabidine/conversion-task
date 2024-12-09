# ------------- core/models/status_log.py

from django.forms import ValidationError
from core.enums.status import Status, Action, StatusShortList
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.models.flexup_enum_field import FlexUpEnumField
from core.models.flexup_model import FlexUpModel
from utils.print_object import _print_object


class StatusLog(FlexUpModel):
    """  Model to keep track of status changes and actions taken for any entity (e.g., Contract, Order). This is different from the LogEntry model which is used to keep track of changes to any fields of an object. """

    class Meta:
        ordering = ['-action_datetime']
        verbose_name = _('Status Log')
        verbose_name_plural = _('Status Logs')
        indexes = [ models.Index(fields=['content_type', 'object_id']) ]

    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, verbose_name=_('Object Type'))
    object_id = models.PositiveIntegerField(verbose_name=_('Object ID'))
    content_object = GenericForeignKey('content_type', 'object_id')

    action = FlexUpEnumField(flexup_enum=Action, choices=Action.choices, blank=True, null=True) # blank for system status changes
    initial_status = FlexUpEnumField(flexup_enum=Status, choices=Status.choices, blank=True, null=True) # blanks for the first status assigned to an object
    new_status = FlexUpEnumField(flexup_enum=Status, choices=Status.choices, blank=True, null=True) # blank for joint action requests

    action_datetime = models.DateTimeField(default=timezone.now) # date and time of the action, except for system status changes which apply effective date or termination date
    action_by_system = models.BooleanField(default=False)


    def __str__(self):
        by_label = self.created_by_member.account if self.created_by_member and self.created_by_member.account else 'System'
        # _print_object(self.new_status, label="StatusLog.__str__ : self.new_status")
        new_status = f"{self.new_status.label} {self.new_status.symbol} " if self.new_status else '(no new status)'
        return f"{self.action_datetime.date()}: {self.action.label}, {self.initial_status.label} {self.initial_status.symbol} -> {new_status}, by {by_label}"

    def clean(self):
        if not self.created_by_member and not self.action_by_system:
            raise ValueError("Either the created_by_member or action_by_system field must be filled in")
        super().clean()

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValidationError("StatusLog instances cannot be modified once created.")
        super().save(*args, **kwargs)
