# Project Apartment

# add all directory paths
import sys
from pathlib import Path
crime_path = str(Path(__file__).parent.absolute()) + '/crime'
imap_path = str(Path(__file__).parent.absolute()) + '/imap'
rest_path = str(Path(__file__).parent.absolute()) + '/restaurant'
apt_path = str(Path(__file__).parent.absolute()) + '/apartments'
sys.path.insert(1, crime_path)
sys.path.insert(1, imap_path)
sys.path.insert(1, rest_path)
sys.path.insert(1, apt_path)


# import individual modules
import crime_final as crime
import imap
from apartment.add_geocode import add_geocode
from restaurant.clean_restaurant import clean_restaurant
from visualization.map_visualization import map_visualize


# Example of using data from module
print(crime.df2)
print(imap.map_data)


# run add_geocode()
add_geocode()
print('add geocode: done')


# run clean_restaurant()
clean_restaurant()
print('restaurant data clean: done')


# call map_visualize
apt_name = 'Royal York'
apt_lat = 40.453150
apt_lng = -79.953920
crime_percentage = 0.398
distance = 1385
time = [366, 1006, 371]
map_visualize(apt_name=apt_name, apt_lat=apt_lat, apt_lng=apt_lng, 
				crime=crime_percentage, distance=distance, time=time)
