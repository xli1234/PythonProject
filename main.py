# Project Apartment

# add all directory paths
import sys
from pathlib import Path
crime_path = str(Path(__file__).parent.absolute()) + '/crime'
imap_path = str(Path(__file__).parent.absolute()) + '/imap'
sys.path.insert(1, crime_path)
sys.path.insert(1, imap_path)

# import individual modules
import crime_final
import imap

# Example of using data from module
print(crime_final.df2)
print(imap.map_cache)
