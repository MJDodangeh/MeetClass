from django.db import models
from account.models import User

class RequestRoom(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    number = models.IntegerField()
    date = models.DateField(null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.TimeField()