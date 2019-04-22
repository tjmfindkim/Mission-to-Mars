# Import Dependecies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd 
import requests
import time

### Initialize browser
def init_browser(): 

#Windows Users
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

mars_info = {}

# NASA MARS NEWS
def scrape_mars_news():
    
    try:
        browser = init_browser()
        
        # Visit Nasa news url through splinter module
        mars_url = 'https://mars.nasa.gov/news/'
        browser.visit(mars_url)

        time.sleep(1)

        # Scrape page into Soup
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup_mars = bs(html, 'html.parser')


        # Retrieve the latest element that contains news title and news_paragraph
        latest_mars_news_title = soup_mars.find('div', class_='content_title').text
        paragraph = soup_mars.find('div', class_='article_teaser_body').text


        # Store data from MARS NEWS into dictionary
        mars_info['news_title'] = latest_mars_news_title
        mars_info['news_paragraph'] = paragraph

        
        return mars_info

    finally:
        # Close the browser after scraping
        browser.quit()
        

# JPL Images
def jpl_mars_space_images():

    try: 
        browser = init_browser()

        # Visit JPL Images through splinter module
        jpl_url = 'https://www.jpl.nasa.gov'
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)
        
        time.sleep(1)

        # Scrape page into Soup
        jpl_image = browser.html
        # Parse HTML with Beautiful Soup
        soup_jpl = bs(jpl_image, 'html.parser')

        # Retrieve background-image url from style tag 
        featured_image  = soup_jpl.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Concatenate website url with scrapped route
        featured_image_url = jpl_url + featured_image

        # Display full link to featured image
        featured_image_url 

        # Dictionary entry from FEATURED IMAGE
        mars_info['featured_image'] = featured_image_url
        
        return mars_info
    
    finally:
        # Close the browser after scraping
        browser.quit()


# Mars Weather 
def scrape_mars_weather():

    try:
        browser = init_browser()

       # Visit Mars Weather Twitter through splinter module
        mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(mars_weather_url)

        time.sleep(1)

        # Scrape page into Soup
        html_mars_weather = browser.html
        # Parse HTML with Beautiful Soup
        soup_mars_weather = bs(html_mars_weather, 'html.parser')

        # Find all elements that contain tweets
        latest_mars_tweets = soup_mars_weather.find_all('div', class_='js-tweet-text-container')

        # Retrieve all elements that contain news title in the specified range
        # Look for entries that display weather related words to exclude non weather related tweets 
        for tweet in latest_mars_tweets: 
            mars_weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in mars_weather_tweet:
                print(mars_weather_tweet)
                break
            else: 
                pass

        # Dictionary entry from WEATHER TWEET
        mars_info['mars_weather_tweet'] = mars_weather_tweet
                        
        return mars_info
    
    finally:
        # Close the browser after scraping
        browser.quit()

# Mars Facts
def scrape_mars_facts():

    mars_facts_url = 'https://space-facts.com/mars/'
    
    # Use Panda's `read_html` to parse the url
    table = pd.read_html(mars_facts_url)
    df = table[0]
    
    # Assign the columns
    df.columns = ['Parameters','Values']
    
    # Set the index to the `Parameters`
    df.set_index('Parameters', inplace=True)
   
    # Save html code to folder Assets
    fact = df.to_html()

    # Dictionary entry from MARS FACTS
    mars_info['table'] = fact
        
    return mars_info


def scrape_mars_hemispheres():

    try: 
        browser = init_browser()

        # Visit hemispheres website through splinter module 
        hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemi_url)

        time.sleep(1)

        # Scrape page into Soup
        html_hemi = browser.html
        # Parse HTML with Beautiful Soup
        soup_hemi = bs(html_hemi, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup_hemi.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hemispheres = []

        # Store the main_ul 
        hemi_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemi_main_url + partial_img_url)
            
            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = bs(partial_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = hemi_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemispheres.append({"title" : title, "img_url" : img_url})

        mars_info['hemispheres'] = hemispheres

        
        # Return mars_data dictionary 

        return mars_info
    
    finally:

        # Close the browser after scraping
        browser.quit()