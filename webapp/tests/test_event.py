from dbot.api import views
from webapp import models

from django.utils.timezone import now
from django.test import TestCase
from rest_framework.test import APIClient


class CreateEventTestCase(TestCase):
    def setUp(self):
        self.room = models.Room.objects.create(id=462822593)
        self.target_date_and_time = now()
        models.Event.objects.create(id=481151389, room=self.room, target_date_and_time=self.target_date_and_time)

    def test_id(self):
        event = models.Event.objects.get(id=481151389)
        self.assertEqual(event.id, 481151389)

    def test_time(self):
        event = models.Event.objects.get(id=481151389)
        self.assertEqual(event.target_date_and_time, self.target_date_and_time)

    def test_room(self):
        event = models.Event.objects.get(id=481151389)
        self.assertEqual(event.room, self.room)

    def test_get_api(self):
        req = self.client.get("/api/events/", format='json')
        self.assertEqual(req.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(req.status_code))
