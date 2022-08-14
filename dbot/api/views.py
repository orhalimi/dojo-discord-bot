from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import (
    MemberSerializer,
    RoomSerializer,
    ProfileSerializer,
    EventSerializer,
    MessageSerializer,
    RoomProfileRoleSerializer,
    SummarySerializer
)
from webapp.models import (
    Member, 
    Profile, 
    Room, 
    Event, 
    RoomProfileRole, 
    Summary, 
    Message
)

# ViewSets define the view behavior.
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class RoomProfileRoleViewSet(viewsets.ModelViewSet):
    queryset = RoomProfileRole.objects.all()
    serializer_class = RoomProfileRoleSerializer

class SummaryViewSet(viewsets.ModelViewSet):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer

