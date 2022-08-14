from django.shortcuts import render, redirect
from .models import Message, Room


def Dashboard(request):
    messages = Message.objects.all()
    rooms = Room.objects.all()

    context = {"messages": messages, "rooms":rooms}
    
    return render(request, "dashboard.html", context)