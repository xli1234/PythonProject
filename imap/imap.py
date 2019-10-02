#!/usr/bin/env python
# coding: utf-8

# Modules
import numpy as np
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
map_file = str(Path(__file__).parent.absolute())+'/map_cache.npy'
load = True
try:
    map_cache = np.load(map_file)
except:
    load = False
    
apt_file = 'apt_file.npy'
try:
    apt_list = np.load(apt_file) # update this to be compatible, load exported data from apt.py and filter here
except:
    apt_list = [
        'Royal York',
        'Oakland Apartments',
        'Oak Hill Apartments',
        'The Bridge on Forbes',
        'Schenley Apartments',
        'One on Centre',
        'Portal Place',
        'Devon Towers',
        'Amberson Gardens',
        'Webster Hall',
        'Fairfax Apartments',
        'Ambassador Apartments',
        'North Windsor Apartments',
        'Shadyside Commons',
    ]
    addr_list = [
        '3955 Bigelow Blvd, Pittsburgh, PA 15213',
        '4629 Bayard St, Pittsburgh, PA 15213',
        '475 Garner Ct, Pittsburgh, PA 15213',
        '3423 Forbes Ave, Pittsburgh, PA 15213',
        '4101 Bigelow Blvd, Pittsburgh, PA 15213',
        '4500 Centre Ave, Pittsburgh, PA 15213',
        '2633 Fifth Ave, Pittsburgh, PA 15213',
        '4920 CENTRE Ave, Pittsburgh, PA 15213',
        '1-4 Bayard Rd, Pittsburgh, PA 15213',
        '101 N Dithridge St, Pittsburgh, PA 15213',
        '4614 5th Ave, Pittsburgh, PA 15213',
        '4733 Centre Ave, Pittsburgh, PA 15213',
        '234 Melwood Ave, Pittsburgh, PA 15213',
        '401 Amberson Ave, Pittsburgh, PA 15232',
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

# Helper function to create query, open url, call parse api and output one data
# Sample data: ['APT_NAM', 'DIS_DRI', 'TIM_DRI', ' DIS_WAL', 'TIM_WAL', 'DIS_BIC', 'TIM_BIC']
travel_mode = ['driving', 'walking', 'bicycling'] #, 'transit'] # do not support transit now, noise in sub-routes
def goog_map(apt_name, apt_addr):
    goog_map_data = [apt_name]
    for tm in travel_mode:
        link = 'https://www.google.com/maps/dir/?api=1&origin=' +                (apt_name+' '+apt_addr).replace(' ', '+') +                '&destination=CMU&travelmode=' + tm
        html = urlopen(link)
        bsyc = BeautifulSoup(html.read(), "lxml")
        time.sleep(5)
        fout = open(apt_name+' '+tm+'.txt', 'wt',encoding='utf-8')
        fout.write(str(bsyc))
        fout.close()
        goog_map_data += shortest_distance_time(bsyc)
    return goog_map_data


# Search
if load:
    apt_cache = map_cache[:,0].tolist() #[map_cache[r][0] for r in range(len(map_cache))]
else:
    apt_cache = [] # also needed to avoid duplicates
apt_data_list = [] # to store new apt_data
for apt,addr in zip(apt_list, addr_list):
    # Data in cache, skip search
    if apt in apt_cache:
        continue
    try:
        # Read one data
        apt_data = goog_map(apt, addr)
        # Add data
        apt_data_list.append(apt_data)
        # Avoid duplicate
        apt_cache.append(apt)
    except:
        iprint('Unable to read more map. Save current data.')
        break

# Add new data to cache
if apt_data_list:
    if load:
        map_cache = np.concatenate((map_cache, np.array(apt_data_list)), axis = 0)
    else:
        map_cache = np.array(apt_data_list)
# else: do nothing to map_cache


# Check current cache, old + new data
iprint(map_cache)
# Save all data
np.save(map_file, map_cache)


