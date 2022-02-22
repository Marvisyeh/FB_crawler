from selenium import webdriver
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import requests

# 進入主頁
def chorme_get_page(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("user-agent={}".format(generate_user_agent()))
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs",prefs)

    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)

    driver.implicitly_wait(20)
    driver.get(url)
    res = driver.page_source
    soup = BeautifulSoup(res, 'html.parser')
    driver.quit()
    return soup



# get content without selenium
def get_page(url):
    headers = {'User-Agent':generate_user_agent()}
    next_res = requests.get(url, headers=headers)
    next_soup = BeautifulSoup(next_res, 'html.parser')

    return next_soup

if __name__ == '__main__':
    url= 'https://mbasic.facebook.com/groups/1260448967306807'
    print(chorme_get_page(url))