from django.db import models
from django.contrib.auth.models import AbstractUser

# Should we put Group of Users here? (e.g. Students, Teachers, System Programming Student etc.)

# Put AUTH_USER_MODEL = 'users.User' in settings.py

class User(AbstractUser):
    # groups = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    # Is it better to use WEBP for images? django-resized contains ResizeImageField that works with pillow automatically
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Avatar")

    # Points to show activity (yes, it can be negative :0 )
    points = models.IntegerField(default=0)

    # Awards for User (e.g. "The Holy Ghost - Gain over 50 likes(stars) on Lecture Note")
    awards = models.ManyToManyField('Award', related_name='awards', blank=True)

    # Contacts
    telegram = models.URLField(blank=True, null=True, verbose_name="Telegram")
    vkontakte = models.URLField(blank=True, null=True, verbose_name="VK")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
