from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100)
    # description = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Collection(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title