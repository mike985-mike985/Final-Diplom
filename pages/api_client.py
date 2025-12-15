import requests
from config import API_URL, API_KEY


class APIClient:
    def __init__(self):
        self.base_url = API_URL.rstrip('/')
        self.headers = {'X-API-KEY': API_KEY} if API_KEY else {}

    def request(self, method, endpoint, params=None, use_auth=True):
        url = f"{self.base_url}{endpoint}"
        headers = self.headers if use_auth else {}

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params
        )
        return response

    def search_movies(self, query, page=1, limit=10, use_auth=True):
        params = {'page': page, 'limit': limit, 'query': query}
        return self.request('GET', '/v1.4/movie/search', params, use_auth)

    def get_movie_by_id(self, movie_id, use_auth=True):
        return self.request(
            'GET', f'/v1.4/movie/{movie_id}', use_auth=use_auth)
