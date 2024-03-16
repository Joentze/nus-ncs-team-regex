import os
import requests
import json
import asyncio
from ..utils.api import lta_api
from ..utils.geocode import geocode

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

class Message:
    incident_domain = "TrafficIncidents"
    warning_domain = "VMS"

    def __init__(self):
        self.key = os.getenv('api_key')
        self.headers  = {
            'Accept': 'application/json',          
            'AccountKey': self.key             
        }
        self.geolocator = geocode() 
        
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
        content = lta_api(domain, None)
        content = content.json()
        if content["value"]:
            values = content["value"]
            if domain == self.incident_domain:
                return self.process_events(values, "Type") 
            else:
                return self.process_events(values, "EquipmentID")
        else:
            return None


if __name__ == "__main__":
    obj = Message()
    events = obj.get_events("TrafficIncidents")
    for e in events:
        print(f"{e.id}, \n {e.address}, \n {e.message}")


