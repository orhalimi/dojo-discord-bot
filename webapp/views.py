""" this file used as a main feature of django, we can register views for specific urls """
from asyncio import events
import datetime
from django.shortcuts import render
from .models import Message, Room, Profile, Summary, Event
from django.utils import timezone
import pytz


def dashboard(request):
    timezone.now()
    """@dashboard view control on how we server the html and the date from the server"""
    date: str = request.GET.get("from_date")
    all_rooms = Room.objects.all().order_by("-created_at")
    all_messages = Message.objects.all().order_by("created_at")
    all_summaries = Summary.objects.all().order_by("created_at")
    all_events = Event.objects.all().order_by("created_at")

    if date != None:
        c_date: object = datetime.datetime.now(tz=pytz.UTC)
        c_date_format: str = f"{c_date.year}-{c_date.month}-{c_date.day}"

        all_messages = Message.objects.filter(
            created_at__range=[date, c_date_format]
        ).order_by("created_at")

    context = {"messages": all_messages, "rooms": all_rooms,
               "summaries": all_summaries, "events": all_events}
    return render(request, "dashboard.html", context)
