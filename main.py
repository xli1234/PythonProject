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
# import crime_final as crime
import imap
from apartment.add_geocode import add_geocode
from apartment.house_summary import summary_house
from restaurant.clean_restaurant import clean_restaurant
from visualization.add_score import add_score
from visualization.calculate_score import calculate_score
from visualization.map_visualization import map_visualize


# # Example of using data from module
# print(crime.df2)
# print(imap.map_data)


# # run add_geocode()
# add_geocode()
# print('add geocode: done')


# # run clean_restaurant()
# clean_restaurant()
# print('restaurant data clean: done')


# # run add_score()
# add_score()
# print('add apartment score: done')


# get user input
# print('Areas nearby CMU:')
# summary_house()
# print('Enter areas to explore:')
# print('Pittsburgh'.rjust(20) + ':  0')
# print('Oakland'.rjust(20) + ':  1')
# print('Squirrel Hill'.rjust(20) + ':  2')
# print('Shadyside'.rjust(20) + ':  3')
# area_choice = eval(input())
# print('Tell us how important are these factors to you on a 1-5 scale:')
# print('    1: Not at all important')
# print('    2: Slightly Important')
# print('    3: Important')
# print('    4: Fairly Important')
# print('    5: Very Important')
# weight_c = eval(input('Safety of the neighbourhood: ')) # weight for crime
# weight_r = eval(input('Convenience to eat at the neighbourhood: ')) # weight for restaurant
# weight_t = eval(input('Convenience of going school from home and back: ')) # weight for transportation
# print('    1: Drive')
# print('    2: Walk')
# print('    3: Bike')
# trans_choice = eval(input('How will travel from home to campus or back: '))
# calculate_score(weight_c, weight_r, weight_t, area_choice, trans_choice)
calculate_score(area_choice=3)

# # call map_visualize()
# apt_name = 'Royal York'
# apt_lat = 40.453150
# apt_lng = -79.953920
# crime_percentage = 0.398
# distance = 1385
# time = [366, 1006, 371]
# map_visualize(apt_name=apt_name, apt_lat=apt_lat, apt_lng=apt_lng, 
# 				crime=crime_percentage, distance=distance, time=time)
