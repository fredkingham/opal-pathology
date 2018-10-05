from opal.core.test import OpalTestCase
from opal.core import exceptions
from pathology.models import PathologyTest


class AbstractPathology(OpalTestCase):
    def setUp(self):
        self.patient, _ = self.new_patient_and_episode_please()


class PathologyTestDefaultUpdateTestCase(AbstractPathology):
    """
    Tests the default update behavour for the Pathology Test
    """
    def test_generic_update(self):
        data = {
            "patient_id": self.patient.id,
            "observation_set": [
                dict(result="something")
            ],
        }

        to_test = PathologyTest()
        to_test.update_from_dict(data, self.user)

        pt = PathologyTest.objects.get()
        obs = pt.observation_set.get()

        self.assertEqual(
            obs.result, "something"
        )

        self.assertIsNotNone(obs.consistency_token)
        self.assertIsNotNone(to_test.consistency_token)

    def test_consistency_token_on_pathology(self):
        pathology_test = PathologyTest.objects.create(
            patient=self.patient, consistency_token="1"
        )
        pathology_test.observation_set.create(
            result="something", consistency_token="2"
        )
        data = {
            "patient_id": self.patient.id,
            "id": pathology_test.id,
            "observation_set": [
                dict(
                    result="something",
                    id=pathology_test.observation_set.first().id
                )
            ],
        }

        with self.assertRaises(exceptions.MissingConsistencyTokenError) as er:
            pathology_test.update_from_dict(data, self.user)

        expected = 'Missing field (consistency_token) for PathologyTest'
        self.assertEqual(
            str(er.exception), expected
        )

    def test_consistency_token_on_observation(self):
        pathology_test = PathologyTest.objects.create(
            patient=self.patient, consistency_token="1"
        )
        pathology_test.observation_set.create(
            result="something", consistency_token="2"
        )
        data = {
            "patient_id": self.patient.id,
            "id": pathology_test.id,
            "consistency_token": "1",
            "observation_set": [
                dict(
                    result="something",
                    id=pathology_test.observation_set.first().id
                )
            ],
        }

        with self.assertRaises(exceptions.MissingConsistencyTokenError) as er:
            pathology_test.update_from_dict(data, self.user)

        expected = 'Missing field (consistency_token) for Observation'
        self.assertEqual(
            str(er.exception), expected
        )


class PathologyTestDefaultToDictTestCase(AbstractPathology):
    """
    Tests the default to dict behavoiur of the pathology model
    """

    def setUp(self):
        self.patient, _ = self.new_patient_and_episode_please()

    def test_consistency_token_on_pathology(self):
        self.maxDiff = None
        pathology_test = PathologyTest.objects.create(
            patient=self.patient, consistency_token="1"
        )
        pathology_test.observation_set.create(
            result="something", consistency_token="2"
        )
        expected = {
            'category_name': 'default',
            'consistency_token': '1',
            'created': None,
            'created_by_id': None,
            'datetime_ordered': None,
            'id': pathology_test.id,
            'name': 'default',
            'observation_set': [
                {
                    'code': u'',
                    'comment': u'',
                    'consistency_token': u'2',
                    'created': None,
                    'created_by_id': None,
                    'data_absent_reason': u'',
                    'datetime_received': None,
                    'id': pathology_test.observation_set.get().id,
                    'name': u'',
                    'reference_range_max': None,
                    'reference_range_min': None,
                    'result': u'something',
                    'result_number': None,
                    'test_id': 1,
                    'units': u'',
                    'updated': None,
                    'updated_by_id': None
                }
            ],
            'patient_id': self.patient.id,
            'status': None,
            'updated': None,
            'updated_by_id': None
        }
        self.assertEqual(pathology_test.to_dict(self.user), expected)


class ObservationTestCase(AbstractPathology):
    def setUp(self):
        super(ObservationTestCase, self).setUp()
        self.pathology_test = PathologyTest.objects.create(
            patient=self.patient, consistency_token="1"
        )

    def test_result_float(self):
        self.pathology_test.observation_set.create(
            result="1000", consistency_token="2"
        )
        observation = self.pathology_test.observation_set.get()
        self.assertEqual(observation.result, "1000")
        self.assertEqual(observation.result_number, 1000)

    def test_result_not_float(self):
        self.pathology_test.observation_set.create(
            result="something", consistency_token="2"
        )
        observation = self.pathology_test.observation_set.get()
        self.assertEqual(observation.result, "something")
        self.assertIsNone(observation.result_number)

