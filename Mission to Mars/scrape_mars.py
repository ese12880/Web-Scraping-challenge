from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\\bin\chromedriver.exe"}
    return Browser("chrome", executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    def nasa():
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        time.sleep(2)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        news_ttl=[]
        for div in soup.find_all('div', attrs={'class':'content_title'}):
            news_ttl.append(div.find('a'))
        news_title=news_ttl[1].text
        # print(soup.find_all('div', attrs={'class':'article_teaser_body'})[0].text)
        news=soup.find('div', attrs={'class':'article_teaser_body'}).text
        return(news_title,news)

    news_title,news_p=nasa()
    def marsPhoto():
        url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
        browser.visit(url)
        time.sleep(2)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        image_url=soup.find('img', attrs={'class':'thumb'})
        featured_image_url=f"https://www.jpl.nasa.gov{image_url['src']}"

        return(featured_image_url)

    featured_image_url=marsPhoto()
        
    #Mars Fact
    def marsFact():
        url='https://space-facts.com/mars/'
        tables = pd.read_html(url)
        time.sleep(3)
        df=tables[0].reset_index(drop=True)
        df.columns = ['Attributes','Value']
        df['Attributes'] = [x.strip().replace(':', '') for x in df['Attributes']]
        df['Attributes'] = [x.strip().replace(' ', '') for x in df['Attributes']]
        df=df.set_index('Attributes').T.to_dict('records')[0]
        # df=df.to_dict('records')
        return df
    mars_fact=marsFact()
    def marsHemisphere(name):
        url=f'https://astrogeology.usgs.gov/search/map/Mars/Viking/{name}'
        browser.visit(url)
        time.sleep(2)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img=soup.find("div", attrs={"class":"wide-image-wrapper"}).find('li').find('a').get('href')
        title=soup.find("h2", attrs={"class":"title"}).text
        return img,title

    hemisphere_image_urls=[]
    image_links=['cerberus_enhanced','schiaparelli_enhanced','syrtis_major_enhanced','valles_marineris_enhanced']
    for image_link in range(0,len(image_links)):
        img_url,title=marsHemisphere(image_links[image_link])
        hemisphere={
        'title':title,
        'img_url':img_url
        }
        hemisphere_image_urls.append(hemisphere)

    nasa_data = {
        "news_title": news_title,
        "news_p": news_p,
        "mars_weather":mars_weather,
        "featured_image_url": featured_image_url

    }
    
    browser.quit()

    # Return results
    return nasa_data,mars_fact,hemisphere_image_urls