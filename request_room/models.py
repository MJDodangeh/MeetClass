from django.db import models
from account.models import User

class RequestRoom(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True)
    number = models.IntegerField()
    date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    duration = models.TimeField(null=True)