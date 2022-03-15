from django.contrib import admin
from .models import Ticket, Event ,  ListEvents

# Register your models here.
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(ListEvents)
