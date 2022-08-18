from django.test import TestCase
from webapp import models
from rest_framework.test import APIClient


class CreateSummaryTestCase(TestCase):
    def setUp(self):
        self.room = models.Room.objects.create(id=697613873)
        self.profile = models.Profile.objects.create(id=470374164, discord_name="test")

        models.Summary.objects.create(id=787274094,content="summary1",room=self.room,profile=self.profile)



    def test_id(self):
        summary = models.Summary.objects.get(id=787274094)
        self.assertEqual(summary.id, 787274094)

    def test_content(self):
        summary = models.Summary.objects.get(id=787274094)
        self.assertEqual(summary.content, "summary1")

    def test_profile(self):
        summary = models.Summary.objects.get(id=787274094)
        self.assertEqual(summary.profile, self.profile)

    def test_room(self):
        summary = models.Summary.objects.get(id=787274094)
        self.assertEqual(summary.room, self.room)

    def test_get_api(self):
        req = self.client.get("/api/summaries/", format='json')
        self.assertEqual(req.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(req.status_code))

