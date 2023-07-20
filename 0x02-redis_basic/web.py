#!/usr/bin/env python3
"""
Web module to fetch web pages with caching using Redis
"""


import requests
import redis
from typing import Optional


class Wed:
    """
    Web class to fetch web pages
    """
    def __init__(self):
        """
        Initializes the web instance
        """
        self._redis = redis.Redis()

    def get_page(self, url: str) -> Optional[str]:
        """
        Fetches the HTML content of given url
        """
        count_key = f"count:{url}"
        page_key = f"page:{url}"
        self._redis.incr(count_key)
        cached_page = self._redis.get(page_key)
        if cached_page:
            return cached_page.decode("utf-8")

        try:
            response = requests.get(url)
            response.raise_for_status()
            page_content = response.text
            self._redis.setex(page_key, 10, page_content)
            return page_content
        except requests.exceptions.RequestException:
            return None
