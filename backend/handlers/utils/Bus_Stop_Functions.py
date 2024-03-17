import pandas as pd
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

class Bus_Stop_Finder:
    def __init__(self, bus_routes, bus_services, bus_stops, passenger_vol_feb):
        self.bus_routes = bus_routes
        self.bus_services = bus_services
        self.bus_stops = bus_stops
        self.passenger_vol_feb = passenger_vol_feb

    def find_nearby_bus_stops(self, location, radius=800):
        """
        Find nearby bus stops within a specified radius (800m for now) from the given location
        
        :param location: A tuple of (latitude, longitude) for the location
        :param radius: The radius within which to find bus stops, in meters
        :return: A DataFrame of nearby bus stops
        """
        self.bus_stops['Distance_to_Location'] = self.bus_stops.apply(
            lambda row: geodesic((row['Latitude'], row['Longitude']), location).meters, axis=1)

        nearby_stops = self.bus_stops[self.bus_stops['Distance_to_Location'] <= radius]
        nearby_stops = nearby_stops.sort_values(by='Distance_to_Location').reset_index(drop=True)
        
        return nearby_stops


    ############# historical bus crowdedness data #############
    def find_crowded_stops(self, nearby_stops_df):
        """
        Find the most crowded bus stops based on passenger volume data
        
        :param nearby_stops_df: A DataFrame of nearby bus stops
        :return: A DataFrame of crowded bus stops with passenger volume data
        """
        # passenger volume data for the closest bus stops
        nearby_stops_codes = nearby_stops_df['BusStopCode'].tolist()
        filtered_passenger_volume = self.passenger_vol_feb[passenger_vol_feb['PT_CODE'].isin(nearby_stops_codes)]

        # total tap-in and tap-out volumes to identify crowded stops
        crowdedness = filtered_passenger_volume.groupby('PT_CODE').agg(
            Total_Tap_In=('TOTAL_TAP_IN_VOLUME', 'sum'),
            Total_Tap_Out=('TOTAL_TAP_OUT_VOLUME', 'sum')
        ).reset_index()

        crowdedness = crowdedness.merge(self.bus_stops, left_on='PT_CODE', right_on='BusStopCode')
        
        # stops sorted by total tap-in volume (proxy for crowdedness)
        crowdedness_sorted = crowdedness.sort_values(by='Total_Tap_In', ascending=False)
        
        return crowdedness_sorted[['PT_CODE', 'RoadName', 'Description', 'Total_Tap_In', 'Total_Tap_Out']]
        
    
    def find_less_crowded_alternatives(self, crowded_stop_code):
        """
        Identify less crowded bus stops within 500m of the given crowded stop
        
        :param crowded_stop_code: The bus stop code for the crowded stop.
        :return: A DataFrame of less crowded alternative bus stops.
        """
        crowded_stop_info = self.bus_stops[self.bus_stops['BusStopCode'] == crowded_stop_code]
        print(crowded_stop_info)
        crowded_stop_location = crowded_stop_info[['Latitude', 'Longitude']].iloc[0]
        crowded_stop_location = (crowded_stop_location['Latitude'], crowded_stop_location['Longitude'])
        
        # total tap-ins for the crowded stop
        crowded_stop_crowdedness = self.find_crowded_stops(crowded_stop_info)
        crowded_stop_tap_ins = crowded_stop_crowdedness['Total_Tap_In'].iloc[0]

        nearby_stops = self.find_nearby_bus_stops(crowded_stop_location, 500)
        nearby_stops = nearby_stops[nearby_stops['BusStopCode'] != crowded_stop_code]

        nearby_crowdedness = self.find_crowded_stops(nearby_stops)

        # make sure stops have lesser tap-ins than the crowded stop
        less_crowded_alternatives = nearby_crowdedness[nearby_crowdedness['Total_Tap_In'] < crowded_stop_tap_ins]
        less_crowded_alternatives = less_crowded_alternatives.sort_values(by='Total_Tap_In')

        return less_crowded_alternatives
    
    
    def find_buses_serving_stop(self, bus_stop_code):
        """
        Find bus services that serve the specified bus stop
        
        :param bus_stop_code: The bus stop code for which to find serving bus services
        :return: A list containing bus services that serve the specified bus stop
        """
        services_at_stop = self.bus_routes[self.bus_routes['BusStopCode'] == bus_stop_code]
        return services_at_stop['ServiceNo'].tolist()


    def get_route_details(self, service_no, route_direction):
        """
        Get the route details for a specific bus service and direction.
        
        :param service_no: The bus service number
        :param route_direction: The direction of the bus route
        :return: A DataFrame containing the route details
        """
        route_details = self.bus_routes[(self.bus_routes['ServiceNo'] == service_no) &
                                        (self.bus_routes['Direction'] == route_direction)]

        route_details = route_details.merge(self.bus_stops, left_on='BusStopCode', right_on='BusStopCode', how='left')
        route_details = route_details.sort_values(by=['ServiceNo', 'Direction', 'StopSequence'])
        route_details = route_details[['ServiceNo', 'Direction', 'StopSequence', 'BusStopCode', 'RoadName', 'Description', 'Latitude', 'Longitude']]
        return route_details



    def chart_bus_route(self, route_details, target_coords):
        """
        Plot the route details on a map, with the target location
        
        :param route_details: DataFrame containing route details
        :param target_coordinates: (latitude, longitude) for target location 
        """
        singapore_map = gpd.read_file('../../misc/data/RoadSectionLine.shp')
        
        svy21_wkt = 'PROJCS["SVY21",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",28001.642],PARAMETER["False_Northing",38744.572],PARAMETER["Central_Meridian",103.8333333333333],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",1.366666666666667],UNIT["Meter",1.0]]'
        singapore_map.set_crs(svy21_wkt, inplace=True)
        singapore_map = singapore_map.to_crs('epsg:4326')

        buffer = 0.01
        min_lon, max_lon = route_details['Longitude'].min() - buffer, route_details['Longitude'].max() + buffer
        min_lat, max_lat = route_details['Latitude'].min() - buffer, route_details['Latitude'].max() + buffer
        
        # base layer: SG map 
        fig, ax = plt.subplots(figsize=(10, 8))
        singapore_map.plot(ax=ax, color='gray')
        ax.set_xlim(min_lon, max_lon)
        ax.set_ylim(min_lat, max_lat)

        # bus route scatter plot
        sns.scatterplot(x='Longitude', y='Latitude', data=route_details, color='blue', s=50, label='Bus Stops')

        # target coordinates 
        ax.scatter(target_coords[1], target_coords[0], color='red', s=100, label='Target Location')

        route_details.sort_values('StopSequence', inplace=True)
        first_stop_name = route_details.iloc[0]['Description']
        last_stop_name = route_details.iloc[-1]['Description']
        service_no = route_details.iloc[0]['ServiceNo']
        direction = route_details.iloc[0]['Direction']
        plot_title = f"Bus Service No. {service_no} Route (Direction {direction}) from {first_stop_name} to {last_stop_name}"
        plt.title(plot_title)
        
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        ax.legend()
        plt.show()
        

bus_routes = pd.read_csv("../../misc/data/Bus_Routes.csv")
bus_services = pd.read_csv("../../misc/data/Bus_Services.csv")
bus_stops = pd.read_csv("../../misc/data/Bus_Stops.csv")
passenger_vol_feb = pd.read_csv("../../misc/data/transport_node_bus_202402.csv")

bus_object = Bus_Stop_Finder(bus_routes, bus_services, bus_stops, passenger_vol_feb)
stadium_coords = (1.3040, 103.8748)
nearby_stops = bus_object.find_nearby_bus_stops(stadium_coords)
print(nearby_stops)

crowded_stops = bus_object.find_crowded_stops(nearby_stops)
print(crowded_stops)

crowded_stop_code = 80119 # stadium stn
less_crowded_alternatives = bus_object.find_less_crowded_alternatives(crowded_stop_code)
print(less_crowded_alternatives)

bus_services_at_stop = bus_object.find_buses_serving_stop(crowded_stop_code)
print(bus_services_at_stop)


route_details = bus_object.get_route_details('10', 1)
bus_object.chart_bus_route(route_details, stadium_coords)