import os
from functools import partial

from PIL import Image
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import CharField
from django_resized import ResizedImageField
from random_username.generate import generate_username
from mdeditor.fields import MDTextField

from tyf.settings import MEDIA_ROOT
from registry.models import Major, University
from utils import generate_media_path, generate_uuid
import markdown


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, blank=False, null=True, related_name="profile",)
    email = models.EmailField(unique=False, blank=False, null=False)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    university = models.ForeignKey(
        University,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="University",
    )
    major = models.ForeignKey(
        Major,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Major",
    )
    date_of_birth = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
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
    thumbnail = models.ImageField(
        upload_to=partial(generate_media_path, key="email", remove_with_same_key=True),
        blank=True,
        null=True,
        verbose_name="Thumbnail",
    )
    points = models.IntegerField(default=0, blank=True, null=True)
    awards = models.IntegerField(default=0, blank=True, null=True)
    telegram = models.URLField(blank=True, null=True, verbose_name="Telegram")
    vkontakte = models.URLField(blank=True, null=True, verbose_name="VK")
    __original_mode = None

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        **kwargs,
    ):
        if self.avatar != self.__original_mode:
            self.__original_mode = self.avatar
            # self.save_thumbnail()

        if not self.username:
            username = generate_username()[0]
            while Profile.objects.filter(username=username).exists():
                username = generate_username()[0]
            self.username = generate_username()[0]
        super(Profile, self).save(force_insert, force_update, *args, **kwargs)

    # def save_thumbnail(self):
    #     if not self.avatar:
    #         return
    #     image = Image.open(self.avatar)
    #     image.thumbnail((49, 50), Image.Resampling.LANCZOS)
    #     thumb_name, _ = os.path.splitext(self.avatar.name)
    #     thumb_filename = thumb_name + "_thumb" + ".webp"
    #     image.save(MEDIA_ROOT + thumb_filename, "WEBP")
    #     self.thumbnail = thumb_filename
    #     return True

    def __str__(self):
        return f"{self.username} ({self.email})"


class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} follows {self.following}"


class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    identifier = CharField(max_length=8, primary_key=False, editable=False, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    collections = models.ManyToManyField(Collection, related_name="posts", blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    content = MDTextField()
    stars = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        **kwargs,
    ):
        md = markdown.Markdown(extensions=["fenced_code", "codehilite"])
        self.content = md.convert(self.content)
        self.identifier = generate_uuid(klass=Post)
        super(Post, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    identifier = CharField(max_length=8, primary_key=False, editable=False, unique=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    stars = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        **kwargs,
    ):
        self.identifier = generate_uuid(klass=Comment)
        super(Comment, self).save(force_insert, force_update, *args, **kwargs)


class Media(models.Model):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="media"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    file = models.FileField(
        upload_to=partial(
            generate_media_path, key="object_id", remove_with_same_key=False
        ),
        null=True,
        blank=True,
    )
    description = models.CharField(max_length=255, blank=True, null=True)
