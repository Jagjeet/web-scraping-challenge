from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
import pandas as pd
import requests

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = { "executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape_nasa_mars_news():
    url = 'https://mars.nasa.gov/news/'

    browser = init_browser()
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    browser.quit()

    soup = BeautifulSoup(html, "html.parser")

    slides = soup.find_all('li', class_='slide')
#     print(slides[0].prettify())

    title = slides[0].find('div', class_='content_title')
    link = title.find('a')
    teaser = slides[0].find('div', class_='article_teaser_body')
    
    return link.text.strip(), teaser.text.strip()


def scrape_jpl_featured_image():
    browser = init_browser()

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    browser.visit(url)
    html = browser.html

    browser.quit()

    soup = BeautifulSoup(html, "html.parser")
    header = soup.find('div', class_='header')
    text_area = header.find('div', class_='floating_text_area')
    link = text_area.find('a', class_='showimg')

    #For getting the base URL see:
    #https://stackoverflow.com/questions/35616434/how-can-i-get-the-base-of-a-url-in-python
    return urljoin(url, '.') + link['href']


def scrape_mars_space_facts():

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(requests.get(url).text)
    df = tables[2]
    return df.to_html(classes='table table-striped', header=False, index=False)

import time

url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

def scrape_mars_hemispheres():
    hemisphere_list = []
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser = init_browser()
    browser.visit(url)
    html = browser.html

    soup = BeautifulSoup(html, "html.parser")
    mars_section = soup.find("section", {"id": "results-accordian"})
    # mars_section = soup.find("section")
    descriptions = mars_section.find_all('div', class_='description')

    # print(mars_section.prettify())
    # print(descriptions)

    for desc in descriptions:
        mars_dict = {}
        # print(desc.prettify())
        title = desc.find("h3").text
        # print(title)
        mars_dict['title'] = title
        link = desc.find("a", class_='product-item')

        link_url = urljoin(url, '/') + link['href']
        # print(link_url)
        browser.visit(link_url)
        link_html = browser.html
        time.sleep(1)

        # print(link_html)
        link_soup = BeautifulSoup(link_html, 'html.parser')
        download = link_soup.find("div", class_="downloads")
        img_anchor = download.find("a")
        # print(download)
        # print(img_anchor)
        # print(img_anchor['href'])
        mars_dict['img_url']=img_anchor['href']
        hemisphere_list.append(mars_dict)

    browser.quit()

    return hemisphere_list

def scrape_mars_data():
    mars_dict = {}

    # Mars News
    news_tuple = scrape_nasa_mars_news()
    news_title, news_p = news_tuple
    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p

    # JPL
    mars_dict['featured_image_url'] = scrape_jpl_featured_image()

    # Mars Space Facts
    mars_dict['space_facts_HTML'] = scrape_mars_space_facts()

    # Mars Hemisphers
    mars_dict['hemispheres'] = scrape_mars_hemispheres()

    return mars_dict

# mars_dict = scrape_mars_data()
# print(mars_dict)