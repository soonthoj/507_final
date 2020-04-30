from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/city')
def city():
    return render_template('city.html')

@app.route('/cities')
def cities():
    return render_template('cities.html')


### Get Yelp for Cities
###

def get_yelp_nashville():
    conn = sqlite3.connect('finalproj.db')
    cur = conn.cursor()
    q = '''
        SELECT * FROM yelp
        WHERE cityName="nashville"
        ORDER BY yelpNumber ASC
        LIMIT 10
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results

def get_yelp_chicago():
    conn = sqlite3.connect('finalproj.db')
    cur = conn.cursor()
    q = '''
        SELECT * FROM yelp
        WHERE cityName="chicago"
        ORDER BY yelpNumber ASC
        LIMIT 10
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results

def get_yelp_houston():
    conn = sqlite3.connect('finalproj.db')
    cur = conn.cursor()
    q = '''
        SELECT * FROM yelp
        WHERE cityName="houston"
        ORDER BY yelpNumber ASC
        LIMIT 10
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results

def get_yelp_philadelphia():
    conn = sqlite3.connect('finalproj.db')
    cur = conn.cursor()
    q = '''
        SELECT * FROM yelp
        WHERE cityName="philadelphia"
        ORDER BY yelpNumber ASC
        LIMIT 10
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results


### Get News for Cities
###

def get_news_nashville():
    conn = sqlite3.connect('finalproj.db')
    cur = conn.cursor()
    q = '''
        SELECT * FROM news
        WHERE cityName="nashville"
        ORDER BY articleNumber ASC
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results

def get_news_chicago():
    conn = sqlite3.connect('finalproj.db')
    cur = conn.cursor()
    q = '''
        SELECT * FROM news
        WHERE cityName="chicago"
        ORDER BY articleNumber ASC
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results

def get_news_houston():
    conn = sqlite3.connect('finalproj.db')
    cur = conn.cursor()
    q = '''
        SELECT * FROM news
        WHERE cityName="houston"
        ORDER BY articleNumber ASC
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results

def get_news_philadelphia():
    conn = sqlite3.connect('finalproj.db')
    cur = conn.cursor()
    q = '''
        SELECT * FROM news
        WHERE cityName="philadelphia"
        ORDER BY articleNumber ASC
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results


### Get Twitter Trends for Cities
###

def get_twitter_nashville():
    conn = sqlite3.connect('finalproj.db')
    cur = conn.cursor()
    q = '''
        SELECT * FROM twitter
        WHERE cityName="nashville"
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results

def get_twitter_chicago():
    conn = sqlite3.connect('finalproj.db')
    cur = conn.cursor()
    q = '''
        SELECT * FROM twitter
        WHERE cityName="chicago"
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results

def get_twitter_houston():
    conn = sqlite3.connect('finalproj.db')
    cur = conn.cursor()
    q = '''
        SELECT * FROM twitter
        WHERE cityName="houston"
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results


def get_twitter_philadelphia():
    conn = sqlite3.connect('finalproj.db')
    cur = conn.cursor()
    q = '''
        SELECT * FROM twitter
        WHERE cityName="philadelphia"
    '''
    results = cur.execute(q).fetchall()
    conn.close()
    return results


### App route statements
###

@app.route('/city/nashville')
def nashville():
    city_name='nashville'
    news=get_news_nashville()
    twitter=get_twitter_nashville()
    yelp=get_yelp_nashville()
    return render_template('nashville-results.html', yelp=yelp, news=news, twitter=twitter)

@app.route('/city/chicago')
def chicago():
    city_name='chicago'
    news=get_news_chicago()
    twitter=get_twitter_chicago()
    yelp=get_yelp_chicago()
    return render_template('chicago-results.html', yelp=yelp, news=news, twitter=twitter, city_name=city_name)

@app.route('/city/houston')
def houston():
    city_name='houston'
    news=get_news_houston()
    twitter=get_twitter_houston()
    yelp=get_yelp_houston()
    return render_template('houston-results.html', yelp=yelp, news=news, twitter=twitter, city_name=city_name)

@app.route('/city/philadelphia')
def philadelphia():
    city_name='philadelphia'
    news=get_news_philadelphia()
    twitter=get_twitter_philadelphia()
    yelp=get_yelp_philadelphia()
    return render_template('philadelphia-results.html', news=news, twitter=twitter, yelp=yelp, city_name=city_name)


if __name__ == '__main__':
    app.run(debug=True)