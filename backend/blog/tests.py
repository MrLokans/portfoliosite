from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from blog.models import Post


User = get_user_model()


class BaseCase(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.api_client.logout()
        super().setUp()

    def assertKeysEqual(self, dict_like, keys_list):
        dict_keys = set(dict_like.keys())
        keys_set = set(keys_list)
        self.assertSetEqual(dict_keys, keys_set,
                            "Dictionary keys do not match.")


class BlogAPITests(BaseCase):

    def test_created_post_is_available_via_API(self):
        p1 = Post.objects.create(author='SomeAuthor',
                                 title='Some Post',
                                 content='Some Content')
        p2 = Post.objects.create(author='AnotherAuthor',
                                 title='Other Post',
                                 content='Content')
        posts_url = reverse('blog-api:list')

        response = self.api_client.get(posts_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        sorted_posts = sorted(response.data, key=lambda x: x['id'])

        post_0 = sorted_posts[0]

        self.assertKeysEqual(post_0, ['id', 'author', 'title',
                                      'content', 'created'])

        self.assertEqual(sorted_posts[0]['id'], p1.id)
        self.assertEqual(sorted_posts[0]['author'], p1.author)
        self.assertEqual(sorted_posts[0]['title'], p1.title)
        self.assertEqual(sorted_posts[0]['content'], p1.content)
        self.assertIn('created', sorted_posts[0])
        self.assertEqual(sorted_posts[1]['id'], p2.id)

    def test_detail_view_for_post_is_available_via_API(self):
        p1 = Post.objects.create(author='SomeAuthor',
                                 title='Some Post',
                                 content='Some Content')

        detail_url = reverse('blog-api:detail',
                             kwargs={'pk': p1.id})
        response = self.api_client.get(detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertKeysEqual(response.data, ['id', 'author', 'title',
                                             'content', 'created'])

        self.assertEqual(response.data['id'], p1.id)
        self.assertEqual(response.data['author'], p1.author)
        self.assertEqual(response.data['title'], p1.title)
        self.assertEqual(response.data['content'], p1.content)

    def test_it_is_impossible_to_delete_post_for_anon(self):
        p1 = Post.objects.create(author='SomeAuthor',
                                 title='Some Post',
                                 content='Some Content')

        posts_count = Post.objects.count()

        detail_url = reverse('blog-api:detail',
                             kwargs={'pk': p1.id})
        response = self.api_client.delete(detail_url, format='json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Post.objects.count(), posts_count)

    def test_admin_is_able_to_delete_blog_post(self):
        p1 = Post.objects.create(author='SomeAuthor',
                                 title='Some Post',
                                 content='Some Content')
        posts_count = Post.objects.count()

        User.objects.create_superuser('admin', 'admin@ad.com',
                                      password='123123')
        self.api_client.login(username='admin', password='123123')

        detail_url = reverse('blog-api:detail',
                             kwargs={'pk': p1.id})
        response = self.api_client.delete(detail_url, format='json')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.count(), posts_count - 1)

    def test_it_is_possible_to_create_post_for_admin_user(self):
        posts_count = Post.objects.count()
        posts_url = reverse('blog-api:list')

        User.objects.create_superuser('admin', 'admin@ad.com',
                                      password='123123')
        self.api_client.login(username='admin', password='123123')

        payload = {
            'author': 'Some Unique Author',
            'title': 'New Title',
            'content': 'Some **markdown** content'
        }

        response = self.api_client.post(posts_url, payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), posts_count + 1)
        post_id = response.data['id']
        post = Post.objects.get(id=post_id)
        self.assertEqual(post.content, 'Some **markdown** content')
        self.assertEqual(post.title, 'New Title')
        self.assertEqual(post.author, 'Some Unique Author')

    def test_it_is_impossible_to_create_post_for_anon(self):
        posts_count = Post.objects.count()
        posts_url = reverse('blog-api:list')

        payload = {
            'author': 'Some Unique Author',
            'title': 'New Title',
            'content': 'Some **markdown** content'
        }

        response = self.api_client.post(posts_url, payload)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Post.objects.count(), posts_count)
