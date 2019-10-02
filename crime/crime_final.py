# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 00:01:34 2019

@author: tlpierce
"""

# Import pandas
import pandas as pd

#read crime values
df = pd.read_excel(r'C:/Users/trist/OneDrive/Documents/PYTHON/Final Project/Crime Data.xlsx', sheet_name='Crime-Cleaned') 

#extract total crime
zips= df.loc[df['ZipCode'] == 'All']
#print(zips)
zsums= zips.sum(axis = 0, skipna = True) 
ztotal=zsums.iloc[2]
#print(ztotal)

#extract crime numbers by location
oakland= df.loc[df['ZipCode'] == 15213]
#print(oakland)
shadyside= df.loc[df['ZipCode'] == 15232]
#print(shadyside)
sqhill= df.loc[df['ZipCode'] == 15217]
#print(sqhill)


#Bar graph of top 3 crimes in each area
o= oakland.loc[df['% of Total'] > .08]
#print(o)
#produce bar graph of data
ax_o = o.plot.bar(x='Criminal Offense', y='Number of Crimes', rot=0, title='Top Crimes in Oakland from 2018 and 2019')

ss= shadyside.loc[df['% of Total'] > .06]
#print(ss)
#produce bar graph of data
ax_ss = ss.plot.bar(x='Criminal Offense', y='Number of Crimes', rot=0, title='Top Crimes in Shadyside from 2018 and 2019')

sh= sqhill.loc[df['% of Total'] > .08]
#print(sh)
#produce bar graph of data
ax_sh = sh.plot.bar(x='Criminal Offense', y='Number of Crimes', rot=0, title='Top Crimes in Squirrel Hill from 2018 and 2019')


#get totals by location 
osums= oakland.sum(axis = 0, skipna = True) 
ototal=osums.iloc[2]
#print(ototal)

sssums= shadyside.sum(axis = 0, skipna = True) 
sstotal=sssums.iloc[2]
#print(sstotal)

shsums= sqhill.sum(axis = 0, skipna = True) 
shtotal=shsums.iloc[2]
#print(shtotal)


#make percentages by location 
oper= ototal/ztotal
#print(oper)

ssper= sstotal/ztotal 
#print(ssper)

shper= shtotal/ztotal
#print(shper)


#make summary table
data= [[15213, "{:.2%}".format(oper)], [15232, "{:.2%}".format(ssper)], [15217, "{:.2%}".format(shper)]]
df2 = pd.DataFrame(data, index= ['Oakland', 'ShadySide', 'Squirrel Hill'], columns = ['Zip Code', '% of Crime']) 
print(df2)





#import time of day
df2 = pd.read_excel(r'C:/Users/trist/OneDrive/Documents/PYTHON/Final Project/Crime Data.xlsx', sheet_name='Times-Cleaned') 
#print(df2)


#extract crime numbers by location
oakland2= df2.loc[df2['ZipCode'] == 15213]
print(oakland2)
shadyside2= df2.loc[df2['ZipCode'] == 15232]
print(shadyside2)
sqhill2= df2.loc[df2['ZipCode'] == 15217]
print(sqhill2)
