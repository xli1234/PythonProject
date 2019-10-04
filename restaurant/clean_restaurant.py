#!/usr/bin/env python
# coding: utf-8


import pandas as pd

def clean_restaurant():
    file_path = 'restaurant/business.json' # downloaded from https://www.yelp.com/dataset
    f = open(file_path, 'r')
    i = 0
    cols = ['business_id', 'name', 'address', 'city', 'state', 'postal_code', 'latitude', 'longitude', 'stars', 'review_count', 'is_open', 'attributes', 'categories', 'hours']
    df = pd.DataFrame(columns = cols)
    df['attributes'] = df['attributes'].astype(str)
    for line in f.readlines():
        if '"city":"Pittsburgh"' in line:
    #         print(eval(line.strip().replace('null', '""')))
            df = pd.concat([df, pd.DataFrame(eval(line.strip().replace('null', '""')), index=[i])], ignore_index=True)
            i = i + 1
    f.close()
    
    
    # only columns we will need
    cols = ['name', 'address', 'city', 'state', 'postal_code', 'latitude', 'longitude', 'stars', 'review_count', 'is_open', 'categories']
    # only zip code in (15213, 15217, 15232)
    # save to csv format
    df[((df.postal_code == '15213') | (df.postal_code == '15217') | (df.postal_code == '15232'))][cols].to_csv('restaurant/restaurant.csv', index = False) 







