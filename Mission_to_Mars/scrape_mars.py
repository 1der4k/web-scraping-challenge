#dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def mars_scraper():
    browser = Browser('chrome',executable_path = "C:/Users/19105/ChromeDriver",headless=True)
    
    # NASA Mars News
    browser.visit("https://redplanetscience.com/")

    html = browser.html
    soup = bs(html, "html.parser")

    raw_news_title = soup.find('div', class_ = "content_title")
    raw_news_teaser = soup.find('div', class_ = "article_teaser_body")

    news_title = raw_news_title.text
    news_teaser = raw_news_teaser.text


    # JPL Mars Space Images
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    featured_image_href = soup.find('a', class_ = "showimg fancybox-thumbs")

    href = featured_image_href['href']

    img_url = url + href

    # Mars Facts table
    browser.visit("https://galaxyfacts-mars.com")

    html = browser.html
    soup = bs(html, "html.parser")

    scrape_facts = []

    table = soup.find("div", class_ = "sidebar")
    facts = table.find_all("tr")

    for fact in facts:
        scrape_facts.append({"category":fact.th.text, "data":fact.td.text.strip()})

    scrape_facts_df = pd.DataFrame(scrape_facts)
    scrape_facts_html = scrape_facts_df.to_html(header=False)

    # Mars Hemispheres images scrape
    url = "https://marshemispheres.com/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    collapsible = soup.find("div", class_ = "collapsible results")
    
    h3_clean = []

    h3 = collapsible.find_all("h3")
    for item in h3:
        h3_clean.append(item.text.strip())
        
    h3_clean

    full_url_list = []

    for item in h3_clean:
        browser.links.find_by_partial_text(item).click()

        html_2 = browser.html
        soup_2 = bs(html_2, "html.parser")

        downloads = soup_2.find("div", class_ = "downloads")
        
        img_anchor = downloads.find("a")
        href = img_anchor['href']
        #href
        
        full_url = url + href
        #full_url
        
        full_url_list.append(full_url)
        
        browser.back()

    browser.quit()

    mars_hemi_dict = []

    hemisphere_list = []

    for item in h3_clean:
        item = item.replace(' Enhanced','')
        hemisphere_list.append(item)

    loop = 0

    for item in hemisphere_list:
        
        mars_hemi_dict.append({"title":item, "img_url":full_url_list[loop]})
        loop += 1

    mars_data_dict = {
        "mars_news" : {
            news_title : news_teaser
        },
        "featured_img" : img_url,
        "mars_facts" : scrape_facts_html,
        "mars_hemispheres" : mars_hemi_dict
    }

    return mars_data_dict