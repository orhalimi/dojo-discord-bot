from django.contrib import admin
from django.db import models



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True



class Room(BaseModel):
    id = models.PositiveIntegerField(primary_key = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        qet_members = Member.objects.filter(room = self.id)
        student , mentor = None, None
        for mem in qet_members:
            if(mem.role.name == "Student"):
                student = mem
            if(mem.role.name == "Mentor"):
                mentor = mem

        ## CR: maybe a good idea to wrap with <>
        return f'{mentor} mentor {student}'

    def __id__(self):
        return self.id

            
    @admin.display(description='Messages')
    def get_message_amount(self):
        message_amount = len(Message.objects.filter(room = self.id))
        return message_amount



class Member(BaseModel):
    profile = models.ForeignKey('webapp.Profile', null=True, on_delete=models.SET_NULL)
    ## CR: I think I would have gone with static roles (as string with `choices` but sure lets do this)
    role = models.ForeignKey('webapp.RoomProfileRole', null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey('webapp.Room', null=True, on_delete=models.SET_NULL)
    


    def __str__(self):
        ## CR: would be nice to be able to distinguish a profile from a membership I think
        ## CR: maybe a good idea to wrap with <>
        return str(self.profile)



class Profile(BaseModel):
    id = models.PositiveIntegerField(primary_key = True)
    discord_name = models.CharField(max_length=128)
    real_name = models.CharField(max_length=128, null=True)
    phone_number = models.CharField(max_length=16, null=True)
    subscribed = models.BooleanField(default=True)
    


    def __str__(self):
        ## CR: maybe a good idea to wrap with <>
        return self.discord_name

    def getName(self):
        return self.discord_name



class RoomProfileRole(models.Model):
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return self.name



class Message(BaseModel):
    content = models.TextField()
    profile = models.ForeignKey("webapp.Profile", null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey('webapp.Room', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        ## CR: maybe a good idea to wrap with <>
        return self.content[:50]



class Summary(BaseModel):
    content = models.TextField()
    profile = models.ForeignKey("webapp.Profile", on_delete=models.CASCADE)
    room = models.ForeignKey('webapp.Room', on_delete=models.CASCADE)
    ## CR: do we want summaries to be linked to their events or not? not sure

    def __str__(self):
        ## CR: maybe a good idea to wrap with <>
        return self.content[:50]

    class Meta:
        verbose_name_plural = "Summaries"
        
class Event(BaseModel):
    
    room = models.ForeignKey("webapp.Room", null=True, on_delete=models.SET_NULL)
    target_date_and_time = models.DateTimeField()

    def __str__(self):
        ## CR: maybe a good idea to wrap with <>
        return "Weekly Meeting"


