from django.db import models
from Authentication.models import TrackingModel

class Task(TrackingModel):
    """Class for the task model"""
    name = models.CharField(max_length=250)
    description = models.TextField(default='')
    is_complete = models.BooleanField(default=False)
