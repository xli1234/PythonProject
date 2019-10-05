import pandas as pd

def summary_house():
	df = pd.read_csv('apartment/house_cache.csv')
	zip_area = {15213: 'Oakland', 15217: 'Squirrel Hill', 15232: 'Shadyside'}
	house_count = list(df[['Zip', 'Street']].groupby('Zip').count().values.reshape(3))
	house_area = list(df[['Zip', 'Street']].groupby('Zip').count().index)
	print('All three areas'.rjust(20), str(sum(house_count)).rjust(5), 'houses/apartments')
	for i in range(len(house_area)):
		print(zip_area[house_area[i]].rjust(20), str(house_count[i]).rjust(5), 'houses/apartments')