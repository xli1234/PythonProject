#!/usr/bin/env python
# coding: utf-8

# Modules
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
from pathlib import Path

# Settings
# Do not print if import as module
def iprint(*args):
    if __name__ == '__main__':
        for arg in args:
            print(arg, end=' ')
        print('')

# Load
filename = str(Path(__file__).parent.absolute())+'/map_cache.csv'
try:
    # Get DataFrame from cache if any
    map_data = pd.read_csv(filename)
    map_data = map_data.set_index('APT')
except:
    # If no previous valid cache, let's begin with an empty DF
    map_data = pd.DataFrame(columns=['DRIV_DIST', 'DRIV_TIME', ' WALK_DIST', 'WALK_TIME', 'BIKE_DIST', 'BIKE_TIME'])
    map_data.index.name = 'APT'
    
# import or use apt+address from apartment module
apt_list = [
    'Royal York',
    'Oakland Apartments',
    'Oak Hill Apartments',
    'Wendover Apartments',
]
addr_list = [ # replace with zip_list if needed
    '3955 Bigelow Blvd, Pittsburgh, PA 15213',
    '4629 Bayard St, Pittsburgh, PA 15213',
    '475 Garner Ct Suite 215, Pittsburgh, PA 15213'
    '5562 Hobart St, Pittsburgh, PA 15217',
]

# Map Data Scraping Function
# Sample format [1987,\"1.2 miles\",1]\n,[366,\"6 min\"]
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
        # Only do shortest distance
        if shortest_distance != 0 and distance >= shortest_distance:
            # move cursor after 'mile'
            end_idx = text.find(']', end_idx)
            continue
        shortest_distance = distance
        # Get time for shortest distance
        start_idx = text.find('[', end_idx) + 1
        end_idx = text.find(',', start_idx)
        # Assume google lists shorter time first for same distance
        shortest_time = int(text[start_idx : end_idx])
    if shortest_distance == 0: # too close, < 0.1 mile and unit is ft
        return ['< 160', 'FAST']
    return [shortest_distance, shortest_time]

# Let's not support transit now, noise in sub-routes
travel_mode = ['driving', 'walking', 'bicycling'] #, 'transit']

# Function to create query, open url, call scraping and return one data entry
def goog_map(apt, addr):
    goog_map_data = []
    for tm in travel_mode:
        destination = 'Carnegie Mellon University, 5000 Forbes Ave, Pittsburgh, PA 15213'.replace(' ','+')
        idx = apt.find('#')
        if (idx > 0):
            origin = (apt[:idx] + addr).replace(' ','+')
        else:
            origin = (apt + ' ' + addr).replace(' ','+')
        link = 'https://www.google.com/maps/dir/?api=1&origin='+origin+'&destination='+destination+'&travelmode='+tm
        html = urlopen(link)
        bsyc = BeautifulSoup(html.read(), "lxml")
        time.sleep(5)
        # Save raw data if Professor asks for it
        #fout = open(apt+' '+tm+'.txt', 'wt',encoding='utf-8')
        #fout.write(str(bsyc))
        #fout.close()
        goog_map_data += shortest_distance_time(bsyc)
    return goog_map_data

# Search
iprint('Current map_data:')
iprint(map_data)
idx = 0
for apt,addr in zip(apt_list, addr_list):
    idx += 1;
    # Skip apt that exists in DF
    if apt == 'Address Not Disclosed' or apt in map_data.index:
        continue
    try:
        # Add row to DataFrame
        iprint('Updating...(', idx,'/',len(apt_list),')')
        map_data.loc[apt] = goog_map(apt, addr)
        iprint(map_data.loc[apt].to_frame().T)
    except:
        iprint('Unable to read more map. Save current data.')
        break

# Check updated DF
iprint('\nUpdating map_data done.')
iprint(map_data)
# Save our DF
map_data.to_csv(filename)

