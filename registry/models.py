from django.db import models


class University(models.Model):
    acronym = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.acronym


class Major(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
