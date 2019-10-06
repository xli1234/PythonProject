#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import random
import folium
import subprocess
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from tempfile import NamedTemporaryFile
import os

# use a temporary-HTML renderer to display
PORT = 1000 + int(random.random()*9000) # randomly generate a port number
HOST = '127.0.0.1'
SERVER_ADDRESS = '{host}:{port}'.format(host=HOST, port=PORT)
FULL_SERVER_ADDRESS = 'http://' + SERVER_ADDRESS


def map_visualize(df_house):
	# location data for CMU (Pittsburgh)
	cmu_name = 'CMU'
	cmu_lat = 40.444229
	cmu_lng = -79.943367

	
	# load restaurant data
	df_restaurant = pd.read_csv('restaurant/restaurant.csv')
	# print(df_restaurant.head())
	
	
	# Zip,
	# Street,
	# Region,
	# Price,
	# Bedrooms,
	# Bathrooms,
	# Floorspace,
	# Pet_friendly,
	# Furnished,
	# lat,
	# lng,
	# crime_percentage,
	# restaurant_num,
	# restaurant_star,
	# trans_time_driv,
	# trans_time_walk,
	# trans_time_bike

	
	# create map
	cmu_map = folium.Map(location=[cmu_lat, cmu_lng], zoom_start=14)
	
	
	folium.Marker([cmu_lat, cmu_lng], popup=cmu_name, color='red').add_to(cmu_map)
	for i in range(df_house.shape[0]):
		# add pop-up text to the apartment on the map
		Name = df_house.loc[i, 'Street']
		Region = df_house.loc[i, 'Region']
		Price = df_house.loc[i, 'Price']
		Bedrooms = df_house.loc[i, 'Bedrooms']
		Bathrooms = df_house.loc[i, 'Bathrooms']
		Floorspace = df_house.loc[i, 'Floorspace']
		Pet_friendly = df_house.loc[i, 'Pet_friendly']
		Furnished = df_house.loc[i, 'Furnished']
		trans_time_driv = df_house.loc[i, 'trans_time_driv']
		trans_time_walk = df_house.loc[i, 'trans_time_walk']
		trans_time_bike = df_house.loc[i, 'trans_time_bike']
		apt_lat = df_house.loc[i, 'lat']
		apt_lng = df_house.loc[i, 'lng']
		info = """{}, {}\nPrice: {}\nBedrooms: {}\nBathrooms: {}\nFloorspace: {}\nPet friendly: {}\nFurnished: {}\nNumber of restaurants: {}\nAverage star of restaurants: {:.2f}\n
				""".format(df_house.loc[i,'Street'],
						   df_house.loc[i,'Region'],
						   df_house.loc[i,'Price'],
						   df_house.loc[i,'Bedrooms'],
						   df_house.loc[i,'Bathrooms'],
						   df_house.loc[i,'Floorspace'],
						   df_house.loc[i,'Pet_friendly'],
						   df_house.loc[i,'Furnished'],
						   df_house.loc[i,'restaurant_num'],
						   df_house.loc[i,'restaurant_star'])
		folium.Marker([apt_lat, apt_lng], popup=info).add_to(cmu_map)
	
		# instantiate a feattaure group for the restaurants in the dataframe
		incidents = folium.map.FeatureGroup()
		
		# add each to the resurant feature group
		for lat, lng, in zip(df_restaurant.latitude, df_restaurant.longitude):
		    if abs(lat - apt_lat) < 0.005 and abs(lng - apt_lng) < 0.0025:
		        incidents.add_child(
		            folium.CircleMarker(
		                [lat, lng],
		                radius=5, # define how big the circle markers to be
		                color='yellow',
		                fill=True,
		                fill_color='blue',
		                fill_opacity=0.6
		            )
		        ) 
		        
		# add restaurants to map
		cmu_map.add_child(incidents)
	
	# # add legend of transportation&crime data to map
	# legend_html =   '''
	#                 <div style="position: fixed; 
	#                             bottom: 50px; right: 50px; width: 310px; height:170px; 
	#                             border:2px solid grey; z-index:9999; font-size:13px;
	#                             backgroud:white
	#                             ">&nbsp; <br>
	#                               &nbsp;<font size="3" face="Verdana">{:0.1f} km to CMU</font> <br>
	#                               &nbsp;&nbsp;&nbsp; <i class="fa fa-map-marker fa-2x" style="color:green"></i>Drive: {:0.2f}min &nbsp; <br>
	#                               &nbsp;&nbsp;&nbsp; <i class="fa fa-map-marker fa-2x" style="color:red"></i>Walk: {:0.2f}min &nbsp; <br>
	#                               &nbsp;&nbsp;&nbsp; <i class="fa fa-map-marker fa-2x" style="color:blue"></i>Bike: {:0.2f}min &nbsp; <br><br>
	#                               &nbsp; <font size="3" face="Verdana">{:.2%} of the Crime was in this area </font>&nbsp; <br>
	#                 </div>
	#                 '''.format(distance_km, time_drive, time_walk, time_bike, crime)
	
	# cmu_map.get_root().html.add_child(folium.Element(legend_html))

	# save the visualization into the temp file and render it
	tmp = NamedTemporaryFile(mode='w', delete=False)
	cmu_map.save(tmp.name)
	tmp.close()
	with open(tmp.name) as f:
	    folium_map_html = f.read()
	
	os.unlink(tmp.name) # delete the tmp file, so no garbage remained after the program ends
	run_html_server(folium_map_html)





# ------------------------------------------------------------------------------------------------
# use a temporary-HTML renderer to display 
# pretty much copy-paste of this answer: https://stackoverflow.com/a/38945907/3494126

def TemproraryHttpServer(page_content_type, raw_data):
    """
    A simpe, temprorary http web server on the pure Python 3.
    It has features for processing pages with a XML or HTML content.
    """

    class HTTPServerRequestHandler(BaseHTTPRequestHandler):
        """
        An handler of request for the server, hosting XML-pages.
        """

        def do_GET(self):
            """Handle GET requests"""

            # response from page
            self.send_response(200)

            # set up headers for pages
            content_type = 'text/{0}'.format(page_content_type)
            self.send_header('Content-type', content_type)
            self.end_headers()

            # writing data on a page
            self.wfile.write(bytes(raw_data, encoding='utf'))

            return

    if page_content_type not in ['html', 'xml']:
        raise ValueError('This server can serve only HTML or XML pages.')

    page_content_type = page_content_type

    # kill a process, hosted on a localhost:PORT
    subprocess.call(['fuser', '-k', '{0}/tcp'.format(PORT)], shell=True)

    # Started creating a temprorary http server.
    httpd = HTTPServer((HOST, PORT), HTTPServerRequestHandler)

    # run a temprorary http server
    httpd.serve_forever()


def run_html_server(html_data=None):

    if html_data is None:
        html_data = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>Page Title</title>
        </head>
        <body>
        <h1>This is a Heading</h1>
        <p>This is a paragraph.</p>
        </body>
        </html>
        """

    # open in a browser URL and see a result
    webbrowser.open(FULL_SERVER_ADDRESS)

    # run server
    TemproraryHttpServer('html', html_data)
