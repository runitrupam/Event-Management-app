from django.contrib import admin
from .models import Ticket, Event ,  ListEvents

# Register your models here.
#admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(ListEvents)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id','event_name', 'desc', 'status', 'max_seats']
