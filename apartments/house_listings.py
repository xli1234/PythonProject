import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

zipcode = '15217'

/* def house_attr_list(soup, tag, css_identifier, find_children = False, child = 0, content_num = 0):
    attr_list = []
    attr_scraped = soup(tag, css_identifier)
    if find_children:
        for i in range(0, len(attr_scraped)):
            attr_list.append(str(attr_scraped[i].findChildren()[child].contents[content_num]))
            # attr_scraped = attr_scraped[instance].findChildren()[child]
        return attr_list
    for attr in attr_scraped:
        attr_list.append(str(attr.contents[content_num]).replace("\n", "").replace("\r", ""))
    return attr_list */

def url_to_soup(url, headers = {'User-Agent': 'Mozilla/5.0'}, markup = 'lxml'):
    return BeautifulSoup(urlopen(Request(url, headers = headers)).read(), markup)

def lpad(list0, n, fillvalue=''):
        return list0 + [fillvalue] * (n - len(list0))
    
#soup = url_to_soup('https://www.apartments.com/pittsburgh-pa-15213/')
soup = url_to_soup('https://www.trulia.com/for_rent/'+str(zipcode)+'_zip/')

num_pages = house_attr_list(soup, 'li', {'data-testid': 'pagination-page-link'}, True, 2)[-1]
num_pages = int(num_pages)



house_data = pd.DataFrame(columns = ['Street',
                                     'Region',
                                     'Price',
                                     'Bedrooms',
                                     'Bathrooms',
                                     'Floorspace',
                                     'Pet_friendly',
                                     'Furnished'])
    
for i in range(1, num_pages+1):
    print('Traversing page: https://www.trulia.com/for_rent/'+str(zipcode)+'_zip/'+str(i)+'_p/')
    soup = url_to_soup('https://www.trulia.com/for_rent/'+str(zipcode)+'_zip/'+str(i)+'_p/')
    houses = soup('div', {'data-testid': 'home-card-rent'})
    num_houses = len(houses)
    for h in houses:
        house_info = {}
        
        house_info['Street'] = [h('div', {'data-testid': 'property-street'})[0].contents[0]]
        house_info['Region'] = [h('div', {'data-testid': 'property-region'})[0].contents[0]]
        house_info['Price'] = [h('div', {'data-testid': 'property-price'})[0].contents[0].replace('/mo', '').replace('$', '').replace(',', '')]
        
        try:
            house_info['Bedrooms'] = [h('div', {'data-testid': 'property-beds'})[0].contents[0].replace('bd', '')]
        except IndexError:
            house_info['Bedrooms'] = ['']
        
        try:
            house_info['Bathrooms'] = [h('div', {'data-testid': 'property-baths'})[0].contents[0].replace('ba', '')]
        except IndexError:
            house_info['Bathrooms'] = ['']
        
        try:
            house_info['Floorspace'] = [h('div', {'data-testid': 'property-floorSpace'})[0].contents[0].replace('sqft', '').replace(',', '')]
        except IndexError:
            house_info['Floorspace'] = ['']
        
        pf = h('div', {'data-testid': 'property-tags'})[0]
        if str(pf).find('PET FRIENDLY') != -1:
            house_info['Pet_friendly'] = ['Y']
        else:
            house_info['Pet_friendly'] = ['N']
            
        fr = h('div', {'data-testid': 'property-tags'})[0]
        if str(fr).find('FURNISHED') != -1:
            house_info['Furnished'] = ['Y']
        else:
            house_info['Furnished'] = ['N']
            
        house_data = house_data.append(pd.DataFrame(house_info))

house_data = house_data.reset_index()


house_data.to_excel("House_data.xlsx", index = False)
