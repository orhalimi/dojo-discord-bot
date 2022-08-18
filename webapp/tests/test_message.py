from django.test import TestCase
from webapp import models

from rest_framework.test import APIClient

class CreateMessageTestCase(TestCase):
    def setUp(self):
        self.room = models.Room.objects.create(id=697613873)
        self.profile = models.Profile.objects.create(id=470374164, discord_name="test")

        models.Message.objects.create(id=563858793,content="test",room=self.room,profile=self.profile)


    def test_id(self):
        message = models.Message.objects.get(id=563858793)
        self.assertEqual(message.id, 563858793)

    def test_content(self):
        message = models.Message.objects.get(id=563858793)
        self.assertEqual(message.content, "test")

    def test_profile(self):
        message = models.Message.objects.get(id=563858793)
        self.assertEqual(message.profile, self.profile)

    def test_room(self):
        message = models.Message.objects.get(id=563858793)
        self.assertEqual(message.room, self.room)

    def test_get_api(self):
        req = self.client.get("/api/messages/", format='json')
        self.assertEqual(req.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(req.status_code))

