from django.db import models


class Tag(models.Model):

    value = models.CharField(max_length=60)


class Book(models.Model):

    author = models.CharField(max_length=300)
    title = models.CharField(max_length=200)
    tag = models.ManyToManyField(Tag)


class BookNote(models.Model):

    book = models.ForeignKey('Book')
    text = models.TextField()
    type = models.IntegerField()
