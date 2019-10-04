import pandas as pd

def add_score():

	df_house = pd.read_csv('apartment/house.csv')
	df_restaurant = pd.read_csv('restaurant/restaurant.csv')

	df_house.reset_index(inplace=True, drop=True)
	df_house['crime_percentage'] = 0
	df_house['restaurant_num'] = 0
	df_house['restaurant_star'] = 0
	df_house['tranportation_time'] = 0

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
		else:
			print(i)

		# add crime info
		## TODO

		# add transportation info
		## TODO

	df_house.to_csv('visualization/house_score.csv', index=False)