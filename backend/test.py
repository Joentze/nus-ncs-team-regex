from functions.traffic_messages.message import Message
from functions.carpark.carpark import Carpark

if __name__ == "__main__":
    # obj = Message()
    # events = obj.get_events("TrafficIncidents")
    # for e in events:
    #     print(f"{e.id}, \n {e.address}, \n {e.message}")

    carpark = Carpark()
    top5 = carpark.get_top_5_closest_carparks("1.356520 103.829805")
    print(top5)

    



