# src/tools/get_api_data.py

import requests


def get_api_data(query: str) -> str:
    """
    Mock function that calls some external API with 'query'.
    Real usage would parse JSON, etc.
    """
    # This is just a placeholder to show how you'd structure it.
    # e.g. response = requests.get("https://some-financial-api.com", params={"q": query})
    # data = response.json()
    # ...
    return f"API data for '{query}': [mock result]"
