from django.contrib import admin
from django.conf import settings
from webapp.models import Member, Message, Room, Summary, Member, Event, Profile
from django.contrib.auth.models import User, Group
from django.utils.html import format_html

# remove Authentication and Authorization section
admin.site.unregister(User)
admin.site.unregister(Group)


# document settings.
admin.site.site_header = settings.SITE_HEADER
admin.site.site_title = settings.SITE_TITLE
admin.site.index_title = settings.INDEX_TITLE



# Inlines Classes
class MemberTable(admin.StackedInline):
    model = Member
    readonly_fields = ('profile', 'role', 'room')
    extra = 0



class MessageTable(admin.StackedInline):
    model = Message
    readonly_fields = ('content', 'profile','created_at')
    extra = 0



class SummarieTable(admin.StackedInline):
    model = Summary
    readonly_fields = ('content', 'profile')
    extra = 0
    


class EventTable(admin.StackedInline):
    model = Event
    readonly_fields = ['target_date_and_time']
    extra = 0

    


# Admin Classes
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    ## CR: created_at sounds important
    ## CR: if this is going to be used a lot, maybe some event statistics?
    ##     how many happened out of how many weeks, did the last one happen,
    ##     is there a next one scheduled?
    
    list_display = [
        '__str__',
        'get_message_amount',
        'updated_at',
        'created_at',
        'id']
    
    list_filter =  ['created_at']
    readonly_fields = ('id','updated_at', 'created_at')
    fields = ['id', 'created_at', 'updated_at' ]

    search_fields = ['member__profile__discord_name']


    inlines = [MemberTable,
               MessageTable,
               SummarieTable,
               EventTable]
    



@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at','room','profile')    
    list_display = ['id','__str__','role','room', 'created_at']
    list_filter =  ['created_at']
    search_fields = ['profile__discord_name']
    list_display_links = ['__str__']
    
    fields = ['id', 'created_at', 'role', 'room', 'profile']


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at','content','profile','room')    
    list_display = ['__str__','profile','room','created_at']
    list_filter =  ['created_at']
    fields = ['id', 'created_at', 'content', 'profile', 'room']



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at','content','profile','room')    
    list_display = ['__str__','profile','room','created_at']
    list_filter =  ['created_at']
    search_fields = ['content']
    fields = ['id', 'created_at', 'content', 'profile', 'room']



@admin.register(Event)
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at','room','target_date_and_time')    
    list_display = ['__str__','created_at','room','target_date_and_time']
    list_filter =  ['created_at']
    search_fields = ['content']
    fields = ['id', 'created_at', 'room','target_date_and_time']