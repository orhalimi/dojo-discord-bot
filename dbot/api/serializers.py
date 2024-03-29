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
        fields = ['profile', 'role', 'room']


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ['id', '__str__']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'discord_name','real_name','phone_number','subscribed']


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['room', 'target_date_and_time']


class RoomProfileRoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RoomProfileRole
        fields = ['id', 'name']


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ['created_at', 'content', 'profile', 'room']


class SummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Summary
        fields = ['created_at', 'id', 'content', 'profile', 'room']



