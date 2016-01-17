from django.db import models
from tinymce import models as tinymce_models


class Tag(models.Model):
    value = models.CharField(max_length=60)


class Post(models.Model):
    # TODO: turn to slug field
    title = models.CharField(max_length=200)
    text = tinymce_models.HTMLField()
    # Deal withmany to many fields
    tags = models.ManyToManyField(Tag)


class Book(models.Model):

    author = models.CharField(max_length=300)
    title = models.CharField(max_length=200)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return '<Book {}>'.format(self.title)


class BookNote(models.Model):

    book = models.ForeignKey('Book')
    text = models.TextField()
    type = models.IntegerField()
