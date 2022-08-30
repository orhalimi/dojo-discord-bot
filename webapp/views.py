""" this file used as a main feature of django, we can register views for specific urls """
import datetime
from django.shortcuts import render
from .models import Message, Room,Profile


def dashboard(request):
    """@dashboard view control on how we server the html and the date from the server"""
    date: str = request.GET.get("from_date")

    if date is None:
        all_messages = Message.objects.all().order_by("-created_at")
        all_rooms = Room.objects.all().order_by("-created_at")
        profiles = Profile.objects.all()
    else:
        c_date: object = datetime.datetime.now()
        c_date_format: str = f"{c_date.year}-{c_date.month}-{c_date.day}"
        
        all_messages = Message.objects.filter(
            created_at__range=[date, c_date_format]
        ).order_by("-created_at")

        all_rooms = Room.objects.filter(
            created_at__range=[date, c_date_format]

        ).order_by("-created_at")

    context = {"messages": all_messages, "rooms": all_rooms}
    return render(request, "dashboard.html", context)
