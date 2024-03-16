import asyncio
import datetime
import time
import json
import aiohttp
import csv
import os
from collections import defaultdict


async def fetch_data(host, databatch, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(host + str(databatch), headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(
                    f"Error getting data batch {databatch}: {response.status}")
                return None


async def main():
    # use the API key as needed
    api_key = os.environ['LTA_API_KEY']

    host = "http://datamall2.mytransport.sg/ltaodataservice/v3/TrafficSpeedBands?$skip="
    headers = {"AccountKey": api_key,
               "accept": "application/json"}
    # defaultdict with default value of an empty dict
    everything = defaultdict(dict)
    roads = {}
    databatch = 0

    # creating a dictionary of roads that we need
    with open('stadium-roads-table.csv', 'r') as f:
        relevant = csv.reader(f)
        next(relevant)
        for rel_roadname, rel_lineid in relevant:
            if rel_roadname not in roads:
                roads[rel_roadname] = []
            roads[rel_roadname].append(rel_lineid)

    while True:
        task = asyncio.create_task(fetch_data(host, databatch, headers))
        api_call = await task

        # Check for final API call
        if len(api_call['value']) < 500:
            break

        # Filtering out the needed data
        updated = api_call['lastUpdatedTime']
        everything['time'] = updated
        for entry in api_call['value']:
            roadname = entry['RoadName']
            # Will only add to dictionary if in "roads" - for Stadium Area roads only
            # To be updated: the LinkID as well to get more granular data
            linkid = entry["LinkID"]
            if roadname in roads and linkid in roads[roadname]:
                everything[roadname][linkid] = {"RoadCategory": entry["RoadCategory"],
                                                "SpeedBand": entry["SpeedBand"],
                                                "StartLon": entry["StartLon"],
                                                "StartLat": entry["StartLat"],
                                                "EndLon": entry["EndLon"],
                                                "EndLat": entry["EndLat"]}

        databatch += 500
        print(f'pulled databatch #{databatch}')
        time.sleep(0.005)

    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f".\data\{date}_road_data.json", "w") as outfile:
        json.dump(everything, outfile, indent=1)

if __name__ == "__main__":
    asyncio.run(main())