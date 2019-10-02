#!/usr/bin/env python
# coding: utf-8

# Modules
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
from pathlib import Path

# Settings:

def iprint(*args):
    if __name__ == '__main__':
        for arg in args:
            print(arg, end=' ')
        print('')

# Load
filename = str(Path(__file__).parent.absolute())+'/map_cache.csv'
try:
    map_data = pd.read_csv(filename)
    map_data = map_data.set_index('APT')
except:
    map_data = pd.DataFrame(columns=['DIS_DRI', 'TIM_DRI', ' DIS_WAL', 'TIM_WAL', 'DIS_BIC', 'TIM_BIC'])
    map_data.index.name = 'APT'
    
# import or use apt+address from apartment module
apt_list = [
    'Royal York',
    'Oakland Apartments',
]
addr_list = [
    '3955 Bigelow Blvd, Pittsburgh, PA 15213',
    '4629 Bayard St, Pittsburgh, PA 15213',
]

# Map Helper
def shortest_distance_time(arg):
    text = str(arg) # arg = bsyc
    end_idx = 0
    shortest_distance = 0
    shortest_time = 0
    while end_idx != -1:
        # Get distance
        end_idx = text.find(' mile', end_idx+1)
        if end_idx == -1:
            break
        start_idx = end_idx
        while(text[start_idx-1] != '['):
            start_idx -= 1
        end_idx = text.find(',', start_idx)
        distance = int(text[start_idx : end_idx])
        if shortest_distance != 0 and distance > shortest_distance: # Only do shortest distance
            end_idx = text.find(']', end_idx) # move cursor after 'mile'
            continue
        shortest_distance = distance
        # Get time for shortest distance
        start_idx = text.find('[', end_idx) + 1
        end_idx = text.find(',', start_idx)
        shortest_time = int(text[start_idx : end_idx]) # small bug, we are using new time not shortest_time if same shortest_distance
    return [shortest_distance, shortest_time]

# Helper function to create query, open url, call parse api and output one data entry
# Data Column format ['DIS_DRI', 'TIM_DRI', ' DIS_WAL', 'TIM_WAL', 'DIS_BIC', 'TIM_BIC']
travel_mode = ['driving', 'walking', 'bicycling'] #, 'transit'] # do not support transit now, noise in sub-routes
def goog_map(apt_name, apt_addr):
    goog_map_data = []
    for tm in travel_mode:
        link = 'https://www.google.com/maps/dir/?api=1&origin='+(apt_name+' '+apt_addr).replace(' ','+')+'&destination=CMU&travelmode='+tm
        html = urlopen(link)
        bsyc = BeautifulSoup(html.read(), "lxml")
        time.sleep(5)
        fout = open(apt_name+' '+tm+'.txt', 'wt',encoding='utf-8')
        fout.write(str(bsyc))
        fout.close()
        goog_map_data += shortest_distance_time(bsyc)
    return goog_map_data


# Search
for apt,addr in zip(apt_list, addr_list):
    # Data in cache, skip search
    if apt in map_data.index:
        continue
    try:
        # Read one data
        apt_data = goog_map(apt, addr)
        # Add row to DataFrame
        map_data.loc[apt] = apt_data
    except:
        iprint('Unable to read more map. Save current data.')
        break

# Check current cache, old + new data
iprint(map_data)
# Save all data
map_data.to_csv(filename)

