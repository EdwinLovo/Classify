import requests 
from PIL import Image
import io
from time import sleep
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.102')

browser = webdriver.Chrome('D:/Development/Classify/bot/drivers/chromedriver.exe', options=opts)

browser.get('https://duckduckgo.com/')
# searchBar = browser.find_element_by_xpath('//input[@class="search_form_input_homepage"]')
# searchBar.send('dog pictures')

# searchButton = browser.find_element_by_xpath('//span[@class="badge-link__btn btn btn--primary js-badge-link-button"]')
# searchButton.click()

searchBar = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, '//input[@id="search_form_input_homepage"]'))
)
searchBar.send_keys('dog pictures')

searchButton = browser.find_element_by_xpath('//input[@id="search_button_homepage"]')
searchButton.click()

imagesSection = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, '//a[@data-zci-link="images"]'))
)
imagesSection.click()

# searchButton = WebDriverWait(browser, 10).until(
#     EC.presence_of_element_located(
#         (By.XPATH, '//button[@class="Tg7LZd"]'))
# )
# searchButton.click()

browser.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
sleep(5)
browser.execute_script("window.scrollTo({top: 20000, behavior: 'smooth'});")
sleep(5)

imageContainers = browser.find_elements_by_xpath('//div[@class="tile  tile--img  has-detail"]')

dirPath = os.path.join("D:/Development/Classify/classify_dataset/train/", "dog")
os.mkdir(dirPath)
print(dirPath)

i = 0
for container in imageContainers:
    print('Entre')
    try:
        url = container.find_element_by_xpath('.//img').get_attribute('src')
        print("Image url: ", url)
        imageContent = requests.get(url).content

        image_file = io.BytesIO(imageContent)
        image = Image.open(image_file).convert('RGB')
        path = dirPath + '/' + str(i) + '.jpg'
        with open(path, 'wb') as f:
            image.save(f, "JPEG", quality=85)

    except:
        print('Error')
    
    i += 1