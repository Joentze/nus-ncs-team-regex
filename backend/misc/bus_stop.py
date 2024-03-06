import requests
import os
import pandas as pd

bus_stops = os.environ.get(
    "OS_ENVIRON_BUSSTOP_URL",
)

DATAMALL_API_KEY = os.environ.get("dataMall_API_KEY")

params = {"AccountKey": DATAMALL_API_KEY}

response = requests.get(bus_stops, headers=params)

if response.status_code == 200:
    bus_stop_data = response.json()["value"]
    df = pd.DataFrame(bus_stop_data)

    # Now you can perform analysis on the DataFrame
    print(df.head())
    df.to_csv("bus_stops.csv", index=False)
else:
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content)
