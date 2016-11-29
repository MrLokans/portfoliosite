import os

from django.test import Client, TestCase


class SuperTestCase(TestCase):
    def test_simple_page(self):
        print(self.client.get('/'))
