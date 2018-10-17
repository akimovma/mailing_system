from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Profile(AbstractUser):
    # add additional fields in here
    birth_date = models.DateField(null=True)
    phone = PhoneNumberField(blank=True)

    def __str__(self):
        return self.email
