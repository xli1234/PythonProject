# Project Apartment

# add all directory paths
# import sys
# from pathlib import Path
# crime_path = str(Path(__file__).parent.absolute()) + '/crime'
# imap_path = str(Path(__file__).parent.absolute()) + '/imap'
# rest_path = str(Path(__file__).parent.absolute()) + '/restaurant'
# apt_path = str(Path(__file__).parent.absolute()) + '/apartment'
# sys.path.insert(1, crime_path)
# sys.path.insert(1, imap_path)
# sys.path.insert(1, rest_path)
# sys.path.insert(1, apt_path)
import pandas as pd
import numpy as np

# import individual modules
from imap.scrape_route import scrape_route
from apartment.house_listings import scrape_house_data
from apartment.add_geocode import add_geocode
from apartment.house_summary import summary_house

from crime.crime_final import crime_clean
from crime.crime_final import crime_stats

from restaurant.clean_restaurant import clean_restaurant

from visualization.add_score import add_score
from visualization.calculate_score import get_top5
from visualization.map_visualization import map_visualize


# # Example of using data from module
# print(crime.df2)
# print(imap.map_data)

print('--------------------------------------------------------------------')
print('1. Exploring Apartments')
print('2. Setting')
print('3. Exit')
choice = eval(input('Please enter number to choose: '))
while choice != 3:
	
	if choice == 1:
		# get user input
		print('--------------------------------------------------------------------')
		print('Areas nearby CMU:')
		summary_house()
		print('--------------------------------------------------------------------')
		y_or_n = input('Show crime comparison (Press Enter to continue):')
		if y_or_n == '':	
			# run crime_stats()
			crime_stats()
		print('--------------------------------------------------------------------')
		print('    0: All three areas')
		print('    1: Oakland')
		print('    3: Squirrel Hill')
		print('    4: Shadyside')
		area_choice = eval(input('Enter areas to explore: '))
		print('--------------------------------------------------------------------')
		print('Tell us how important are these factors to you on a 1-5 scale:')
		print('    1: Not at all important')
		print('    2: Slightly Important')
		print('    3: Important')
		print('    4: Fairly Important')
		print('    5: Very Important')
		weight_c = eval(input('Safety of the neighbourhood: ')) # weight for crime
		weight_r = eval(input('Convenience to eat at the neighbourhood: ')) # weight for restaurant
		weight_t = eval(input('Convenience of going school from home and back: ')) # weight for transportation
		print('--------------------------------------------------------------------')
		print('    1: Drive')
		print('    2: Walk')
		print('    3: Bike')
		trans_choice = eval(input('How will travel from home to campus or back: '))
		print('--------------------------------------------------------------------')
		top5 = get_top5(weight_c, weight_r, weight_t, area_choice, trans_choice).reset_index(drop=True).replace(np.nan, '')
		print('Here\'s our top 5 recommendation for you:')
		print(top5[['Zip','Street','Region','Price','Bedrooms','Bathrooms','Floorspace','Pet_friendly','Furnished']])
		
		# call map_visualize()
		y_or_n = input('Show apartments/houses on map (Press Enter to continue):')
		if y_or_n == '':
			map_visualize(top5)

	
	if choice == 2:
		y_or_n = input('----------Scrape apartment list (Press Enter to continue)----------')
		if y_or_n == '':
			# run scraping apartment
			scrape_house_data()
	
		y_or_n = input('\n----------Add Geocode to apartment list (Press Enter to continue)----------')
		if y_or_n == '':
			# run add_geocode()
			key = input('    Please enter your Google Map API key: ')
			add_geocode(key)
			
		y_or_n = input('\n----------Scrape route data for apartment (Press Enter to continue)----------')
		if y_or_n == '':	
			# run scrape_route()
			scrape_route()
			
		y_or_n = input('\n----------Clean crime data (Press Enter to continue)----------')
		if y_or_n == '':	
			# run crime_clean()
			crime_clean()
			
		y_or_n = input('\n----------Clean resturant data (Press Enter to continue)----------')
		if y_or_n == '':	
			# run clean_restaurant()
			clean_restaurant()
			print('restaurant data clean: done')
			
		y_or_n = input('\n----------Add score for each apartment (Press Enter to continue)----------')
		if y_or_n == '':
			# run add_score()
			add_score()
			print('add apartment score: done')

	print('1. Exploring Apartments')
	print('2. Setting')
	print('3. Exit')
	choice = eval(input('Please enter number to choose:'))


