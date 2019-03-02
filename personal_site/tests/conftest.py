WEBSITE_URL_ENVIRONMENT_VARIABLE = "SERVER_ADDRESS"


def pytest_addoption(parser):
    parser.addoption(
        "--site_base_address",
        type=str,
        default=WEBSITE_URL_ENVIRONMENT_VARIABLE,
        help="Base site address for availability tests (e.g. https://mysite.com)",
    )
