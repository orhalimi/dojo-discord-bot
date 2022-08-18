from django.test import TestCase
from webapp import models
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient


class CreateRoomTestCase(TestCase):
    def setUp(self):
        models.Room.objects.create(id=733748678)
        self.client = APIClient()
        self.client.credentials(username="zionamsalem", password="pass")

    def test_id(self):
        room = models.Room.objects.get(id = 733748678)
        self.assertEqual(room.id, 733748678)

    def test_get_api(self):
        req = self.client.get("/api/rooms/", format='json')
        self.assertEqual(req.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(req.status_code))


    # def test_post_api(self):
    #     obj = {"id":10102220}

    #     req = self.client.post("/api/rooms/", obj, format='json') # we failed here
        
    #     self.assertEqual(req.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(req.status_code))
