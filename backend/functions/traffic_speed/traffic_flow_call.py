from ..utils.api import lta_api
from geopy.distance import geodesic
import math



class Traffic_Speed:

    road_width = 40
    band_mapper = {
        1: "extremely heavy traffic with speed range from 0 < 9",
        2: "heavy traffic with speed range from 10 < 19",
        3: "heavy traffic with speed range from 20 < 29",
        4: "moderate traffic with speed range from 30 < 39",
        5: "moderate traffic with speed range from 40 < 49",
        6: "slight traffic with speed range from 50 < 59",
        7: "little to no traffic with speed range from 60 < 69",
        8: "no traffic with speed range from 70 or more",
    }

    def __init__(self):
        pass

    def haversine(self, lat1, lon1, lat2, lon2):
        """Calculates distance between two points on Earth using the Haversine formula.
        """
        R = 6371  # Approximate Earth's radius in kilometers 

        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)

        a = math.sin(dLat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dLon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
        distance = R * c

        return distance * 1000  # Return distance in meters


    def distance_to_line(self, point, startCoord, endCoord):
        """Calculates approximate minimum distance from a point to a line segment."""
        px, py = point
        x1, y1 = startCoord
        x2, y2 = endCoord

        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == 0:
            # The line segment is a point 
            return self.haversine(point[0], point[1], startCoord[0], startCoord[1])

        # Project point onto line, finding parametric value of projection
        u = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)

        # Clamp parametric value to line segment boundaries
        u = max(0, min(1, u)) 

        # Find the closest point on the line segment 
        closest_x = x1 + u * dx
        closest_y = y1 + u * dy

        return self.haversine(point[0], point[1], closest_x, closest_y) 

    def get_speed(self, coords):

        coords = coords.split(",")
        latitude = float(coords[0])
        longitude = float(coords[1])
        try:
            response = lta_api("v3/TrafficSpeedBands")
        except:
            return None
        
        min_distance = 100000
        road_choice = None
        
        if response:
            roads = response.json()
            for road in roads["value"]:
                startCoord, endCoord = (float(road["StartLat"]), float(road["StartLon"])), (float(road["EndLat"]), float(road["EndLon"]))
                # Check distance from line string here
                point = (latitude, longitude)
                distance_to_line = self.distance_to_line(point, startCoord, endCoord)
                if distance_to_line <= min_distance:  # Incorporate road_width
                    min_distance = distance_to_line
                    road_choice = road

            road_name = road_choice["RoadName"]
            speed_band = self.band_mapper[road_choice["SpeedBand"]]
            return speed_band, road_name, round(min_distance, 3)



if __name__ == "__main__":
    pass