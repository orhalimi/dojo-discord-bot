from rest_framework import serializers

from webapp.models import (
    Member, 
    Profile, 
    Room, 
    Event, 
    RoomProfileRole, 
    Summary, 
    Message
)

# Serializers define the API representation.
class MemberSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = Member
        fields = ['id', 'profile', 'role', 'room']



class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        ## CR: do we need updated_at? wouldn't it be auto-populated?
        fields = ['id', 'profiles', 'updated_at']



class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'discord_name']



class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'message','room', 'target_date_and_time']



class RoomProfileRoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RoomProfileRole
        fields = ['id', 'name', 'profile']



class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'profile', 'room']



class SummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Summary
        fields = ['id', 'content', 'profile', 'room']

