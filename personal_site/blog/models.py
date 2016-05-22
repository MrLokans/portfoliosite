from django.db import models


class Tag(models.Model):
    value = models.CharField(max_length=60)


class Post(models.Model):
    # TODO: turn to slug field
    # TODO: reference user
    author = models.CharField(max_length=100, default="John Doe")
    title = models.CharField(max_length=200)
    text = models.TextField()
    # Deal withmany to many fields
    created = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
