# Data retrieved from Kaggle
import math
import requests
import os
import pandas as pd

PLATFORM_DENSITY_LINK = "http://datamall2.mytransport.sg/ltaodataservice/PCDRealTime"
DATAMALL_API_KEY = "yeCfQUR9TIOh/b+JTgbklg=="


class PublicTransportFinder:
    def __init__(self, mrt_data, bus_stop_data):
        # mrt_data represents pd.read_csv('data/MRT Stations.csv')
        self.mrt_data = mrt_data
        self.bus_stop_data = bus_stop_data

    # Helper Function to calculate distance between coordinates
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        # Using Haversine formula to calculate distance between two points on Earth's surface
        radius_earth_km = 6371.0  # Radius of Earth in kilometers
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = radius_earth_km * c

        return distance

    # MRT Code , latitude and longtitude of current position needs to be retrieved first
    def find_nearby_mrts(self, latitude, longitude, radius_km=1):
        nearby_mrts = {}
        for index, station_row in self.mrt_data.iterrows():
            mrt_lat = station_row["Latitude"]
            mrt_lon = station_row["Longitude"]
            distance = self.calculate_distance(latitude, longitude, mrt_lat, mrt_lon)
            if distance <= radius_km:
                if "/" in station_row["STN_NO"]:
                    station_codes = station_row["STN_NO"].split("/")
                    nearby_mrts[station_row["STN_NAME"]] = station_codes
                else:
                    nearby_mrts[station_row["STN_NAME"]] = [station_row["STN_NO"]]
        return nearby_mrts

    # Final Function
    def get_low_density_nearby_stations(self, latitude, longitude):

        stations = []

        nearby_mrts = self.find_nearby_mrts(latitude, longitude)
        for station_name, station_number_arr in nearby_mrts.items():

            for stn_no in station_number_arr:
                train_line = stn_no[:-1] + "L"
                response = requests.get(
                    PLATFORM_DENSITY_LINK,
                    params={"TrainLine": train_line},
                    headers={"AccountKey": DATAMALL_API_KEY},
                )
                data = response.json()["value"]

                for stn_dict in data:
                    if stn_no == stn_dict['Station']:
                        if stn_dict['CrowdLevel'] != 'h':
                            stations.append(stn_no)

        return stations


mrt_station_df = pd.read_csv("../../misc/data/MRT Stations.csv")
bus_stops_df = pd.read_csv("../../misc/data/bus_stops.csv")

public_transport_object = PublicTransportFinder(mrt_station_df, bus_stops_df)

nearby_stations = public_transport_object.find_nearby_mrts(
    1.3129816930513392, 103.88709040919767
)

low_density_stations_nearby = public_transport_object.get_low_density_nearby_stations(
    1.3129816930513392, 103.88709040919767
)

print(nearby_stations)
print(low_density_stations_nearby)
