from django.contrib import admin
from django.db import models



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True



class Room(BaseModel):
    ## CR: need a way to know the discord room id
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
        ## CR: maybe a good idea to wrap with <>
        return f'{mentor} mentor {student}'
            
    # @admin.display(description='Events')
    # def get_events(self):
    #     events = Event.objects.filter(room = self.id).__len__()
    #     return events
        
    @admin.display(description='Messages')
    def get_message_amount(self):
        ## CR: x.__len__() => len(x) or x.count()
        message_amount = Message.objects.filter(room = self.id).__len__()
        return message_amount





class Member(BaseModel):
    profile = models.ForeignKey('webapp.Profile', on_delete=models.CASCADE)
    ## CR: I think I would have gone with static roles (as string with `choices` but sure lets do this)
    ## CR: Are you sure you want on_delete=models.CASCADE
    role = models.ForeignKey('webapp.RoomProfileRole', on_delete=models.CASCADE)
    room = models.ForeignKey('webapp.Room', on_delete=models.CASCADE)
    
    def __str__(self):
        ## CR: would be nice to be able to distinguish a profile from a membership I think
        ## CR: maybe a good idea to wrap with <>
        return self.profile.discord_name



class Profile(BaseModel):
    ## CR: we want to know who this person is, lets add a name field? Also maybe phone?
    discord_name = models.CharField(max_length=128)
    
    def __str__(self):
        ## CR: maybe a good idea to wrap with <>
        return self.discord_name




class RoomProfileRole(models.Model):
    name = models.CharField(max_length=64)
    ## CR: are you sure this is supposed to be here?
    profile = models.ManyToManyField("webapp.Profile", through='Member')
    
    def __str__(self):
        return self.name




class Message(BaseModel):
    ## CR: message reflects a discord message, we don't know what it's length limit is/will be.
    ##     Better not have a limit ourselves (can use TextField() instead)
    content = models.CharField(max_length=2000)
    ## CR: on_delete=models.CASCADE can only end in tears (usually, here included)
    ##     Losing information tends to be... sad for all involved
    profile = models.ForeignKey("webapp.Profile", on_delete=models.CASCADE)
    room = models.ForeignKey('webapp.Room', on_delete=models.CASCADE)

    def __str__(self):
        ## CR: maybe a good idea to wrap with <>
        ## CR: maybe more informative to have a bit of the content? content[:50] or something
        return f"Message {self.id}"




class Summary(BaseModel):
    ## CR: We _want_ long summaries. Better not have a limit ourselves (can use TextField() instead)
    content = models.CharField(max_length=2000)
    profile = models.ForeignKey("webapp.Profile", on_delete=models.CASCADE)
    room = models.ForeignKey('webapp.Room', on_delete=models.CASCADE)
    ## CR: do we want summaries to be linked to their events or not? not sure

    def __str__(self):
        ## CR: maybe a good idea to wrap with <>
        ## CR: maybe more informative to have a bit of the content? content[:50] or something
        return f"Summary {self.id}"



class Event(BaseModel):
    ## CR: who populates this? with what? are there different types of events?
    name = models.CharField(max_length=64)
    ## CR: is there anything to record here?
    ## CR: why limit length?
    message = models.CharField(max_length=1024)
    room = models.ForeignKey("webapp.Room", on_delete=models.CASCADE)
    target_date_and_time = models.DateTimeField() # validation logic?

    def __str__(self):
        ## CR: maybe a good idea to wrap with <>
        ## CR: maybe more informative to have the date?
        return self.name
