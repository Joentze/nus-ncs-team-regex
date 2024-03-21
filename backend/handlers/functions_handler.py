from functions.carpark.carpark import Carpark
from functions.bus.Bus_Stop_Functions import Bus_Stop_Finder
from functions.public_transport.public_transport import PublicTransportFinder
from functions.traffic_messages.message import Message
from functions.traffic_speed.traffic_flow_call import Traffic_Speed
from functions.utils.geocode import geocode
import spacy
from spacy.training import Example 
import pandas as pd
import asyncio
import traceback

#methods - two methods

def identify_location(nlp, prompt):
    coords = []
    doc = nlp(prompt)
    locations = [ent.text for ent in doc.ents if ent.label_ == "SG_ROAD"]
    geocoder = geocode()
    print(locations)
    for loc in locations:
        # if "road" in loc.lower():
        #     loc.replace("road", "")
        try: 
            coord = asyncio.run(geocoder.forward(f"{loc}, Singapore"))
            coords.append(coord)
        except Exception as e:
            continue

    if coords:
        return coords[0]
    else:
        return False

class Augmented_Prompt():
    data_prompt = "Data that the user cannot see: \n"

    def __init__(self, coords, original_prompt):
        self.coords = coords
        self.original_prompt = original_prompt

    async def construct(self, type = "Live"):
        if type == "Live":
            tasks = [
                self.get_traffic_data(),
                self.get_carpark_data(),
                self.get_mrt_data(),
                self.get_message_data(),
                self.get_bus_data()
            ]

            results = await asyncio.gather(*tasks)
            self.data_prompt += results[0] 
            self.data_prompt += results[1] 
            self.data_prompt += results[2] 
            self.data_prompt += results[3] 
            self.data_prompt += results[4] 
            self.data_prompt += "\nRequest:\n\n Please provide the following, prioritizing safety and efficient congestion reduction, provide a actionable, straightforward, data-driven answer for the question below and explain the logic:\n"
            self.data_prompt += self.original_prompt

            return self.data_prompt

    async def get_traffic_data(self):
        #traffic data
        try:
            traffic_finder = Traffic_Speed()
            speedMessage, roadName, distance = traffic_finder.get_speed(self.coords)
            traffic_prompt = f"\nDetected {speedMessage} at {roadName} about {distance}m away from users location\n"

            return traffic_prompt
        
        except Exception as e:
            traceback.print_exc() 
            

    async def get_carpark_data(self):
        #carpark data
        try:
            carpark_prompt = "\n Below is the Carpark situation for developments around the area:\n"
            carpark_finder = Carpark()
            available_carparks = carpark_finder.get_top_5_closest_carparks(self.coords)
            for index, row in available_carparks.iterrows():
                carpark_prompt += f"Development: Carpark @ {row['Development']}, Lots Available: {row['AvailableLots']}\n"

            return carpark_prompt
        except:
            print("Failed to retrieve Carpark Data")

    async def get_mrt_density(self):
        pass

    async def get_mrt_data(self):
        #low density stations
        try: 
            mrt_prompt = "\n Below are the train stations nearby that have low crowd density: \n"
            mrt_finder = PublicTransportFinder()
            stations = mrt_finder.get_low_density_nearby_stations(self.coords)
            mrt_prompt += ", ".join(stations)

            return mrt_prompt
        except Exception as e:
            traceback.print_exc() 

    async def get_message_data(self):       
        #messages
        try:
            message_prompt = ""
            message_finder = Message()
            #fetches list of messages
            traffic_incidents = message_finder.get_events("TrafficIncidents", self.coords)
            vms = message_finder.get_events("VMS", self.coords)
            message_prompt += "\n Below are Traffic Incidents within a 3km radius of the location: \n"
            message_prompt += "\n".join(traffic_incidents)
            message_prompt += "\n Below are VMS messages within a 3km radius of the location: \n"
            message_prompt += "\n".join(vms)
            
            return message_prompt
        except Exception as s:
            traceback.print_exc() 

                
        #bus stop
    async def get_bus_data(self): 
        try:
            bus_prompt = "\n \n Below are the nearby bus stops that are crowded: "
            busstop_finder = Bus_Stop_Finder()
            coords = self.coords.split(",")
            nearby_stops = busstop_finder.find_nearby_bus_stops((float(coords[0]), float(coords[1])))
            crowded_stops = busstop_finder.find_crowded_stops(nearby_stops.head(5))
            for index, row in crowded_stops.iterrows():
                bus_prompt += f"Bus stop {row['PT_CODE']} at {row['RoadName']} has {row['Total_Tap_In']} tap ins \n"
                if index == 1:
                    crowded_stop_name = row['RoadName']
                    crowded_stop_code = row['PT_CODE']

            less_crowded_alternatives = busstop_finder.find_less_crowded_alternatives(crowded_stop_code).head(3)
            bus_prompt += f"\n These are some of the alternatives for more crowded bus stop @ {crowded_stop_name} with code {crowded_stop_code}: \n"
            for index, row in less_crowded_alternatives.iterrows():
                bus_prompt += f"Alternative bus stop {row['PT_CODE']} at {row['RoadName']} has {row['Total_Tap_In']} tap ins \n"

            return bus_prompt
        
            # 'PT_CODE', 'RoadName', 'Description', 'Total_Tap_In', 'Total_Tap_Out'
        
        except Exception as s:
            traceback.print_exc() 

    


# Data:

# Roads:
# Stadium Crescent: Average speed 1.5 km/h
# Nicoll Highway & Mountbatten Road: Average speed 35 km/h (alternate routes)
# Carpark: 800 spaces available in carpark 300m from the stadium.
# MRT:
# Platform 95% capacity
# Estimated 30-minute wait before boarding
# Platform density 5 people/sq meter
# Bus Stop:
# 1500 people waiting, queue 100m beyond bus stop
# Next bus in 3 minutes (normal capacity: 100)
# VMS:
# Traffic breakdown at road connected to nicoll highway

def main():
    nlp = spacy.load("misc/NEP2") 
    original_prompt = "The Taylor Swift Eras Concert has just ended, we have 50000 attendees and there is a severe congestion around the roads near Marina Bay Sands. As Authorities, what can we do to better manage the traffic and Crowds"
    extracted_coords = identify_location(nlp, original_prompt)
    if extracted_coords:
        a_prompt = Augmented_Prompt(extracted_coords, original_prompt)
        prompt = asyncio.run(a_prompt.construct())
        print(prompt)
    



if __name__ == "__main__":
    pass
    # data = generate_training_data(road_names)
    # print(data)
    # scores = nlp.evaluate(data)
    # precision = scores["ents_p"]
    # recall = scores["ents_r"]
    # f1_score = scores["ents_f"]

    # # Print evaluation results
    # print("Precision:", precision)
    # print("Recall:", recall)
    # print("F1 Score:", f1_score)

# roads = pd.read_csv("/misc/road_network.csv")
# road_names = list(roads["road"])

# Simplified training data generation
# def generate_training_data(roads):
#     data = []
#     for road in roads[3300:3900]:  # Adjust slice for batching
#         sentence = f"There is heavy congestion on {road}."
#         entities = [(len(f"There is heavy congestion on "), len(sentence) - 1, "SG_ROAD")]
#         example = Example.from_dict(nlp.make_doc(sentence), {"entities": entities})
#         data.append(example)
#     return data

