import pandas as pd
from math import log

def add_score():

	df_house = pd.read_csv('apartment/house_geocode.csv')
	df_restaurant = pd.read_csv('restaurant/restaurant.csv')
	df_transportation = pd.read_csv('imap/map_cache.csv')
	df_transportation.replace('FAST', 60, inplace=True) # if the distance is too close, use 60s (1min) as the time
	df_transportation.DRIV_TIME = df_transportation.DRIV_TIME.astype('int') # convert data type to int
	df_transportation.WALK_TIME = df_transportation.WALK_TIME.astype('int') # convert data type to int
	df_transportation.BIKE_TIME = df_transportation.BIKE_TIME.astype('int') # convert data type to int

	df_house.reset_index(inplace=True, drop=True)
	df_house['crime_percentage'] = 0
	df_house['restaurant_num'] = 0
	df_house['restaurant_star'] = 0
	df_house['trans_time_driv'] = 0
	df_house['trans_time_walk'] = 0
	df_house['trans_time_bike'] = 0

	for i in range(df_house.shape[0]):
		apt_lat = dict(df_house.loc[i])['lat']
		apt_lng = dict(df_house.loc[i])['lng']
		
		# count number of restaurants around the house, and calculate the average star of them
		restaurant_num = 0
		star_sum = 0
		for lat, lng, star in zip(df_restaurant.latitude, df_restaurant.longitude, df_restaurant.stars):
			if abs(lat - apt_lat) < 0.005 and abs(lng - apt_lng) < 0.0025:
				restaurant_num += 1
				star_sum += star
		if restaurant_num != 0:
			df_house.loc[i, 'restaurant_num'] = restaurant_num
			df_house.loc[i, 'restaurant_star'] = star_sum/restaurant_num
		# else:
		# 	print(i)

		# add crime info
		## TODO

		# add transportation info
		# print('----', df_house.loc[i, 'Street'])
		try:
			data_trans = df_transportation[df_transportation.APT == df_house.loc[i, 'Street']][['DRIV_TIME', 'WALK_TIME', 'BIKE_TIME']] # find transportation info for current apartment
			# print(data_trans)
			data_trans.values[0][0]
			df_house.loc[i, 'trans_time_driv'] = round(int(data_trans.values[0][0])/60 * 2) / 2
			df_house.loc[i, 'trans_time_walk'] = round(int(data_trans.values[0][1])/60 * 2) / 2
			df_house.loc[i, 'trans_time_bike'] = round(int(data_trans.values[0][2])/60 * 2) / 2
		except:
			pass

	# normalize data for later score calculation
	df_house['crime_percentage'] = normalize(df_house['crime_percentage'])
	df_house['restaurant_num'] = df_house['restaurant_num'].apply(lambda x: log(x+1)) # use natural log to smooth data
	df_house['restaurant_num'] = normalize(df_house['restaurant_num'])
	df_house['restaurant_star'] = normalize(df_house['restaurant_star'])
	df_house['trans_time_driv'] = normalize(df_house['trans_time_driv'])
	df_house['trans_time_walk'] = normalize(df_house['trans_time_walk'])
	df_house['trans_time_bike'] = normalize(df_house['trans_time_bike'])

	# save data to csv
	df_house.to_csv('visualization/house_score.csv', index=False)

# use (v-min)/(max-min) to normalize data
def normalize(df_col):
	return (df_col-df_col.min()) / (df_col.max()-df_col.min())
