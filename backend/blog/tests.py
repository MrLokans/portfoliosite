from django.test import Client, TestCase
from django.urls import reverse

from blog.models import Post


class BlogAPITests(TestCase):

    def test_created_post_is_available_via_API(self):
        p1 = Post.objects.create(author='SomeAuthor',
                                 title='Some Post',
                                 content='Some Content')

        # url = reverse('blog-api:')