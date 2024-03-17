import pandas as pd
import asyncio
from functions.traffic_messages.message import Message
from functions.carpark.carpark import Carpark
from functions.public_transport.public_transport import PublicTransportFinder
from functions.crowd_density import Stations, get_crowd_density
from functions.traffic_speed.traffic_flow_call import main

if __name__ == "__main__":
    # Traffic_flow (Nic)
    traffic_flow = asyncio.run(main("./misc/stadium-roads-table.csv"))
    print(traffic_flow)

    # Message (Jerric)
    obj = Message()
    events = obj.get_events("TrafficIncidents")
    for e in events:
        print(f"{e.id}, \n {e.address}, \n {e.message}")

    # Carpark (Emmanuel)
    carpark = Carpark()
    top5 = carpark.get_top_5_closest_carparks("1.356520 103.829805")
    print(top5)

    # MRT and BUS Station (Ethan / Wei Xuan)

    mrt_station_df = pd.read_csv("./misc/data/MRT Stations.csv")
    bus_stops_df = pd.read_csv("./misc/data/bus_stops.csv")

    public_transport_object = PublicTransportFinder(mrt_station_df, bus_stops_df)
    nearby_stations = public_transport_object.find_nearby_mrts(
    1.3129816930513392, 103.88709040919767
    )

    low_density_stations_nearby = public_transport_object.get_low_density_nearby_stations(
        1.3129816930513392, 103.88709040919767
    )

    print(nearby_stations)
    print(low_density_stations_nearby)

    #Station Crowd Density (Joen)
    dens = get_crowd_density(Stations.CIRCLE_LINE.value)
    print(dens)



