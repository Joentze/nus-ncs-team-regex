import os
import requests
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env') 
load_dotenv(dotenv_path)
API_KEY =  os.getenv('API_KEY')
BASE_URL =  os.getenv('BASE_URL')

def lta_api(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url,
                            params=params,
                            headers= {"AccountKey": API_KEY})
    response.raise_for_status() 
    return response
