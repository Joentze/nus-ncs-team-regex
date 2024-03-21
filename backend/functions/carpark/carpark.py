import requests
import pandas as pd
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
from ..utils.api import lta_api
from ..utils.geocode import geocode

class Carpark:

    def __init__(self) -> None:
        pass

    def get_carpark_data(self):
        response = lta_api("CarParkAvailabilityv2")

        if response.status_code == 200:
            data = response.json()
            carpark_data = data['value']
            df = pd.DataFrame(carpark_data)
            location_data = df['Location'].str.extract(r'(\d+\.\d+)\s+(\d+\.\d+)')
            df[['Latitude', 'Longitude']] = location_data.astype(float) 
            df['timestamp'] = datetime.now()
                
            return df
        
        else:
            print("Error:", response.status_code)
            print(response.text)
            

    def haversine(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # Convert decimal degrees to radians 
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a)) 
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles
        return r * c
    

    def get_top_5_closest_carparks(self, location):
        """
        Takes in a single string with latitude and longitude separated
        with a space and outputs the closest 5 carparks as a dataframe
        """
        # Extract latitude and longitude from the location
        lat, lon = map(float, location.split(','))
        
        carpark_df = self.get_carpark_data()
        # Calculate distance from each car park to the given location
        carpark_df['distance'] = carpark_df.apply(lambda row: self.haversine(lat, lon, row['Latitude'], row['Longitude']), axis=1)
        
        # Sort dataframe by distance and select top 5 closest car parks
        closest_carparks = carpark_df.sort_values(by='distance').head(5)
        # Filter out relevant columns and return the result
        return closest_carparks[['CarParkID',"Area","Development",'AvailableLots']].sort_values(by='AvailableLots', ascending=False)
