import pytest
import requests


SUCCESS_STATUS_CODE = 200


@pytest.mark.parametrize(
    "url_path,description",
    (
        ("/", "Site main page is available"),
        ("/admin/", "Admin page is available"),
        ("/_internal-portal_/", "Internal admin page is available"),
        ("/api/health/", "Health check is available"),
        ("/api/books/", "Books API is available"),
    ),
)
def test_http_availability(request, url_path, description):
    site_base_address = request.config.getoption("--site_base_address")
    assert requests.get(site_base_address + url_path).status_code == SUCCESS_STATUS_CODE
