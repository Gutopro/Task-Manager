from django.db import models

# Create your models here.
class TrackingModel(models.Model):
    """ Definition of the tracking model for create and update """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserModel(TrackingModel):
    """ Defines user model for task app """
    username = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
