import requests 
import ssl
import re
import pandas as pd

"""
WPScraper class
takes a website and a datastore of type CSVDataStore or SqliteDataStore.
It scrapes certain number of latest articles from the website
and store it in the specified datastore.
"""
class WPScraper:
    def __init__(self, url, datastore):
        self.url = 'http://' + url + '/wp-json/wp/v2/posts?'
        self.datastore = datastore
        
        df = self.datastore.read()
        if not isinstance(df, pd.DataFrame) or df.empty:
            self.saved_id_set = set()
            self.cutoff_date = None
            self.earliest_date = None
        else:
            self.saved_id_set = set(df['id'].tolist())
            df = df.sort_values(by=['date'], ascending=False)
            self.cutoff_date = df.iloc[0].date
            self.earliest_date = df.iloc[-1].date
            
        self.new_article_list = []
        self.author_name_lookups = {}

        
    def scrape(self, total_count, count_per_page = 10):
        if total_count <= 0:
            return
        
        parameters_new = {}
        if self.cutoff_date:
            parameters_new['after'] = self.cutoff_date
            
        self._get_latest_articles(self.url, parameters_new, total_count, count_per_page)
        
        remaining_count = total_count - len(self.new_article_list)
        df = self.datastore.read()
        remaining_count -= df.shape[0]
        
        if remaining_count > 0 and self.earliest_date:
            parameters_old = {}
            parameters_old['before'] = self.earliest_date        


            print('get older articles...')
            self._get_latest_articles(self.url, parameters_old, remaining_count, count_per_page)
        
          
    def save(self):
        if len(self.new_article_list) > 0:
            self.datastore.save(pd.DataFrame(self.new_article_list))
            self.new_article_list = []
        
    def count(self):
        df = self.datastore.read()
        return len(df)

    def _get_latest_articles(self, url, parameters, total_count, count_per_page):
        page = 1
        current_total_count = total_count
        parameters['per_page'] = min(total_count, count_per_page, 100)

        while True:
            parameters['page'] = page
            response = requests.get(self.url, params = parameters) 
            response_status = response.status_code

            if response_status != 200:
                print('Warning: requests.get {} {} status: {}'.format(self.url, parameters, response_status))
                break

            try:
                response_json = response.json() 
            except ValueError as e:
                break
            else:
                if len(response_json) == 0:
                    break
                    
                for article in response_json:
                    article_id = article['id']
                    
                    if len(self.saved_id_set) == 0 or article_id not in self.saved_id_set:
                        self.saved_id_set.add(article_id)
                        self.new_article_list.append(self._parse(article))

                    current_total_count -= 1
                    if current_total_count <= 0:
                        break
                        
            finally:
                if current_total_count <= 0:
                    break
                    
                page += 1
                

    def _clean(self, raw_html):
        if isinstance(raw_html, dict) and 'rendered' in raw_html:
            raw_html = raw_html['rendered']

        clean_r = re.compile('<.*?>')
        clean_text = re.sub(clean_r, '', raw_html)
        return clean_text

    def _get_author_name(self, article):
        author_str = article['author']
        if author_str in self.author_name_lookups:
            return self.author_name_lookups[author_str]
        
        if '_links' in article:
            if 'author' in article['_links']:
                if 'href' in article['_links']['author'][0]:
                    url = article['_links']['author'][0]['href']
                    response = requests.get(url) 
                    response_status = response.status_code
                    if response_status == 200:
                        try:
                            response_json = response.json() 
                        except ValueError as e:
                            print('response.json {} fails:\n  {}'.format(self.url, e))
                        else:
                            if 'name' in response.json():
                                author_str = response.json()['name']
                                self.author_name_lookups[article['author']] = author_str
        return author_str


    def _get_article_field(self, article, key):
        try:
            v = article[key]
        except KeyError:
            v = 'NA'
        finally:
            return v
            
    def _parse(self, article):
        article_id = article['id']
        author = self._get_article_field(article, 'author')
        author_name = self._get_author_name(article)
        date = self._get_article_field(article, 'date')
        title = self._clean(self._get_article_field(article, 'title'))
        link = self._get_article_field(article, 'link')
        content = self._clean(self._get_article_field(article, 'content'))
        
        return {
                'id': article_id,
                'author': author,
                'author_name': author_name,
                'date': date,
                'title': title,
                'link': link,
                'content': content
            }

