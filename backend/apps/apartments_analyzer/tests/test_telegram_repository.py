import pytest

from apps.apartments_analyzer.management.commands.run_apartments_bot import TelegramSearchRepository


pytestmark = pytest.mark.django_db


def test_creating_new_contact():
    repo = TelegramSearchRepository()
    is_created, user_search  = repo.get_or_create_for_user("12312414512")
    assert is_created
    assert user_search.search_version == 0
    assert user_search.min_price == 0
    assert user_search.max_price == 300
    assert user_search.is_active


def test_search_representation():
    repo = TelegramSearchRepository()
    is_created, user_search  = repo.get_or_create_for_user("12312414512")
    assert is_created
    user_search.as_displayed_to_user()


def test_double_create_does_not_create_new_search():
    repo = TelegramSearchRepository()
    search_id = "12312414512"
    _, first_search = repo.get_or_create_for_user(search_id)
    is_created, second_search = repo.get_or_create_for_user(search_id)
    assert not is_created
    assert second_search.pk == first_search.pk
