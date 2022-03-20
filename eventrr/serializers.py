from rest_framework import serializers
from .models import *
class EventSerialize(serializers.Serializer):
    id = serializers.IntegerField()
    event_name = serializers.CharField(max_length=15)
    desc = serializers.CharField(max_length=215)
    status = serializers.IntegerField()
    max_seats = serializers.IntegerField(default = 10)

class ListEventSerialize(serializers.ModelSerializer):
    class Meta:
        model = ListEvents
        #field = '__all__'
        fields = ['id', 'event','booking_start', 'booking_end', 'price_per_seat', 'seats_avaialble',]