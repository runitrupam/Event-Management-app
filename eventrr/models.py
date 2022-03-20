from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Event(models.Model):
    class Meta:
        unique_together = (('event_name', 'desc'),)
    window_choices = (
        (1, 'Not Booked'),
        (2, 'Ready For Booking'),
        (3, 'Booking on '),
        (4, 'Booking over')
    )
    event_name = models.CharField(max_length=15)
    desc = models.CharField(max_length=215)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices = window_choices, default=1)
    max_seats = models.IntegerField(default = 10)
    def __str__(self):
        return self.event_name
class ListEvents(models.Model):
   
    event = models.ForeignKey(Event, on_delete=models.CASCADE,unique = True)
    booking_start = models.DateTimeField(default = None)
    booking_end = models.DateTimeField(default = None)

    price_per_seat = models.IntegerField(default = 100)
    seats_avaialble = models.IntegerField(default = 100)
    
    def __str__(self):
        return self.event.event_name
class Ticket(models.Model):
    class Meta:
        unique_together = (('ListEvents', 'user'),)
        
    ticket_id =  models.AutoField(primary_key=True)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    ListEvents = models.ForeignKey(ListEvents,default = None , on_delete=models.CASCADE)
    seats_booked = models.IntegerField(default = 0)
    total_price = models.IntegerField(default = 0)
    def __str__(self):
        return self.ListEvents.event.event_name + self.user.username