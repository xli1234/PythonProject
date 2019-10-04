import pandas as pd
import requests

def add_geocode():
	df = pd.read_csv('apartment/house_cache.csv')
	df['lat'] = ''
	df['lng'] = ''
	df.reset_index(inplace=True, drop=True)
	for i in range(df.shape[0]):
		data = dict(df.loc[i])
		address = data['Street'].split('#')[0].split('-')[0].strip() + ' Pittsburgh, PA ' + str(data['Zip'])
		if data['Street'] == 'Address Not Disclosed': # ignore house without address
			# print(i)
			continue
		lat, lng = get_geocode(address)
		df.loc[i, 'lat'] = lat
		df.loc[i, 'lng'] = lng

	# only save those with specific address
	df[~(df.lat == '')].to_csv('apartment/house.csv', index=False)


# using google geocode api to get geocode of an house/apartment
def get_geocode(address):
    key = 'your_key'
    address = address.replace(' ','+')
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address, key)
    r = requests.get(url)
    results = r.json()['results']
    location = results[0]['geometry']['location']
    return (location['lat'], location['lng'])
