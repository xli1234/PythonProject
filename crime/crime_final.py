# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 00:01:34 2019

@author: tlpierce
"""

# Import 
import pandas as pd
import matplotlib as mpl

mpl.style.use('ggplot')


from pathlib import Path

# settings
filename = str(Path(__file__).parent.absolute())+'/crime.csv'
def iprint(*args):
    if __name__ == '__main__':
        for arg in args:
            print(arg, end=' ')
        print('')


#upload and combine csv files
df = pd.concat(map(pd.read_csv, ['15213.csv', '15232.csv','15217.csv', 'Pgh.csv']))

#format
df.columns = ['Criminal Offense', 'Type', 'ZipCode','% of Total','Number of Crimes']
df.astype({'% of Total': 'float'})
#print(df).


#save to new csv
df.to_csv(r'crime.csv', index=None)


#extract total crime
zips= df.loc[df['ZipCode'] == 'Pgh']
#print(zips)
zsums= zips.sum(axis = 0, skipna = True)
ztotal=zsums.iloc[4]


#extract crime numbers by location
oakland= df.loc[df['ZipCode'] == 15213]
#print(oakland)
shadyside= df.loc[df['ZipCode'] == 15232]
#print(shadyside)
sqhill= df.loc[df['ZipCode'] == 15217]
#print(sqhill)



#Bar graph of top 3 crimes in each area
o= oakland.loc[oakland['% of Total'] >= .08]
#print(o)

#produce bar graph of oakland
ax_o = o.plot.bar(x='Criminal Offense', y='Number of Crimes', rot=0, title='Top Crimes in Oakland from 2018 and 2019')

ss= shadyside.loc[shadyside['% of Total'] >= .09]
#print(ss)

#produce bar graph of shadyside
ax_ss = ss.plot.bar(x='Criminal Offense', y='Number of Crimes', rot=0, title='Top Crimes in Shadyside from 2018 and 2019')

sh= sqhill.loc[sqhill['% of Total'] > .08]
#print(sh)

#produce bar graph of squirrel hill
ax_sh = sh.plot.bar(x='Criminal Offense', y='Number of Crimes', rot=0, title='Top Crimes in Squirrel Hill from 2018 and 2019')



#get totals by location 
osums= oakland.sum(axis = 0, skipna = True) 
ototal=osums.iloc[4]

sssums= shadyside.sum(axis = 0, skipna = True) 
sstotal=sssums.iloc[4]

shsums= sqhill.sum(axis = 0, skipna = True) 
shtotal=shsums.iloc[4]


#make percentages by location 
oper= ototal/ztotal
ssper= sstotal/ztotal 
shper= shtotal/ztotal


#make summary table
data= [[15213, "{:.2%}".format(oper)], [15232, "{:.2%}".format(ssper)], [15217, "{:.2%}".format(shper)]]
df2 = pd.DataFrame(data, index= ['Oakland', 'ShadySide', 'Squirrel Hill'], columns = ['Zip Code', '% of Crime']) 
print(df2)
