import unittest
import random
import math

from wpscraper import WPScraper, CSVDataStore, SqliteDataStore

class WPScraperTestBase(unittest.TestCase):
    def _get_articles(self, n, max_count=None):
        if n == 1:
            print('scrape latest {} article...'.format(n))
        else:
            print('scrape latest {} articles...'.format(n))

        self.scraper.scrape(n)
        self.scraper.save()
        if max_count:
            self.assertEqual(self.scraper.count(), max(max_count,n))
        else:
            self.assertEqual(self.scraper.count(), n)


    def _scrape_times(self, n, given_count=None):
        for i in range(n):
            if not given_count:
                count = math.ceil(random.random()*10)
            else:
                count = given_count
            
            if not self.max_count:
                self.max_count = count
            else:
                self.max_count = max(self.max_count, count)
                
            self._get_articles(count,self.max_count)
        return self.max_count

        
"""
WPScraperTestCSV
"""
class WPScraperTestCSV(WPScraperTestBase):
    def setUp(self):
        self.csv = CSVDataStore('mr.csv')
        self.scraper = WPScraper('rollingstone.com', self.csv)
        self.max_count = 0

    def test_scrape_1_times_100(self):
        count = self._scrape_times(1, 100)
        self.assertEqual(self.scraper.count(), count)

    def test_scrape_3_times_random(self):
        count = self._scrape_times(3)
        self.assertEqual(self.scraper.count(), count)

    def tearDown(self):
        self.csv.clean()

"""
WPScraperTestDB
"""
class WPScraperTestDB(WPScraperTestBase):
    def setUp(self):
        self.db = SqliteDataStore('techcrunch.db', 'techcrunch')
        self.scraper = WPScraper('techcrunch.com', self.db)
        self.max_count = 0
        
    def test_scrape_1_times_100(self):
        count = self._scrape_times(1, 100)
        self.assertEqual(self.scraper.count(), count)

    def test_scrape_3_times_random(self):
        count = self._scrape_times(3)
        self.assertEqual(self.scraper.count(), count)

    def tearDown(self):
        self.db.clean()


