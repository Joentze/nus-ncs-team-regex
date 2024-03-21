import os
import requests
import json
import asyncio
import math
from ..utils.api import lta_api
# from ..utils.geocode import geocode

class Alert:
    def __init__(self, id, latitude, longitude, message, address=None):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.message = message
        self.address = address

    def within_3km_radius(self, coords):
        coords = coords.split(',')
        user_lat = float(coords[0])
        user_long = float(coords[1])
        R = 6371 

        delta_lat = math.radians(user_lat - self.latitude)
        delta_long = math.radians(user_long - self.longitude)

        a = math.sin(delta_lat / 2) ** 2 + \
            math.cos(math.radians(self.latitude)) * math.cos(math.radians(user_lat)) * \
            math.sin(delta_long / 2) ** 2
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c  

        return distance <= 3


class Message:
    incident_domain = "TrafficIncidents"
    warning_domain = "VMS"

    def __init__(self):
        pass
        # self.key = os.getenv('api_key')
        # self.headers  = {
        #     'Accept': 'application/json',          
        #     'AccountKey': self.key             
        # }
        # self.geolocator = geocode() 
        
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
        
    def process_events(self, values, event_type, coords):
        """Processes events (for now, geocodes messages)

        Args:
            values (dict)

        Returns:
            events (list): List of events (objects) 
        """
        events = []
        count = 0
        for item in values:
            # address = self.get_address(item["Latitude"], item["Longitude"])
            event = Alert(item[event_type], item["Latitude"], item["Longitude"], item["Message"])
            if event.within_3km_radius(coords):
                events.append(event.message)
                count += 1
            if count > 4:
                break
        return events
    
    def get_events(self, domain, coords):
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
                return self.process_events(values, "Type", coords) 
            else:
                return self.process_events(values, "EquipmentID", coords)
        else:
            return None


if __name__ == "__main__":
    obj = Message()
    events = obj.get_events("TrafficIncidents")
    for e in events:
        print(f"{e.id}, \n {e.address}, \n {e.message}")


