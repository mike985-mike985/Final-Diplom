import pytest
from pages.api_client import APIClient
from config import VALID_API_FILMS, VALID_MOVIE_ID, EMPTY_QUERY, \
    INVALID_QUERY, SPECIAL_CHARS_QUERY, RUSSIAN_NO_SPACES, INVALID_MOVIE_ID


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.parametrize("query", VALID_API_FILMS)
def test_search_valid_queries(client, query):
    response = client.search_movies(query)
    assert response.status_code == 200
    data = response.json()
    assert "docs" in data
    assert isinstance(data["docs"], list)


def test_get_movie_by_id(client):
    response = client.get_movie_by_id(VALID_MOVIE_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == VALID_MOVIE_ID
    assert "name" in data


def test_empty_query(client):
    response = client.search_movies(EMPTY_QUERY)
    assert response.status_code == 200


def test_invalid_query(client):
    response = client.search_movies(INVALID_QUERY)
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("docs", [])) == 0


def test_special_chars_query(client):
    response = client.search_movies(SPECIAL_CHARS_QUERY)
    assert response.status_code == 200


def test_russian_no_spaces(client):
    response = client.search_movies(RUSSIAN_NO_SPACES)
    assert response.status_code == 200
    assert len(response.json().get("docs", [])) == 0


def test_without_token(client):
    response = client.get_movie_by_id(INVALID_MOVIE_ID, use_auth=False)
    assert response.status_code == 401
