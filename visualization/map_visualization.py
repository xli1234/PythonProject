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


PORT = 1000 + int(random.random()*9000) # randomly generate a port number
HOST = '127.0.0.1'
SERVER_ADDRESS = '{host}:{port}'.format(host=HOST, port=PORT)
FULL_SERVER_ADDRESS = 'http://' + SERVER_ADDRESS


def map_visualize(apt_name='Royal York', apt_lat=40.453150, apt_lng=-79.953920, crime=0.398, distance=1385, time=[366, 1006, 371]):
	# location data for CMU (Pittsburgh)
	cmu_name = 'CMU'
	cmu_lat = 40.444229
	cmu_lng = -79.943367
	distance_km = distance/1000
	time_drive = time[0]/60
	time_walk = time[1]/60
	time_bike = time[2]/60
	
	# load restaurant data
	df_restaurant = pd.read_csv('restaurant/restaurant.csv')
	print(df_restaurant.head())
	
	
	# # get (latitude, longitude) from physical address
	# def get_lat_lng(addr):
	#     geolocator = Nominatim(user_agent="my-application")
	#     try:
	#         location = geolocator.geocode(addr)
	#         lat = location.latitude
	#         lng = location.longitude
	#     except:
	#         lat = 0
	#         lng = 0
	#     # print(lat, lng)   return (lat, lng)
	
	
	# create map
	cmu_map = folium.Map(location=[cmu_lat, cmu_lng], zoom_start=14)
	
	
	# add pop-up text to the apartment on the map
	folium.Marker([apt_lat, apt_lng], popup=apt_name).add_to(cmu_map)
	folium.Marker([cmu_lat, cmu_lng], popup=cmu_name, color='yellow').add_to(cmu_map)
	
	# instantiate a feattaure group for the restaurants in the dataframe
	incidents = folium.map.FeatureGroup()
	
	# add each to the resurant feature group
	for lat, lng, in zip(df_restaurant.latitude, df_restaurant.longitude):
	    if abs(lat - apt_lat) < 0.005 and abs(lng - apt_lng) < 0.0025:
	        incidents.add_child(
	            folium.CircleMarker(
	                [lat, lng],
	                radius=5, # define how big you want the circle markers to be
	                color='yellow',
	                fill=True,
	                fill_color='blue',
	                fill_opacity=0.6
	            )
	        ) 
	        
	# add restaurants to map
	cmu_map.add_child(incidents)
	
	# add legend of transportation&crime data to map
	legend_html =   '''
	                <div style="position: fixed; 
	                            bottom: 50px; right: 50px; width: 310px; height:170px; 
	                            border:2px solid grey; z-index:9999; font-size:13px;
	                            backgroud:white
	                            ">&nbsp; <br>
	                              &nbsp;<font size="3" face="Verdana">{:0.1f} km to CMU</font> <br>
	                              &nbsp;&nbsp;&nbsp; <i class="fa fa-map-marker fa-2x" style="color:green"></i>Drive: {:0.2f}min &nbsp; <br>
	                              &nbsp;&nbsp;&nbsp; <i class="fa fa-map-marker fa-2x" style="color:red"></i>Walk: {:0.2f}min &nbsp; <br>
	                              &nbsp;&nbsp;&nbsp; <i class="fa fa-map-marker fa-2x" style="color:blue"></i>Bike: {:0.2f}min &nbsp; <br><br>
	                              &nbsp; <font size="3" face="Verdana">{:.2%} of the Crime was in this area </font>&nbsp; <br>
	                </div>
	                '''.format(distance_km, time_drive, time_walk, time_bike, crime)
	
	cmu_map.get_root().html.add_child(folium.Element(legend_html))

	# save the visualization into the temp file and render it
	tmp = NamedTemporaryFile()
	cmu_map.save(tmp.name)
	with open(tmp.name) as f:
	    folium_map_html = f.read()
	
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
    subprocess.call(['fuser', '-k', '{0}/tcp'.format(PORT)])

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
