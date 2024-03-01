import os
from dotenv import load_dotenv
import requests

load_dotenv()

key = os.getenv('api_key')

url = "http://datamall2.mytransport.sg/ltaodataservice/VMS"

response = requests.post(url, headers=key)
print(response)