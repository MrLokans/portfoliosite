from django.urls import reverse

from personal_site.tests.base import BaseCase
from favorites.models import FavoriteLink


class FavoritesTestCase(BaseCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.favorites_link_url = reverse('favorites-api:favorites-list')

    def test_favorite_may_be_created_via_api_by_admin(self):
        favorites_count = FavoriteLink.objects.count()

        payload = {
            'url': 'http://some-new-note-3.com',
            'comment': 'Here is also some comment'
        }

        self.login_as_admin()
        resp = self.rest_client.post(self.favorites_link_url, data=payload)

        self.assertEqual(resp.status_code, 201)
        new_id = resp.json()['id']

        new_favorite = FavoriteLink.objects.get(id=int(new_id))
        self.assertEqual(FavoriteLink.objects.count(), favorites_count + 1)
        self.assertEqual(new_favorite.url, payload['url'])
        self.assertEqual(new_favorite.comment, payload['comment'])

    def test_favorite_may_not_be_created_via_unauthorized(self):
        payload = {
            'url': 'http://some-new-note-3.com',
            'comment': 'Here is also some comment'
        }

        resp = self.rest_client.post(self.favorites_link_url, data=payload)

        self.assertEqual(resp.status_code, 403)

    def test_favorite_may_not_be_created_via_simple_user(self):
        user_data = {
            'username': 'test_user',
            'email': 'us@us.us',
            'password': 'test'
        }
        self._create_user(**user_data)

        self.rest_client.login(username=user_data['username'],
                               password=user_data['password'])

        payload = {
            'url': 'http://some-new-note-3.com',
            'comment': 'Here is also some comment'
        }

        resp = self.rest_client.post(self.favorites_link_url, data=payload)

        self.assertEqual(resp.status_code, 403)

    def test_favorite_list_may_be_obtained_by_admin(self):
        FavoriteLink.objects.create(url='http://some-note1.ru')
        FavoriteLink.objects.create(url='http://some-note2.ru')

        self.login_as_admin()
        resp = self.rest_client.get(self.favorites_link_url)

        self.assertEqual(resp.status_code, 200)

    def test_favorite_list_may_not_be_obtained_by_authorized_non_admin(self):
        user_data = {
            'username': 'test_user',
            'email': 'us@us.us',
            'password': 'test'
        }
        self._create_user(**user_data)

        self.rest_client.login(username=user_data['username'],
                               password=user_data['password'])

        # We are logged as non-admin
        resp = self.rest_client.get(self.favorites_link_url)
        self.assertEqual(resp.status_code, 403)

    def test_favorite_list_may_not_be_obtained_by_non_authorized(self):
        FavoriteLink.objects.create(url='http://some-note2.ru')
        FavoriteLink.objects.create(url='http://some-note1.ru')

        # We are not logged in
        resp = self.rest_client.get(self.favorites_link_url)
        self.assertEqual(resp.status_code, 403)
