''' the admin moudle let us design and change the admin panael  '''

from django.contrib import admin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from webapp.models import Member, Message, Room, Summary, Event

# remove Authentication and Authorization section
admin.site.unregister(get_user_model())
admin.site.unregister(Group)

# document settings.
admin.site.site_header = settings.SITE_HEADER
admin.site.site_title = settings.SITE_TITLE
admin.site.index_title = settings.INDEX_TITLE

class MemberTable(admin.StackedInline):
    ''' inherent from StackInLine, consume a model and shows the data as simple table '''

    model = Member
    readonly_fields = ('profile', 'role', 'room')
    extra = 0

class MessageTable(admin.StackedInline):
    ''' consume a model and shows the data as simple table '''

    model = Message
    readonly_fields = ('content', 'profile','created_at')
    extra = 0

class SummarieTable(admin.StackedInline):
    ''' consume a model and shows the data as simple table '''

    model = Summary
    readonly_fields = ('content', 'profile')
    extra = 0

class EventTable(admin.StackedInline):
    ''' consume a model and shows the data as simple table '''
    model = Event
    readonly_fields = ['target_date_and_time']
    extra = 0

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    ''' define the stracture of the Room moudle in the admin panel '''

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
    inlines = [MemberTable,MessageTable,SummarieTable,EventTable]


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    ''' define the stracture of the Member moudle in the admin panel '''

    readonly_fields = ('id', 'created_at','room','profile')
    list_display = ['id','__str__','role','room', 'created_at']
    list_filter =  ['created_at']
    search_fields = ['profile__discord_name']
    list_display_links = ['__str__']
    fields = ['id', 'created_at', 'role', 'room', 'profile']


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    ''' define the stracture of the Summary moudle in the admin panel '''

    readonly_fields = ('id', 'created_at','content','profile','room')
    list_display = ['__str__','profile','room','created_at']
    list_filter =  ['created_at']
    fields = ['id', 'created_at', 'content', 'profile', 'room']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    ''' define the stracture of the Message moudle in the admin panel '''

    readonly_fields = ('id', 'created_at','content','profile','room')
    list_display = ['__str__','profile','room','created_at']
    list_filter =  ['created_at']
    search_fields = ['content']
    fields = ['id', 'created_at', 'content', 'profile', 'room']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    ''' define the stracture of the Event moudle in the admin panel '''
    
    readonly_fields = ('id', 'created_at','room','target_date_and_time')
    list_display = ['__str__','created_at','room','target_date_and_time']
    list_filter =  ['created_at']
    search_fields = ['content']
    fields = ['id', 'created_at', 'room','target_date_and_time']
