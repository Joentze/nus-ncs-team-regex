import os
from dotenv import load_dotenv
import requests
import json
from geocode import geocode
import asyncio

class Alert:
    def __init__(self, id, latitude, longitude, message, address):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.message = message
        self.address = address

    def parse_message():
        pass
        #function to retrieve date and time 

class api:
    url = "http://datamall2.mytransport.sg/ltaodataservice/"
    incident_domain = "TrafficIncidents"
    warning_domain = "VMS"

    def __init__(self):
        load_dotenv()
        self.key = os.getenv('api_key')
        self.headers  = {
            'Accept': 'application/json',          
            'AccountKey': self.key             
        }
        self.geolocator = geocode()

    def fetch_api(self, domain):
        """Fetches datamall API.

        Args:
            domain (str): Domain path (refer to the Datamall API documentation).

        Returns:
            dict: The parsed JSON response from the API.

        Raises:
            requests.exceptions.HTTPError: If the API request fails (e.g., error code 404, 500).
        """
        try:
            response = requests.get(self.url + domain, headers=self.headers)
            response.raise_for_status() 
            return json.loads(response.content)
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None 
        
    def get_address(self, lat, long):
        """Reverse geocoding

        Args:
            lat (str): Latitude
            long (str): Longitude

        Returns:
            address (str)
        """
        address = asyncio.run(self.geolocator.reverse(f"{lat}, {long}"))
        return address
        
    def process_events(self, values, event_type):
        """Processes events (for now, geocodes messages)

        Args:
            values (dict)

        Returns:
            events (list): List of events (objects) 
        """
        events = []
        for item in values:
            address = self.get_address(item["Latitude"], item["Longitude"])
            event = Alert(item[event_type], item["Latitude"], item["Longitude"], item["Message"], address)
            events.append(event)

        return events
    
    def get_events(self, domain):
        """Calls other functions 

        Args:
            domain (str): Domain path (refer to the Datamall API documentation).

        Returns:
            events (list): List of events (objects)
        """
        content = self.fetch_api(domain)
        if content["value"]:
            values = content["value"]
            if domain == self.incident_domain:
                return self.process_events(values, "Type") 
            else:
                return self.process_events(values, "EquipmentID")
        else:
            return None


if __name__ == "__main__":
    obj = api()
    events = obj.get_events("TrafficIncidents")
    for e in events:
        print(f"{e.id}, \n {e.address}, \n {e.message}")


