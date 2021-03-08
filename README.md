# WPScraper pckage

This is a python package that collects and stores the most recent articles from a WordPress website.

It currently supports CSV and Sqlite data stores.

# Files
README.md   
setup.py   
wpscraper/wpscraper.py  
wpscraper/datastores.py   
tests/test_wpscraper.py  

# Installation
Step 1&2 are optional but recommended  
1. python3 -m venv test-wpscraper   
2. source test-wpscraper/bin/activate   
3. pip install .  

# Usage
1. Instantiate a CSV datastore or a sqlite datastore   
2. Instantiate a WPScraper with a url and the datastore  
3. Call scrape with number of articles n   
4. Call save to put the result in the datastore. 

# Example using CSVDataStore
```
from wpscraper import WPScraper, CSVDataStore  
ds = CSVDataStore('result.csv')  
scraper = WPScraper('techcrunch.com', ds)   
scraper.scrape(100)  
scraper.save()  
```

# Example using SqliteDataStore
```
from wpscraper import WPScraper, SqliteDataStore  
ds = SqliteDataStore('techcrunch.db', 'techcrunch')  
scraper = WPScraper('techcrunch.com', ds)  
scraper.scrape(100)  
scraper.save()  
```

# To run unittest
```
python -m unittest test_wpscraper  
```

