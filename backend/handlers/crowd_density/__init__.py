"""gets crowd density from platforms"""
import os
from typing import List
from enum import Enum
from requests import get
from pprint import pprint

API_KEY = os.environ["API_KEY"]


class Stations(Enum):
    """enums for stations"""
    CIRCLE_LINE = "CCL"
    CIRCLE_LINE_EXT = "CEL"
    CHANGI_EXT = "CGL"
    DOWNTOWN_LINE = "DTL"
    EAST_WEST_LINE = "EWL"
    NORTH_EAST_LINE = "NEL"
    NORTH_SOUTH_LINE = "NWL"
    BUKIT_PANJANG_LRT = "BPL"
    SENGKANG_LRT = "SLRT"
    PUNGGOL_LRT = "PLRT"


def get_crowd_density(station: Stations) -> List[object]:
    """returns list of crowd densities"""
    url_route = f"http://datamall2.mytransport.sg/ltaodataservice/PCDRealTime?TrainLine={station}"
    response = get(url_route, headers={
                   "AccountKey": API_KEY, "Accept": "application/json"}, timeout=5000)
    return response.json()


if __name__ == "__main__":
    dens = get_crowd_density(Stations.CIRCLE_LINE.value)
    pprint(dens)
