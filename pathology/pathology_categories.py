from opal.core.discoverable import DiscoverableFeature
from opal.core import serialization


class PathologyCategory(DiscoverableFeature):
    module_name = "pathology_categories"

    def __init__(self, model):
        self.model = model

    def update_from_dict(self, data, user, *args, **kwargs):
        field_names = self._get_fieldnames_to_serialize()
        field_names.remove("observations")
        super(self.model.__class__, self.model).update_from_dict(data, user, *args, **kwargs)
        self.model.save()
        self.model.observations = self.update_observations(data.pop("observations"), [])

    def get_or_create_observation(observation_dict, *args, **kwargs):
        from pathology.models import PathologyObservation

        if "id" in observation_dict:
            return self.model.observation_set.get(id=observation_dict["id"]), True
        else:
            return PathologyObservation.objects.create(test=self.model), False
        
    def update_observations(observations, user, *args, **kwargs):
        for observation_dict in observations:
            observation.update_from_dict(observation_dict, user, *args, **kwargs)

    # def to_dict(self, *args, **kwargs):
    #     return dict(
    #         extras=self.model.extras,
    #         datetime_ordered=self.datetime_ordered,
    #         observations=[i.to_dict(*args, **kwargs) for i in self.model.observation_set.all()]
    #     )

    @classmethod
    def get_display_template(cls, *args, **kwargs):
        return cls.get_display_template(*args, **kwargs)

    @classmethod
    def get_detail_template(cls, *args, **kwargs):
        return "records/pathology_test.html"

    @classmethod
    def get_form_template(cls, *args, **kwargs):
        return "forms/pathology_test_form.html"


class DefaultCategory(PathologyCategory):
    display_name = "Default"
    slug = "default"

    
