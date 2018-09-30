import os

import pytest
import requests


SUCCESS_STATUS_CODE = 200


@pytest.fixture
def domain_address():
    return os.environ.get('SERVER_ADDRESS', 'http://localhost:8000')


@pytest.mark.parametrize("url_path,description", (
        ('/', 'Site main page is available'),
        ('/admin/', 'Admin page is available'),
        ('/_internal-portal_/', 'Internal admin page is available'),
        ('/api/health/', 'Health check is available'),
        ('/api/books/', 'Books API is available'),
))
def test_http_availability(domain_address, url_path, description):
    assert requests.get(domain_address + url_path).status_code == SUCCESS_STATUS_CODE
