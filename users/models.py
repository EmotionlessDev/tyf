from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    # groups = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    username = models.CharField(max_length=50, unique=True, blank=True, null=False)

    email = models.EmailField(unique=True)

    # Is it better to use WEBP for images? django-resized contains ResizeImageField that works with pillow automatically
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=False, verbose_name="Avatar")

    # Points to show activity (yes, it can be negative :0 )
    points = models.IntegerField(default=0)

    # Awards for User (e.g. "The Holy Ghost - Gain over 50 likes(stars) on Lecture Note")
    # awards = models.ManyToManyField('Award', related_name='awards', blank=True)

    # Contacts
    telegram = models.URLField(blank=True, null=True, verbose_name="Telegram")
    vkontakte = models.URLField(blank=True, null=True, verbose_name="VK")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.generate_username()

        super(User, self).save(*args, **kwargs)

    @staticmethod
    def generate_username():
        # We can use this to generate random username:
        # https://pypi.org/project/random-username/
        return "Kukold228"

    def __str__(self):
        return self.username