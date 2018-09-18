"""
Models for pathology
"""
from django.db import models
from opal.models import PatientSubrecord, UpdatesFromDictMixin, ToDictMixin, TrackedModel
from pathology.pathology_categories import PathologyCategory
from jsonfield import JSONField


class PathologyTest(PatientSubrecord):
    category_name = models.CharField(max_length=256, default="default")
    name = models.CharField(max_length=256, default="default")
    datetime_ordered = models.DateTimeField(blank=True, null=True)
    extras = JSONField(blank=True, null=True)

    @property
    def category(self):
        return PathologyCategory.get(self.category_name)(self)

    def update_from_dict(self, data, *args, **kwargs):
        self.category_name = data.pop("category_name", "default")
        self.category.update_from_dict(data, *args, **kwargs)

    def to_dict(self, *args, **kwargs):
        return self.category.to_dict(*args, **kwargs)


class PathologyObservation(UpdatesFromDictMixin, ToDictMixin, TrackedModel, models.Model):
    _icon = "fa fa-crosshars"
    _advanced_searchable = False
    _exclude_from_extract = True

    datetime_received = models.DateTimeField(blank=True, null=True)
    result = models.CharField(max_length=256, default="", blank=True)
    result_number = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=256, default="", blank=True)
    code = models.CharField(max_length=256, default="", blank=True)
    test = models.ForeignKey(PathologyTest)
    extras = JSONField(blank=True, null=True)

    class Meta:
        ordering = ["-datetime_received"]

    def update_from_dict(self, data, *args, **kwargs):
        if is_numeric(data["result"]):
            self.result_number = float(data["result"])
        return super(PathologyObservation, self).update_from_dict(data, *args, **kwargs)