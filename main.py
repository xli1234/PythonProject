# Project Apartment
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

from visualization.data_combine import combine_data
from visualization.calculate_score import get_top5
from visualization.map_visualization import map_visualize

def get_longest_length(series):
	longest_length = 0
	for v in list(series):
		if len(v.split(',')[0].strip()) > longest_length:
			longest_length = len(v.split(',')[0].strip())
	return longest_length

# # Example of using data from module
# print(crime.df2)
# print(imap.map_data)

print('Welcome to EZ-Apart!')
print('--------------------------------------------------------------------')
print('Option menu: ')
print('    1. Explore apartments')
print('    2. Settings')
print('    3. Exit')
choice = eval(input('Please enter your choice: '))
while choice != 3:
	
	if choice == 1:
		# get user input
		print('--------------------------------------------------------------------')
		print('Areas nearby CMU:')
		summary_house()
		print('--------------------------------------------------------------------')
		y_or_n = input('Do you want to see crime comparison on a chart? (Y/N) ')
		if y_or_n in ['Y', 'y']:	
			# run crime_stats()
			crime_stats()
		else:
			pass
		print('--------------------------------------------------------------------')
		print('    0: All three areas')
		print('    1: Oakland')
		print('    2: Squirrel Hill')
		print('    3: Shadyside')
		area_choice = eval(input('Enter areas to explore: '))
		print('--------------------------------------------------------------------')
		print('Tell us how important these factors are to you on a 1-5 scale:')
		print('    1: Not at all important')
		print('    2: Slightly important')
		print('    3: Important')
		print('    4: Fairly important')
		print('    5: Very important')
		weight_c = eval(input('Safety of the neighbourhood: ')) # weight for crime
		weight_r = eval(input('Eating options nearby: ')) # weight for restaurant
		weight_t = eval(input('Transit time to and from CMU: ')) # weight for transportation
		print('--------------------------------------------------------------------')
		print('    1: Drive')
		print('    2: Walk')
		print('    3: Bike')
		trans_choice = eval(input('Choose your preferred mode of transportation: '))
		print('--------------------------------------------------------------------')
		cols = ['Zip','Street','Region','Price','Bedrooms','Bathrooms','Floorspace','Pet_friendly','Furnished', 'overall_score']
		top5 = get_top5(weight_c, weight_r, weight_t, area_choice, trans_choice).reset_index(drop=True).replace(np.nan, '')
		length_street = get_longest_length(top5['Street'])
		length_region = get_longest_length(top5['Region'])
		print('Here\'s our top 5 recommendation for you:')
		print('Zip'.rjust(7),'Street'.rjust(length_street+1),'Region'.rjust(length_region+4),'Price'.rjust(8),
				'Beds'.rjust(8),'Baths'.rjust(5),'Size'.rjust(7),
				'Pet friendly'.rjust(13),'Furnished'.rjust(10), 'Smart score'.rjust(12))
		for i in range(5):
			print(str(top5[cols].iloc[i, 0]).rjust(7)
				, str(top5[cols].iloc[i, 1]).rjust(length_street+1)
				, str(top5[cols].iloc[i, 2]).split(',')[0].rjust(length_region+4)
				, str(top5[cols].iloc[i, 3]).rjust(8)
				, str(top5[cols].iloc[i, 4]).rjust(5)
				, str(top5[cols].iloc[i, 5]).rjust(8)
				, str(top5[cols].iloc[i, 6]).rjust(7)
				, str(top5[cols].iloc[i, 7]).rjust(13)
				, str(top5[cols].iloc[i, 8]).rjust(10)
				, '{:0.2f}'.format(float(top5.iloc[i, 9])).rjust(12))
		# print(top5[['Zip', 'Street','Region','Price','Bedrooms','Bathrooms','Floorspace','Pet_friendly','Furnished']])
		
		# call map_visualize()
		y_or_n = input('Do you want to see apartments/houses on map (Y/N) ')
		if y_or_n in ['Y', 'y']:
			map_visualize(top5)
		else:
			pass

	
	if choice == 2:
		print('--------------------------------------------------------------------')
		y_or_n = input('Do you want to scrape apartment list? (Y/N) ')
		if y_or_n in ['Y', 'y']:
			# run scraping apartment
			scrape_house_data()
	
		print('--------------------------------------------------------------------')
		y_or_n = input('\nDo you want to add Geocode to apartment list? (Y/N) ')
		if y_or_n in ['Y', 'y']:
			# run add_geocode()
			key = input('    Please enter your Google Map API key: ')
			add_geocode(key)
			
		print('--------------------------------------------------------------------')
		y_or_n = input('\nDo you want to scrape route data for apartment? (Y/N) ')
		if y_or_n in ['Y', 'y']:	
			# run scrape_route()
			scrape_route()
			
		print('--------------------------------------------------------------------')
		y_or_n = input('\nDo you want to update crime data? (Y/N) ')
		if y_or_n in ['Y', 'y']:	
			# run crime_clean()
			crime_clean()
			
		print('--------------------------------------------------------------------')
		y_or_n = input('\nDo you want to update resturant data? (Y/N) ')
		if y_or_n in ['Y', 'y']:	
			# run clean_restaurant()
			clean_restaurant()
			
		print('--------------------------------------------------------------------')
		y_or_n = input('\nAdd score for each apartment. (Press Enter to continue) ')
		if y_or_n == '':
			# run add_score()
			add_score()
			

	print('--------------------------------------------------------------------')
	print('Option menu: ')
	print('    1. Explore apartments')
	print('    2. Settings')
	print('    3. Exit')
	choice = eval(input('Please enter your choice: '))
