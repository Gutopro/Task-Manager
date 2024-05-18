"""Module for base model"""
from django.db import models

class BaseModel(models.Model):
    """Definition of the base model that should be 
    inherited by other models"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
