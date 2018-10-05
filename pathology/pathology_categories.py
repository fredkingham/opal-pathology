from opal.core.discoverable import DiscoverableFeature
from opal.core import serialization


class PathologyCategory(DiscoverableFeature):
    module_name = "pathology_categories"

    def __init__(self, model):
        self.model = model

    def to_dict(self, user):
        result = super(self.model.__class__, self.model).to_dict(user)
        result["observation_set"] = self.to_dict_observations(user)
        return result

    def to_dict_observations(self, user):
        return [i.to_dict(user) for i in self.model.observation_set.all()]

    def update_from_dict(self, data, user, *args, **kwargs):
        observation_set = data.pop("observation_set")
        force = kwargs.get("force", False)
        super(self.model.__class__, self.model).update_from_dict(
            data, user, *args, **kwargs
        )
        self.model.save()
        self.model.observations = self.update_observations(
            observation_set, user, force=force
        )

    def get_or_create_observation(self, observation_dict, user):
        from pathology.models import Observation

        if "id" in observation_dict:
            return self.model.observation_set.get(id=observation_dict["id"]), True
        else:
            return Observation.objects.create(test=self.model), False

    def update_observation(
        self, observation, observation_dict, user, force=False
    ):
        observation.update_from_dict(observation_dict, user, force=force)

    def update_observations(self, observation_set, user, force=False):
        for observation_dict in observation_set:
            observation, _ = self.get_or_create_observation(
                observation_dict, user
            )
            self.update_observation(
                observation, observation_dict, user, force=force
            )

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

    
