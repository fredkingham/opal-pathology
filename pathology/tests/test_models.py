from opal.core.test import OpalTestCase
from pathology.models import PathologyTest


class PathologyTestUpdateTestCase(OpalTestCase):
    def test_generic_update(self):
        data = {
            "observations": [
                dict(result="something")
            ],
            "extras": dict(lab_attendent="Wilma")
        }

        to_test = PathologyTest()
        to_test.update_from_dict(data, self.user)

        pt = PathologyTest.objects.get()
        obs = pt.observation_set.get()

        self.assertEqual(
            obs.result, "something"
        )
        self.assertEqual(
            pt.extras["lab_attendent"], "Wilma"
        )




    