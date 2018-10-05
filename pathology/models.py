"""
Models for pathology
"""
import re
from django.db import models
from opal.models import (
    PatientSubrecord, UpdatesFromDictMixin, ToDictMixin, TrackedModel
)
from pathology.pathology_categories import PathologyCategory
from jsonfield import JSONField


def is_numeric(some_value):
    """
    float will translate e for example as an expenential so we use regex
    """
    regex = r'^[0-9][0-9.]*$'
    return re.match(regex, some_value)


class PathologyTest(PatientSubrecord):
    category_name = models.CharField(max_length=256, default="default")
    name = models.CharField(max_length=256, default="default")
    datetime_ordered = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=256, blank=True, null=True)

    @property
    def category(self):
        return PathologyCategory.get(self.category_name)(self)

    def update_from_dict(self, data, *args, **kwargs):
        self.category_name = data.pop("category_name", "default")
        self.category.update_from_dict(data, *args, **kwargs)

    def to_dict(self, *args, **kwargs):
        return self.category.to_dict(*args, **kwargs)


class Observation(
    UpdatesFromDictMixin, ToDictMixin, TrackedModel, models.Model
):
    _icon = "fa fa-crosshars"
    _advanced_searchable = False
    _exclude_from_extract = True

    datetime_received = models.DateTimeField(blank=True, null=True)
    result = models.CharField(max_length=256, default="", blank=True)
    result_number = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=256, default="", blank=True)
    code = models.CharField(max_length=256, default="", blank=True)
    test = models.ForeignKey(PathologyTest)
    reference_range_min = models.FloatField(blank=True, null=True)
    reference_range_max = models.FloatField(blank=True, null=True)
    units = models.CharField(max_length=256, default="", blank=True)
    data_absent_reason = models.TextField(blank=True, default="")
    comment = models.TextField(blank=True, default="")
    consistency_token = models.CharField(max_length=8)

    class Meta:
        ordering = ["-datetime_received"]


    def save(self, *args, **kwargs):
        """ Where possible we convert numeric to numeric number
            so that we can query it by the database.
        """
        if is_numeric(self.result):
            self.result_number = float(self.result)

        super(Observation, self).save(*args, **kwargs)