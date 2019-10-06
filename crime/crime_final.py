# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 00:01:34 2019

@author: tlpierce
"""

# Import 
import pandas as pd
# import matplotlib as mpl
# mpl.style.use('ggplot')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from pathlib import Path

# settings
filename = str(Path(__file__).parent.absolute())+'/crime.csv'
def iprint(*args):
    if __name__ == '__main__':
        for arg in args:
            print(arg, end=' ')
        print('')


def crime_clean(*args): 
    #upload and combine csv files
    df = pd.concat(map(pd.read_csv, ['crime/15213.csv', 'crime/15232.csv','crime/15217.csv', 'crime/Pgh.csv']))

    #format
    df.columns = ['Criminal Offense', 'Type', 'ZipCode','% of Total','Number of Crimes']
    df.astype({'% of Total': 'float'})
    #print(df).

    #clean data saved to new csv
    df.to_csv(r'crime/crime_clean.csv', index=None)

    print('Crime data updated.')



def crime_stats(*args):
    df = pd.concat(map(pd.read_csv, ['crime/15213.csv', 'crime/15232.csv','crime/15217.csv', 'crime/Pgh.csv']))

    #format
    df.columns = ['Criminal Offense', 'Type', 'ZipCode','% of Total','Number of Crimes']
    df.astype({'% of Total': 'float'})
    
    #extract total crime
    zips= df.loc[df['ZipCode'] == 'Pgh']
    #print(zips)
    zsums= zips.sum(axis = 0, skipna = True)
    ztotal=zsums.iloc[4]

    #extract crime numbers by location
    oakland= df.loc[df['ZipCode'] == 15213]
    shadyside= df.loc[df['ZipCode'] == 15232]
    sqhill= df.loc[df['ZipCode'] == 15217]

    #Bar graph of top 3 crimes in each area
    o= oakland.loc[oakland['% of Total'] >= .08]
    #print(o)
    
    fig = plt.figure(figsize=(20, 6))
    ax_o = fig.add_subplot(1, 3, 1) # add subplot 1 (1 row, 2 columns, first plot)
    ax_ss = fig.add_subplot(1, 3, 2) # add subplot 2 (1 row, 2 columns, second plot)
    ax_sh = fig.add_subplot(1, 3, 3) # add subplot 2 (1 row, 2 columns, second plot)

    #produce bar graph of oakland
    o.plot.bar(x='Criminal Offense', y='Number of Crimes', rot=0, title='Oakland', ax=ax_o)
    # plt.show()
    
    ss= shadyside.loc[shadyside['% of Total'] >= .09]
    #print(ss)

    #produce bar graph of shadyside
    ss.plot.bar(x='Criminal Offense', y='Number of Crimes', rot=0, title='Shadyside', ax=ax_ss)
    # plt.show()

    sh= sqhill.loc[sqhill['% of Total'] > .08]
    #print(sh)

    #produce bar graph of squirrel hill
    sh.plot.bar(x='Criminal Offense', y='Number of Crimes', rot=0, title='Squirrel Hill', ax=ax_sh)
    plt.show()


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
    data= [[15213, "{:f}".format(oper)], [15232, "{:f}".format(ssper)], [15217, "{:f}".format(shper)]]
    df2 = pd.DataFrame(data, index= ['Oakland', 'ShadySide', 'Squirrel Hill'], columns = ['Zip', 'percentage_crime']) 
    # print(df2)

    df2.to_csv(r'crime/crime_output.csv', index=False)
