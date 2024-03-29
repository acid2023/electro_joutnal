from django.db import models
from django.contrib.auth.models import User


class SocialUser(User):
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
