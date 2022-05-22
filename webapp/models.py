from django.contrib import admin
from django.db import models



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True



class Room(BaseModel):
    profiles = models.ManyToManyField('webapp.Profile', through='Member')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        qet_members = Member.objects.filter(room = self.id)
        student , mentor = None, None
        for mem in qet_members:
            if(mem.role.name == "Student"):
                student = mem
            if(mem.role.name == "Mentor"):
                mentor = mem
                
        return f'{mentor} mentor {student}'
            
    @admin.display(description='Events')
    def get_events(self):
        events = Event.objects.filter(room = self.id).__len__()
        return events
        
    @admin.display(description='Messages')
    def get_message_amount(self):
        message_amount = Message.objects.filter(room = self.id).__len__()
        return message_amount





class Member(BaseModel):
    profile = models.ForeignKey('webapp.Profile', on_delete=models.CASCADE)
    role = models.ForeignKey('webapp.RoomProfileRole', on_delete=models.CASCADE)
    room = models.ForeignKey('webapp.Room', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.profile.discord_name



class Profile(BaseModel):
    discord_name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.discord_name




class RoomProfileRole(models.Model):
    name = models.CharField(max_length=64)
    profile = models.ManyToManyField("webapp.Profile", through='Member')
    
    def __str__(self):
        return self.name




class Message(BaseModel):
    content = models.CharField(max_length=2000)
    profile = models.ForeignKey("webapp.Profile", on_delete=models.CASCADE)
    room = models.ForeignKey('webapp.Room', on_delete=models.CASCADE)

    def __str__(self):
        return f"Message {self.id}"




class Summary(BaseModel):
    content = models.CharField(max_length=2000)
    profile = models.ForeignKey("webapp.Profile", on_delete=models.CASCADE)
    room = models.ForeignKey('webapp.Room', on_delete=models.CASCADE)

    def __str__(self):
        return f"Summary {self.id}"



class Event(BaseModel):
    name = models.CharField(max_length=64)
    message = models.CharField(max_length=1024)
    room = models.ForeignKey("webapp.Room", on_delete=models.CASCADE)
    target_date_and_time = models.DateTimeField() # validation logic?

    def __str__(self):
        return self.name
