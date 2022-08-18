from webapp import models

from django.test import TestCase
from rest_framework.test import APIClient

class CreateProfileTestCase(TestCase):
    def setUp(self):
        models.Profile.objects.create(id=186287607, discord_name="test", real_name="Harry Potter")


    def test_id(self):
        profile = models.Profile.objects.get(id=186287607)
        self.assertEqual(profile.id, 186287607)

    def test_discord_name(self):
        profile = models.Profile.objects.get(id=186287607)
        self.assertEqual(profile.discord_name, "test")

    def test_real_name(self):
        profile = models.Profile.objects.get(id=186287607)
        self.assertEqual(profile.real_name, "Harry Potter")

    def test_get_api(self):
        req = self.client.get("/api/profiles/", format='json')
        self.assertEqual(req.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(req.status_code))

