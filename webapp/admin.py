from django.contrib import admin
from django.conf import settings
from webapp.models import Member, Message, Room, Summary, Member, Event
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
    readonly_fields = ('content', 'profile')
    extra = 0

## CR: typo
## CR: typo
class SummarieTabel(admin.StackedInline):
    model = Summary
    readonly_fields = ('content', 'profile')
    extra = 0
    
## CR: typo
class EventTabel(admin.StackedInline):
    model = Event
    readonly_fields = ('name', 'message', 'target_date_and_time')
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
        'updated_at']
    
    list_filter =  ['created_at']
    readonly_fields = ('id', 'updated_at', 'created_at')
    fieldsets = (
        ('Room Details', {
            'fields': ('id', ('created_at', 'updated_at'))
        }),)

    ## CR: if profiles has a name, should be searchable too
    search_fields = ['profiles__discord_name']


    inlines = [MemberTable,
               MessageTable,
               SummarieTabel,
               EventTabel]
    
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    # MemberAdmin.list_display, room retun the to string method insted of the room id?
    readonly_fields = ('id', 'created_at','role','room','profile')    
    list_display = ['id','__str__','role','room', 'created_at']
    list_filter =  ['created_at']
    ## CR: if profiles has a name, should be searchable too
    search_fields = ['profile__discord_name']
    list_display_links = ['__str__']
    

    fieldsets = (
        ('Member Details', {
            'fields': ('id', ('created_at'), 'role','room','profile')
        }),
    )