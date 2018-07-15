from django.db import models


class Tag(models.Model):
    value = models.CharField(max_length=60)


class Post(models.Model):
    author = models.CharField(max_length=100, default="John Doe")
    title = models.CharField(max_length=200)

    content = models.CharField(max_length=30000)

    created = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return ('BlogPost(author={0}, title={1})'
                .format(self.author, self.title))
