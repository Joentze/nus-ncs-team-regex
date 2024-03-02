import os
from dotenv import load_dotenv
import requests
import json
from ..utils.geocode import geocode
import asyncio

class api:
    url = "http://datamall2.mytransport.sg/ltaodataservice/"

    def __init__(self):
        load_dotenv()
        self.key = os.getenv('api_key')
        self.headers  = {
            'Accept': 'application/json',          
            'AccountKey': self.key             
        }

    def fetch_api(self, domain):
        try:
            response = requests.get(self.url + domain, headers=self.headers)
            response.raise_for_status() 
            return json.loads(response.content)
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None 
        
    def process(self, values):
        geolocator = geocode()
        for item in values:
            type = item["Type"]
            lat = item["Latitude"]
            long = item["Longitude"]
            msg = item["Message"]

            address = asyncio.run(geolocator.reverse(f"{lat}, {long}"))

            print(f"type {type} accident at {address}")

    def incidents(self):
        domain = "TrafficIncidents"
        content = self.fetch_api(domain)
        if content["value"]:
            values = content["value"]
            self.process(values)
        else:
            return None

    def warnings(self):
        domain = "VMS"
        content = self.fetch_api(domain)
        if content["value"]:
            values = content["value"]
            self.process(values)
        else:
            return None


if __name__ == "__main__":
    obj = api()
    obj.warnings


