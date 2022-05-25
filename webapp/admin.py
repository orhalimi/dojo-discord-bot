from django.contrib import admin
from django.conf import settings
from webapp.models import Member, Message, Room, Summary, Member
from django.contrib.auth.models import User, Group

# remove Authentication and Authorization section
admin.site.unregister(User)
admin.site.unregister(Group)

# document settings.
admin.site.site_header = settings.SITE_HEADER
admin.site.site_title = settings.SITE_TITLE
admin.site.index_title = settings.INDEX_TITLE

# Inlines Classes
class MemberTable(admin.TabularInline):
    model = Member
    readonly_fields = ('profile', 'role', 'room')
    extra = 0

class MessageTable(admin.TabularInline):
    model = Message
    readonly_fields = ('content', 'profile', 'room')
    extra = 0

class SummarieTabel(admin.TabularInline):
    model = Summary
    readonly_fields = ('content', 'profile', 'room')
    extra = 0
    
    
# Admin Classes
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        # '__str__',
        # 'get_supermentor',
        'get_message_amount',
        'get_events',
        'updated_at']
    
    list_filter =  ['created_at']
    readonly_fields = ('id', 'updated_at', 'created_at')
    fieldsets = (
        ('Room Details', {
            'fields': ('id', ('created_at', 'updated_at'))
        }),)

    inlines = [MemberTable,
               MessageTable,
               SummarieTabel]
    
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    # MemberAdmin.list_display, room retun the to string method insted of the room id?
    readonly_fields = ('id', 'created_at','role','room','profile')    
    list_display = ['__str__','role','room']
    list_filter =  ['created_at']
    fieldsets = (
        ('Member Details', {
            'fields': ('id', ('created_at'), 'role','room','profile')
        }),
    )