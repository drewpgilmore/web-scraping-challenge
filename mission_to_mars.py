#dependencies
#------------
from bs4 import BeautifulSoup as bs
import pymongo
import requests as r
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd

#initiate splinter/browser
#-------------------------
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

#step 1 - NASA article scraping
#------------------------------
nasa_site = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
response = r.get(nasa_site)
soup = bs(response.text, 'html.parser')
articles = soup.find_all('div', class_='slide')
titles = []
paragraphs = []

for article in articles:
    title = article.find('div', class_='content_title').text
    titles.append(title)
    paragraph = article.find('div', class_='rollover_description_inner').text
    paragraphs.append(paragraph)
#return items
news_title = titles[0]
news_p = paragraphs[0]

#step 2 - JPL image scraping
#---------------------------
jpl_link = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(jpl_link)
html = browser.html
soup = bs(html, 'html.parser')
button = soup.find('a', class_='button fancybox')
feature_link = button.attrs['data-fancybox-href']
#return item
featured_image_url = f'https://www.jpl.nasa.gov{feature_link}'

#step 3 - mars facts scraping
#----------------------------
mars_facts = 'https://space-facts.com/mars/'
tables = pd.read_html(mars_facts)
#return items
mars_planet_profile_html = tables[0].to_html()
mars_earth_comparison_html = tables[1].to_html()

#step 4 - hemisphere image scraping
#----------------------------------
hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemisphere_url)
html = browser.html
soup = bs(html, 'lxml')
hemispheres = soup.find_all('div', class_='item')

#return item
hemisphere_image_urls = []

for hem in hemispheres:
    desc = hem.find('div', class_='description')
    
    path = desc.a['href']
    title = desc.h3.text
    url = f'https://astrogeology.usgs.gov{path}'
    
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'lxml')

    results = soup.find('div', class_='downloads')
    link = results.find('a')
    img_url = link['href']    

    #append dictionary of title and url to image url list
    hemisphere_image_urls.append({
        'title': title,
        'img_url': img_url
    })

