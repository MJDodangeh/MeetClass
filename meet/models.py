from django.db import models

from account.models import User

class Room(models.Model):
    capacity = models.IntegerField()

class ConfirmedMeeting(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE,null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()