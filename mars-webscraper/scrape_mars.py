def scrape():
    #Import dependencies
    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    from flask import Flask, render_template
    import requests
    import pandas as pd
    import time
    
    #Initialize web scraper
    def init_browser():
        executable_path = {"executable_path": "/users/samuelgiddins/desktop/chromedriver"}
        return Browser("chrome", **executable_path, headless=False)
    browser = init_browser()
    mars_news_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_news_url)
   
    #Scrape the Mars news page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    #Save title and body as variables
    soup_chunk_1 = soup.select_one('ul.item_list li.slide')
    first_news_title = soup_chunk_1.find("div", class_='content_title').get_text()
    first_news_body = soup_chunk_1.find("div", class_='article_teaser_body').get_text()
   
    #Visit the featured image URL
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    time.sleep(1)
   
    #Find the image in the html
    browser.find_by_id('full_image').click()
    time.sleep(1)
    browser.find_link_by_partial_text('more info').click()
   
    #New html and soup variables for featured image scrape
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')
   
    #Store the image path as a full variable 
    partial_url = soup2.select_one('figure.lede a img').get('src')
    img_path = f'https://www.jpl.nasa.gov{partial_url}'
    
    #New variables to store Mars weather tweet info
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    time.sleep(1)
    html3 = browser.html
    soup3 = bs(html3, 'html.parser')
    twitter_chunk_1 = soup3.select_one("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather_tweet = twitter_chunk_1.get_text()
   
    #Read in mars facts table and convert to HTML
    facts = 'https://space-facts.com/mars/'
    table = pd.read_html(facts)
    mars_facts = table[0].to_html()
    facts_table = mars_facts.replace('\n', '')
    
    #New variables for Mars hemisphere URL's
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    time.sleep(1)
    html4 = browser.html
    soup4 = bs(html4, 'html.parser')
    
    #Find the section of the html where the hemisphere image links are stored, iterate through them and save the URL's 
    hemisphere_img_urls = []
    links = browser.find_by_css("a.product-item h3")
    for object in range(len(links)):
        hemisphere_obj = {}
        browser.find_by_css("a.product-item h3")[object].click()
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere_obj['img_url'] = sample_elem['href']
        hemisphere_obj['title'] = browser.find_by_css("h2.title").text
        hemisphere_img_urls.append(hemisphere_obj)
        browser.back()
   
    #store scraped info in a dcitionary for mongo
    mars_dict = {
    "news_title": first_news_title,
    "news_body": first_news_body,
    "featured_image_path": img_path,
    "weather_tweet": mars_weather_tweet,
    "hemisphere_img_url1": hemisphere_img_urls[0],
    "hemisphere_img_url2": hemisphere_img_urls[1],
    "hemisphere_img_url3": hemisphere_img_urls[2],
    "hemisphere_img_url4": hemisphere_img_urls[3]  
    }
    return(mars_dict)