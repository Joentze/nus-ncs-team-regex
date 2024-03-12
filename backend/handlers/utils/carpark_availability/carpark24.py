#Pull Carpark Availability Data every hour for 24 hours.

import requests
import pandas as pd
import schedule
import time
from datetime import datetime, timedelta



def get_carpark_data24():
    global all_data
    
    url = "http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2"
    headers = {
        "AccountKey": "5CU91Z3YRrC4dvEJmnF8Hw==",
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        carpark_data = data['value']
        df = pd.DataFrame(carpark_data)
        df['timestamp'] = datetime.now()
        all_data = pd.concat([all_data, df],ignore_index=True)
    else:
        print("Error:", response.status_code)
        print(response.text)
        
for i in range(24):
    schedule.every().hour.do(get_carpark_data24).tag('fetch_data')


for _ in range(24):
    schedule.run_pending()
    time.sleep(3600)  



current_datetime = datetime.now()
previous_datetime = current_datetime - timedelta(days=1)

# Format the previous date as DDMMYYYY
previous_date_string = previous_datetime.strftime("%d%m%Y")
# Concatenate the previous date with the filename
filename = f"carpark_data_{previous_date_string}.csv"
# Save the dataframe to CSV with the concatenated filename
all_data.to_csv(filename, index=False)
all_data = pd.DataFrame()
