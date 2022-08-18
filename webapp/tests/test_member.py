from django.test import TestCase
from webapp import models
from rest_framework.test import APIClient

class CreateMemberTestCase(TestCase):
    def setUp(self):
        self.room = models.Room.objects.create(id=697613873)
        self.profile = models.Profile.objects.create(id=470374164, discord_name="test")
        self.role_student = models.RoomProfileRole.objects.get(id=1)
        models.Member.objects.create(id=481398719, role=self.role_student, room=self.room, profile=self.profile)

    def test_id(self):
        member = models.Member.objects.get(id=481398719)
        self.assertEqual(member.id, 481398719)

    def test_role(self):
        member = models.Member.objects.get(id=481398719)
        self.assertEqual(member.role, self.role_student)

    def test_profile(self):
        member = models.Member.objects.get(id=481398719)
        self.assertEqual(member.profile, self.profile)

    def test_room(self):
        member = models.Member.objects.get(id=481398719)
        self.assertEqual(member.room, self.room)

    def test_get_api(self):
        req = self.client.get("/api/members/", format='json')
        self.assertEqual(req.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(req.status_code))
