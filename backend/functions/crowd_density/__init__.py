"""gets crowd density from platforms"""
import os
from typing import List
from enum import Enum
from requests import get
from pprint import pprint
from ..utils.api import lta_api


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


station_map = {"NS10": "Admiralty", "EW9": "Aljunied", "NS16": "Ang Mo Kio", "CR2": "Aviation Park", "JS7": "Bahar Junction", "SE3": "Bakau", "BP9": "Bangkit", "CC12": "Bartley", "DT16": "Bayfront", "CE1": "Bayfront", "TE29": "Bayshore", "DT5": "Beauty World", "EW5": "Bedok", "DT29": "Bedok North", "DT30": "Bedok Reservoir", "TE30": "Bedok South", "DT21": "Bencoolen", "DT23": "Bendemeer", "NS17": "Bishan", "CC15": "Bishan", "NE9": "Boon Keng", "EW27": "Boon Lay", "DT9": "Botanic Gardens", "CC19": "Botanic Gardens", "NS18": "Braddell", "CC2": "Bras Basah", "TE7": "Bright Hill", "NE15": "Buangkok", "EW12": "Bugis", "DT14": "Bugis", "NS2": "Bukit Batok", "JE3": "Bukit Batok West", "NS3": "Bukit Gombak", "DT1": "Bukit Panjang", "BP6": "Bukit Panjang", "EW21": "Buona Vista", "CC22": "Buona Vista", "CC17": "Caldecott", "TE9": "Caldecott", "DT2": "Cashew", "CG2": "Changi Airport", "SW1": "Cheng Lim", "NE4": "Chinatown", "DT19": "Chinatown", "EW25": "Chinese Garden", "NS4": "Choa Chu Kang", "BP1": "Choa Chu Kang", "JS2": "Choa Chu Kang West", "NS25": "City Hall", "EW13": "City Hall", "NE5": "Clarke Quay", "EW23": "Clementi", "EW20": "Commonwealth", "SE1": "Compassvale", "PE3": "Coral Edge", "JS5": "Corporation", "PE1": "Cove", "CC8": "Dakota", "PE7": "Damai", "CR7": "Defu", "NS24": "Dhoby Ghaut", "NE6": "Dhoby Ghaut", "CC1": "Dhoby Ghaut", "EW22": "Dover", "DT17": "Downtown", "CP2": "Elias", "JS9": "Enterprise", "CC3": "Esplanade", "EW7": "Eunos", "DT35": "Expo", "CG1": "Expo", "BP10": "Fajar", "SW2": "Farmway", "NE8": "Farrer Park", "CC20": "Farrer Road", "SW5": "Fernvale", "DT20": "Fort Canning", "TE22A": "Founders' Memorial", "TE22": "Gardens by The Bay", "JW1": "Gek Poh", "DT24": "Geylang Bahru", "TE15": "Great World", "EW30": "Gul Circle", "NE1": "HarbourFront", "CC29": "HarbourFront", "TE16": "Havelock", "CC25": "Haw Par Villa", "DT3": "Hillview", "CC21": "Holland Village", "JS4": "Hong Kah", "NE14": "Hougang", "DT22": "Jalan Besar", "BP12": "Jelapang", "EW29": "Joo Koon", "NS1": "Jurong East", "EW24": "Jurong East", "JS11": "Jurong Hill", "CR19": "Jurong Lake District", "JS12": "Jurong Pier", "JE6": "Jurong Town Hall", "JS6": "Jurong West", "PE5": "Kadaloor", "DT28": "Kaki Bukit", "EW10": "Kallang", "SE4": "Kangkar", "TE24": "Katong Park", "BP3": "Keat Hong", "EW6": "Kembangan", "CC24": "Kent Ridge", "NS14": "Khatib", "DT6": "King Albert Park", "NE13": "Kovan", "NS7": "Kranji", "SW3": "Kupang", "CC27": "Labrador Park", "EW26": "Lakeside", "EW11": "Lavender", "SW6": "Layar", "TE5": "Lentor", "NE7": "Little India", "DT12": "Little India", "CC14": "Lorong Chuan", "CR3": "Loyang", "DT26": "MacPherson", "CC10": "MacPherson",
               "CR16": "Maju", "NS27": "Marina Bay", "CE2": "Marina Bay", "TE20": "Marina Bay", "TE21": "Marina South", "NS28": "Marina South Pier", "TE26": "Marine Parade", "TE27": "Marine Terrace", "NS8": "Marsiling", "CC16": "Marymount", "DT25": "Mattar", "TE18": "Maxwell", "TE6": "Mayflower", "PE2": "Meridian", "TE10": "Mount Pleasant", "CC7": "Mountbatten", "JW4": "Nanyang Crescent", "JW3": "Nanyang Gateway", "TE12": "Napier", "NS21": "Newton", "DT11": "Newton", "PW5": "Nibong", "CC5": "Nicoll Highway", "NS20": "Novena", "PE6": "Oasis", "CC23": "one-north", "NS22": "Orchard", "TE14": "Orchard", "TE13": "Orchard Boulevard", "NE3": "Outram Park", "EW16": "Outram Park", "TE17": "Outram Park", "JE7": "Pandan Reservoir", "CC26": "Pasir Panjang", "EW1": "Pasir Ris", "CR4": "Pasir Ris East", "EW8": "Paya Lebar", "CC9": "Paya Lebar", "BP8": "Pending", "JW5": "Peng Kang Hill", "BP7": "Petir", "BP5": "Phoenix", "EW28": "Pioneer", "NE10": "Potong Pasir", "DT15": "Promenade", "CC4": "Promenade", "NE17": "Punggol", "PW3": "Punggol Point", "EW19": "Queenstown", "NS26": "Raffles Place", "EW14": "Raffles Place", "SE5": "Ranggung", "EW18": "Redhill", "SW8": "Renjong", "PE4": "Riviera", "CP3": "Riviera", "DT13": "Rochor", "SE2": "Rumbia", "PW1": "Sam Kee", "PW4": "Samudera", "BP11": "Segar", "NS11": "Sembawang", "STC": "Sengkang", "NE16": "Sengkang", "BP13": "Senja", "NE12": "Serangoon", "CC13": "Serangoon", "CR9": "Serangoon North", "TE19": "Shenton Way", "TE28": "Siglap", "EW3": "Simei", "DT7": "Sixth Avenue", "NS23": "Somerset", "PW7": "Soo Teck", "BP2": "South View", "TE4": "Springleaf", "CC6": "Stadium", "DT10": "Stevens", "TE11": "Stevens", "PW6": "Sumang", "TE31": "Sungei Bedok", "CC11": "Tai Seng", "EW2": "Tampines", "DT32": "Tampines", "DT33": "Tampines East", "CR6": "Tampines North", "DT31": "Tampines West", "DT8": "Tan Kah Kee", "EW4": "Tanah Merah", "TE25": "Tanjong Katong", "EW15": "Tanjong Pagar", "TE23": "Tanjong Rhu", "CR10": "Tavistock", "JW2": "Tawas", "CR12": "Teck Ghee", "PW2": "Teck Lee", "BP4": "Teck Whye", "DT18": "Telok Ayer", "CC28": "Telok Blangah", "BP14": "Ten Mile Junction", "JS3": "Tengah", "JE2": "Tengah Park", "JE1": "Tengah Plantation", "SW4": "Thanggam", "EW17": "Tiong Bahru", "NS19": "Toa Payoh", "JE4": "Toh Guan", "SW7": "Tongkang", "EW31": "Tuas Crescent", "EW33": "Tuas Link", "EW32": "Tuas West Road", "JS10": "Tukang", "CR14": "Turf City", "DT27": "Ubi", "DT34": "Upper Changi", "TE8": "Upper Thomson", "CR18": "West Coast", "NS9": "Woodlands", "TE2": "Woodlands", "TE1": "Woodlands North", "TE3": "Woodlands South", "NE11": "Woodleigh", "NS5": "Yew Tee", "NS15": "Yio Chu Kang", "NS13": "Yishun"}
station_density = {"l": "Low", "m": "Moderate",
                   "h": "High", "na": "Not Applicable"}


def get_crowd_density(station: str) -> List[object]:
    """returns list of crowd densities"""
    line_map = {"CIRCLE_LINE": "CCL",
                "CIRCLE_LINE_EXT": "CEL",
                "CHANGI_EXT": "CGL",
                "DOWNTOWN_LINE": "DTL",
                "EAST_WEST_LINE": "EWL",
                "NORTH_EAST_LINE": "NEL",
                "NORTH_SOUTH_LINE": "NWL",
                "BUKIT_PANJANG_LRT": "BPL",
                "SENGKANG_LRT": "SLRT",
                "PUNGGOL_LRT": "PLRT"}
    station_code = line_map[station]
    response = lta_api(f"PCDRealTime?TrainLine={station_code}")
    data = response.json()
    values = data["value"]
    return {"value": [{"station": station_map[value["Station"]], "crowd_level": station_density[value["CrowdLevel"]]} for value in values]}


if __name__ == "__main__":
    dens = get_crowd_density(Stations.CIRCLE_LINE.value)
    pprint(dens)
