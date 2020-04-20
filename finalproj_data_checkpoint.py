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

conn = sqlite3.connect("finalproj.db")
cur = conn.cursor()

client_key = secrets.TWITTER_API_KEY
client_secret = secrets.TWITTER_API_SECRET_KEY
access_token = secrets.TWITTER_ACCESS_TOKEN
access_token_secret = secrets.TWITTER_ACCESS_TOKEN_SECRET

yelp_api_key = secrets.YELP_API_KEY
yelp_client_key = secrets.YELP_CLIENT_KEY

newsapi = NewsApiClient(api_key=secrets.NEWS_API_KEY)


# pass object along with requests.get() request and parameters
oauth = OAuth1(client_key,
            client_secret=client_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret)


# dictionary of yahoo woeids for 10 major cities in america. Will need to use this for twitter api query
# woeid api is no longer supported by yahoo, so manual look up plus adding to dictionary is fastest way to build this in.
woeid_dictionary = {'new york': 2459115, 'los angeles': 2442047, 'chicago': 2379574, 'houston': 2424767, 'phoenix': 2471390,
                    'philadelphia': 2471217, 'san antonio': 2487796, 'san diego': 2487889, 'dallas': 2388929, 'san jose': 2488042}


def get_stories(city_name, number=10):
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
          A list with 10 entries. Each entry contains a trend.
        """
        # /v2/top-headlines
        articles = newsapi.get_everything(q=city_name, language='en')
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


def get_twitter_trends(number=10, exclude=None):
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
          A list with 10 entries. Each entry contains a trend.
        """
        url = 'https://api.twitter.com/1.1/trends/place.json'
        params = {'id': city_woeid}

        response = requests.get(url, params=params, auth=oauth)
        trends = json.loads(response.text)

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


def get_trending_restaurants(city_name, number=10, exclude=None):
        """Return the top 10 trending topics for a specific WOEID, if trending
        information is available for it.

        Args:
          woeid:
            int representing the Yahoo! Where On Earth ID for a location. Stored in a dictionary
          exclude:
            Appends the exclude parameter as a request parameter.
            Currently only exclude=hashtags is supported. [Optional]
          number:
            int representing number of trends to include

        Returns:
          A list with 10 entries. Each entry contains a trend.
        """
        url = 'https://api.yelp.com/v3/businesses/search' 
        params = {'location': city_name, 'attributes': 'hot_and_new'}
        headers = {'Authorization': 'Bearer %s' % yelp_api_key}

        response = requests.get(url, params=params, headers=headers)
        businesses = json.loads(response.text)
        businesses = businesses['businesses']
    
        print('')
        print(f'{number} Trending Restaurants on Yelp in {city}')
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

    while True:

        city = input('Enter a city: ')
        city = city.lower()

        if city in woeid_dictionary:
            city_woeid = woeid_dictionary[city]
            get_twitter_trends()
            get_trending_restaurants(city_name=city)
            get_stories(city_name=city)