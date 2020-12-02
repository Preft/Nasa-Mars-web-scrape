import cssutils
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    #Creates browser
    browser = init_browser()
    #////////////////////////////////Section 1:////////////////////////////////
    #//////////// Obtaining most recent article information. //////////////////
    #//////////////////////////////////////////////////////////////////////////
    #Navigates and grabs page html
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Finds article information
    Nasa_Articles = soup.find('ul', class_='item_list')
    Nasa_Mars_Titles_html = Nasa_Articles.find_all('div', class_='content_title')
    Nasa_Mars_Content_html = Nasa_Articles.find_all('div', class_='article_teaser_body')
    #List containing all article information
    Nasa_Mars_Titles = [article.text for article in Nasa_Mars_Titles_html]
    Nasa_Mars_Content = [article.text for article in Nasa_Mars_Content_html]
    #Saves the newest article information
    Nasa_Mars_Newest_Title = Nasa_Mars_Titles[0]
    Nasa_Mars_Newest_Content = Nasa_Mars_Content[0]
    #////////////////////////////////Section 2:////////////////////////////////
    #///////////////////////////Featured Image Url/////////////////////////////
    #//////////////////////////////////////////////////////////////////////////
    #Navigates and grabs page html
    url ='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(.1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Finds Featured image information
    Nasa_Image = soup.find('div', class_='carousel_items')
    Nasa_Image_Style = Nasa_Image.find('article')['style']
    #Grabs Featured Image url
    Styles = cssutils.parseStyle(Nasa_Image_Style)
    Back_Image_Arguement = Styles['background-image']
    End_Path = Back_Image_Arguement.replace('url(', '').replace(')', '')
    #Saves Featured Image url
    Featured_Image_url = 'https://www.jpl.nasa.gov' + End_Path
    #////////////////////////////////Section 3:////////////////////////////////
    #//////////////////////////////Mars Fact Table/////////////////////////////
    #//////////////////////////////////////////////////////////////////////////
    #Navigates and grabs page tables
    url ='https://space-facts.com/mars/'
    tables = pd.read_html(url)
    #Grabls mars fact table
    Mars_Facts_DF = tables[0]
    Mars_Facts_DF = Mars_Facts_DF.rename(columns={0: "Parameters", 1: "Values"})
    Mars_Facts_DF = Mars_Facts_DF.set_index('Parameters')
    Mars_Facts_html_table = Mars_Facts_DF.to_html()
    #////////////////////////////////Section 4:////////////////////////////////
    #//////////////////////Mars Hemispheres Information////////////////////////
    #//////////////////////////////////////////////////////////////////////////
    #Navigates and grabs Hemisphere links
    url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(.1)
    Grab_Hemisphere_Links = browser.links.find_by_partial_text('Hemisphere Enhanced')
    #Loops through number of Hemisphere Links
    Hemisphere_list =[]
    for link in range(len(browser.links.find_by_partial_text('Hemisphere Enhanced'))):
        browser.visit(url)
        Grab_Hemisphere_Links = browser.links.find_by_partial_text('Hemisphere Enhanced')
        image_text = Grab_Hemisphere_Links[link].text
        #Clicks link to grab and store info
        Grab_Hemisphere_Links[link].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image = soup.find_all('img', class_='wide-image')
        #Stores Hemisphere info in dictionary
        for image in image:
            image_url = 'https://astrogeology.usgs.gov' + image['src']
            Hemisphere_list.append({"title": image_text, "img_src": image_url})
        browser.visit(url)
    #Closes Browser
    browser.quit()
    returning_dict ={
        "Article_Title": Nasa_Mars_Newest_Title,
        "Article_Content": Nasa_Mars_Newest_Content,
        "Featured_Image_url": Featured_Image_url,
        "Mars_Facts_html_table": Mars_Facts_html_table,
        "Hemisphere_list": Hemisphere_list
    }
    return returning_dict