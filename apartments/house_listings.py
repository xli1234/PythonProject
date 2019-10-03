# Enter desired zip codes below
zipcodes = ['15213', '15217', '15232'] # Required zip codes (USA only)

# Initializations
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


# Some essential functions
def house_attr_list(soup, tag, css_identifier, find_children = False, child = 0, content_num = 0):
    """
    Fetches value from HTML source code with the help of provided identifier tags and css elements.
    Inputs:
        soup: BeautifulSoup object from which content is to be fetched
        tag: HTML tag to be searched in soup HTML
        css_identifier: CSS identifier to select the required tag from all the found tags
        find_children: Indicate whether to fin children or not (default = False)
        child: Which child to select from all the found children (default= 0)
        content_num: Select the element from the list of found contents (default = 0)
    """
    attr_list = []
    # Scrape data using soup() (earlier: soup.FindAll())
    attr_scraped = soup(tag, css_identifier)
    # If we finding children
    if find_children:
        for i in range(0, len(attr_scraped)):
            attr_list.append(str(attr_scraped[i].findChildren()[child].contents[content_num]))
        return attr_list
    # If not finding children
    for attr in attr_scraped:
        attr_list.append(str(attr.contents[content_num]).replace("\n", "").replace("\r", ""))
    return attr_list

def url_to_soup(url, headers = {'User-Agent': 'Mozilla/5.0'}, markup = 'lxml'):
    """
    Returns a BeautifulSoup object for the provided URL.
    Inputs:
        url: HTTP or HTTPS URL without a redirect
        headers: Pretend to be a browsing agent (default = Mozilla 5.0)
        markup: BeautifulSoup markup (default = lxml)
    """
    # Return a BS object for the URL and the agent provided
    return BeautifulSoup(urlopen(Request(url, headers = headers)).read(), markup)

# Blank Pandas DataFrame to hold house data
house_data = pd.DataFrame(columns = ['Zip', 'Street', 'Region', 'Price', 'Bedrooms', 'Bathrooms',
                                     'Floorspace', 'Pet_friendly', 'Furnished'])

# Traverse each zip code
for z in zipcodes:
    # Traverse the listing page for the zipcode on Trulia.com
    soup = url_to_soup('https://www.trulia.com/for_rent/'+str(z)+'_zip/')
    
    # Find how many pages are there in the listing
    num_pages = house_attr_list(soup, 'li', {'data-testid': 'pagination-page-link'}, True, 1)[-1]
    num_pages = int(num_pages)
    
    # Traverse each page in the listing for the zipcode
    for i in range(1, num_pages+1):
        # Show URL of the current page
        print('Traversing page: https://www.trulia.com/for_rent/'+str(z)+'_zip/'+str(i)+'_p/')
        
        # Create a BeautifulSoup object
        soup = url_to_soup('https://www.trulia.com/for_rent/'+str(z)+'_zip/'+str(i)+'_p/')
        
        # Find all the houses listed on the current page
        houses = soup('div', {'data-testid': 'home-card-rent'})
        # Print how many houses are on the current page
        print("Found " + str(len(houses)) + " houses")
        
        # Traverse each house and fetch its details
        for h in houses:
            # Blank dictionary to be updated and appended to the main DataFrame
            house_info = {}
            
            # Zip
            house_info['Zip'] = z
            # Street
            house_info['Street'] = [h('div', {'data-testid': 'property-street'})[0].contents[0]]
            # Region
            house_info['Region'] = [h('div', {'data-testid': 'property-region'})[0].contents[0]]
            # Price
            house_info['Price'] = [h('div', {'data-testid': 'property-price'})[0].contents[0].replace('/mo', '').replace('$', '').replace(',', '')]
            # Bedrooms
            try:
                house_info['Bedrooms'] = [h('div', {'data-testid': 'property-beds'})[0].contents[0].replace('bd', '')]
            except IndexError:
                house_info['Bedrooms'] = ['']
            # Bathrooms
            try:
                house_info['Bathrooms'] = [h('div', {'data-testid': 'property-baths'})[0].contents[0].replace('ba', '')]
            except IndexError:
                house_info['Bathrooms'] = ['']
            # Floorspace
            try:
                house_info['Floorspace'] = [h('div', {'data-testid': 'property-floorSpace'})[0].contents[0].replace('sqft', '').replace(',', '')]
            except IndexError:
                house_info['Floorspace'] = ['']
            # If pet friendly
            pf = h('div', {'data-testid': 'property-tags'})[0]
            if str(pf).find('PET FRIENDLY') != -1:
                house_info['Pet_friendly'] = ['Y']
            else:
                house_info['Pet_friendly'] = ['N']
            # If furnished
            fr = h('div', {'data-testid': 'property-tags'})[0]
            if str(fr).find('FURNISHED') != -1:
                house_info['Furnished'] = ['Y']
            else:
                house_info['Furnished'] = ['N']
            
            # Form a DataFrame to be appended
            house_data = house_data.append(pd.DataFrame(house_info))
    
# Export data to an Excel file in the current folder
house_data.to_excel("House_data.xlsx", index = False)
