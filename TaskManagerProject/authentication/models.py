from django.db import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from email_validator import validate_email, EmailNotValidError
from .base_model import BaseModel

def custom_email_validator(value):
    try:
        validate_email(value)
    except EmailNotValidError as e:
        raise ValidationError(str(e))

class User(BaseModel):
    """ User Definition """
    username = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200, unique=True, validators=[custom_email_validator])
    password = models.CharField(max_length=200)