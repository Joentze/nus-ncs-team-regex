import os
import requests

API_KEY = os.environ['API_KEY']
BASE_URL = os.environ['BASE_URL']


def lta_api(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url,
                            params=params,
                            headers={"AccountKey": API_KEY})
    response.raise_for_status()
    return response
