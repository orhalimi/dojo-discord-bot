from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

#TODO:
# 1. get messages from API  - 
# 2. get members and rooms names from api
# 3. filter room by user choice 
# 4. show messages relevant to that room only
# 5. display user that sent each message next to message
# 6. create a table and arrange the items nicely on it and a filter drop down list for room name.

members = []
rooms = []
messages_list = []
profiles = []

def get_data(endpoint):
    url = f"http://127.0.0.1:8000/api/{endpoint}/"
    response = requests.get(url)
    json_data = json.loads(response.text)
    print(json_data)
    return json_data

def get_rooms():
    rooms = get_data('rooms')
    return rooms
        
def get_members():
    members = get_data('members')
    return members
def get_profiles():
    profiles = get_data('profiles')
    return profiles

def get_messages():
    messages_list = get_data('messages')
    return messages_list


def messages(request):
    get_profiles()
    return HttpResponse(profiles)
