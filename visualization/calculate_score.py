import pandas as pd
import math

def get_top5(weight_c=5, weight_r=5, weight_t=5, area_choice=0, trans_choice=2):
	# print(weight_c, weight_r, weight_t, area_choice, trans_choice)
	df = pd.read_csv('visualization/house_combine.csv')
	w_c = weight_c / (weight_c+weight_r+weight_t)
	w_r = weight_r / (weight_c+weight_r+weight_t)
	w_t = weight_t / (weight_c+weight_r+weight_t)

	# normalize data for later score calculation
	df['n_restaurant_num'] = df['restaurant_num'].apply(lambda x: math.log(x+1)) # use natural log to smooth data first
	df['n_restaurant_num'] = normalize(df['restaurant_num'])
	df['n_restaurant_star'] = normalize(df['restaurant_star'])
	df['n_trans_time_driv'] = df['trans_time_driv'].apply(lambda x: math.log(x+1)) # use natural log to smooth data first
	df['n_trans_time_driv'] = normalize(df['n_trans_time_driv'])
	df['n_trans_time_walk'] = df['trans_time_walk'].apply(lambda x: math.log(x+1)) # use natural log to smooth data first
	df['n_trans_time_walk'] = normalize(df['n_trans_time_walk'])
	df['n_trans_time_bike'] = df['trans_time_bike'].apply(lambda x: math.log(x+1)) # use natural log to smooth data first
	df['n_trans_time_bike'] = normalize(df['n_trans_time_bike'])

	
	# if user wants all three areas, use all houses
	if area_choice == 0:
		df = df
	# if user wants one area, use only houses in that area
	elif area_choice == 1:
		df = df[df.Zip == 15213]
	elif area_choice == 2:
		df = df[df.Zip == 15217]
	elif area_choice == 3:
		df = df[df.Zip == 15232]

	df.reset_index(inplace=True, drop=True)
	trans_choices = {1: 'n_trans_time_driv', 2: 'n_trans_time_walk', 3: 'n_trans_time_bike'}
	# calculate over all score
	df['overall_score'] = w_c * 8*(1-10*df.crime_percentage) + w_r * (df.n_restaurant_num + df.n_restaurant_star)/2 + w_t * (1-df[trans_choices[trans_choice]])

	df.sort_values('overall_score', ascending=False, inplace=True)

	return df[['Zip','Street','Region','Price','Bedrooms','Bathrooms','Floorspace','Pet_friendly','Furnished','lat','lng','crime_percentage','restaurant_num','restaurant_star','trans_time_driv','trans_time_walk','trans_time_bike', 'overall_score']].head()

# use z-score to normalize data
def normalize(df_col):
	return (df_col - df_col.mean()) / df_col.std()
