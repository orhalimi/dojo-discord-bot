from django.shortcuts import render, redirect
from .models import Message


def Dashboard(request):
    messages = Message.objects.all()
    context = {"messages": messages}
    
    return render(request, "dashboard.html", context)