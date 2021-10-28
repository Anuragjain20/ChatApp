from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(User):

    name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)



    def __str__(self):
        return self.name