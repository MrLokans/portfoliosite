from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

User = get_user_model()


class BaseCase(TestCase):
    """
    Base class shared between multiple applications
    with some common routines
    """

    def _create_admin(self, username,
                      password,
                      email):
        admin = User.objects.create_superuser(username=username,
                                              email=email,
                                              password=password)
        return admin

    @classmethod
    def setUpClass(cls):
        cls.ADMIN_USERNAME = 'superadmin'
        cls.ADMIN_EMAIL = 'admin@email.com'
        cls.ADMIN_PASS = 'TestPassword'
        cls.rest_client = APIClient()
        super().setUpClass()

    def setUp(self):
        self.admin_user = self._create_admin(username=self.ADMIN_USERNAME,
                                             email=self.ADMIN_EMAIL,
                                             password=self.ADMIN_PASS)
        super().setUp()

    def login_as_admin(self):
        self.rest_client.login(username=self.ADMIN_USERNAME,
                               password=self.ADMIN_PASS)

    def logout(self):
        self.rest_client.logout()

    def tearDown(self):
        self.admin_user.delete()
        self.logout()
        super().tearDown()
