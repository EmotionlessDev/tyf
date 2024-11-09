from functools import partial

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django_resized import ResizedImageField
from random_username.generate import generate_username
from utils import generate_media_path


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if user.username is None:
            user.username = generate_username()[0]
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    course = models.CharField(max_length=50, blank=True, null=True)
    major = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = ResizedImageField(
        crop=["middle", "center"],
        size=[300, 300],
        force_format="WEBP",
        quality=100,
        upload_to=partial(generate_media_path, key="email", remove_with_same_key=True),
        blank=True,
        null=False,
        verbose_name="Avatar",
    )
    points = models.IntegerField(default=0)
    awards = models.IntegerField(default=0)
    telegram = models.URLField(blank=True, null=True, verbose_name="Telegram")
    vkontakte = models.URLField(blank=True, null=True, verbose_name="VK")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
