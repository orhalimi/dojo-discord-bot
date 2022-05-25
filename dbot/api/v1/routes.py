from rest_framework import routers
# Routers provide an easy way of automatically determining the URL conf.

from dbot.api.v1.views import (
    MemberViewSet,
    RoomViewSet,
    ProfileViewSet,
    EventViewSet,
    MessageViewSet,
    RoomProfileRoleViewSet,
    SummaryViewSet
)

router = routers.DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'events', EventViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'roles', RoomProfileRoleViewSet)
router.register(r'summaries', SummaryViewSet)
