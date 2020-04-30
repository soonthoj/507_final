##################################
##### Name: Joe Soonthornsawad
##### Uniqname: joesoon
##################################

'''
use a single cache, and use 'construct_unique_key( )' only for web API requests 
since web scraping request URLs are already unique
'''
from requests_oauthlib import OAuth1
from bs4 import BeautifulSoup
import requests
import json
import secrets # file that contains API authorizations
from newsapi import NewsApiClient
import sqlite3

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("finalproj.db")
cur = conn.cursor()

client_key = secrets.TWITTER_API_KEY
client_secret = secrets.TWITTER_API_SECRET_KEY
access_token = secrets.TWITTER_ACCESS_TOKEN
access_token_secret = secrets.TWITTER_ACCESS_TOKEN_SECRET

yelp_api_key = secrets.YELP_API_KEY
yelp_client_key = secrets.YELP_CLIENT_KEY

newsapi = NewsApiClient(api_key=secrets.NEWS_API_KEY)

CACHE_FILENAME = "top_info_cache.json"
CACHE_DICT = {}

# pass object along with requests.get() request and parameters
oauth = OAuth1(client_key,
            client_secret=client_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret)


# dictionary of yahoo woeids for 10 major cities in america. Will need to use this for twitter api query
# woeid api is no longer supported by yahoo, so manual look up plus adding to dictionary is fastest way to build this in.
woeid_dictionary = {'new york': 2459115, 'los angeles': 2442047, 'chicago': 2379574, 'houston': 2424767, 'phoenix': 2471390,
                    'philadelphia': 2471217, 'san antonio': 2487796, 'san diego': 2487889, 'dallas': 2388929, 'san jose': 2488042,
                    'austin': 2357536, 'jacksonville': 2428344, 'fort worth': 2406080, 'columbus': 2383660, 'san francisco': 2487956,
                    'charlotte': 2378426, 'indianapolis': 2427032, 'seattle': 2490383, 'denver': 2391279, 'washington dc': 2514815,
                    'boston': 2367105, 'el paso': 2397816, 'detroit': 2391585, 'nashville': 2457170, 'portland': 2475687}


def get_stories(city_name, number=10):
        """Return the top 10 trending topics for a specific WOEID, if trending
        information is available for it.

        Args:
          city_name:
            (str) name of city to look up
          number:
            number of articles to include

        Returns:
          None
        """
        # /v2/top-headlines
        articles = newsapi.get_everything(q=city_name, language='en')
       
        # check to see how many articles were returned. Alte
        if number > articles['totalResults'] and articles['totalResults'] > 0:
          number = articles['totalResults']
        
        articles = articles['articles']

        print('')
        print(f'{number} Top headlines about {city}')
        print("-------------------------------------------")

        for i in range(number):
            print(f"{i+1}. ({articles[i]['source']['name']}) {articles[i]['title']}")
            print(f"{articles[i]['description']}\n")
            
            insert = '''
                INSERT INTO news
                VALUES (?, ?, ?, ?, ?, ?)
            '''

            listings = [city, city_woeid, i+1, articles[i]['source']['name'], articles[i]['title'], articles[i]['description']]
            cur.execute(insert, listings)
            conn.commit()


def get_twitter_trends(woeid, number=10, exclude=None):
        """Return the top 10 trending topics for a specific WOEID, if trending
        information is available for it.

        Args:
          woeid:
            the Yahoo! Where On Earth ID for a location.
          exclude:
            Appends the exclude parameter as a request parameter.
            Currently only exclude=hashtags is supported. [Optional]
          number:
            number of trends to include

        Returns:
          None
        """
        url = 'https://api.twitter.com/1.1/trends/place.json'
        params = {'id': city_woeid}

        response = requests.get(url, params=params, auth=oauth)
        trends = json.loads(response.text)

        if type(trends) == dict:
          if 'errors' in trends.keys():
            return

        # check to make sure there are more trends than number
        elif len(trends[0]['trends']) < number and len(trends[0]['trends']) > 0:
          number = len(trends[0]['trends']) 

        insert = '''
            INSERT INTO twitter
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        tweets = [city, city_woeid, trends[0]['trends'][0]['name'], trends[0]['trends'][1]['name'],
                 trends[0]['trends'][2]['name'], trends[0]['trends'][3]['name'], trends[0]['trends'][4]['name'],
                 trends[0]['trends'][5]['name'], trends[0]['trends'][6]['name'], trends[0]['trends'][7]['name'],
                 trends[0]['trends'][8]['name'], trends[0]['trends'][9]['name']]
        cur.execute(insert, tweets)
        conn.commit()
    
        print("")
        print(f'{number} Trending topics on Twitter in {city}')
        print("-------------------------------------------")

        for i in range(number):
            print(trends[0]['trends'][i]['name'])


def get_trending_yelp(city_name, number=10, exclude=None):
        """Return the top 10 trending topics for a specific WOEID, if trending
        information is available for it.

        Args:
          city:
            (str) name of the city
          number:
            int representing number of trends to include
          exclude:
            Appends the exclude parameter as a request parameter.
            Currently only exclude=hashtags is supported. [Optional]
        Returns: 
          None
        """
        url = 'https://api.yelp.com/v3/businesses/search' 
        params = {'location': city_name, 'attributes': 'hot_and_new'}
        headers = {'Authorization': 'Bearer %s' % yelp_api_key}

        response = requests.get(url, params=params, headers=headers)
        businesses = json.loads(response.text)
        
        # make sure we don't exceed the amount we have
        if businesses['total'] < number and businesses['total'] > 0:
          number = businesses['total']

        businesses = businesses['businesses']
    
        print('')
        print(f'{number} Trending on Yelp in {city}')
        print("-------------------------------------------")

        for i in range(number):
            print(f"{i+1}. {businesses[i]['name']} ({businesses[i]['categories'][0]['title']}) - {businesses[i]['location']['address1']} {businesses[i]['location']['zip_code']}")
            
            insert = '''
                INSERT INTO yelp
                VALUES (?, ?, ?, ?, ?, ?, ?)
            '''

            listings = [city, city_woeid, i+1, businesses[i]['name'], businesses[i]['categories'][0]['title'], 
                     businesses[i]['location']['address1'], businesses[i]['location']['zip_code']]
            cur.execute(insert, listings)
            conn.commit()


if __name__ == "__main__":

    cities_searched = [] # list that tracks what cities have been looked up

    while True:
        city = input('Enter a city to get information (nashville, chicago, houston, philadelphia), type "view" to learn how to see your tables, or type "exit" to quit the program: ')
        city = city.lower()

        if city in woeid_dictionary and city not in cities_searched:
          cities_searched.append(city)
          city_woeid = woeid_dictionary[city]
          get_twitter_trends(woeid=city_woeid) # TODO: change so that printing and adding to database is dynamically based on api returns, not to exceed 10
          get_trending_yelp(city_name=city)
          get_stories(city_name=city)
          
        elif city == 'view':
          print("please run finalproj_app.py in another terminal window to view tables")

        elif city == 'exit':
          exit()
        
        elif city in cities_searched:
          print("sorry, already added to database")
        
        elif city not in woeid_dictionary: 
          print("sorry, not an option. Try checking your spelling and/or omitting the state")