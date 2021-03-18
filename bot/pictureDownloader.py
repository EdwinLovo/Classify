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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


DATASET_PATH = "D:/Development/Classify/classify_dataset/"
CATEGORIES = ["rubik's cube"]

def createFolder(path, folder):
    dirPath = os.path.join(path, folder)
    os.mkdir(dirPath)
    return dirPath


def saveImage(dirPath, index, content):
    image_file = io.BytesIO(content)
    image = Image.open(image_file).convert('RGB')
    path = dirPath + '/' + str(index) + '.jpg'
    with open(path, 'wb') as f:
        image.save(f, "JPEG", quality=85)


def downloadPictures(browser, name):
    searchBar = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//input[@id="search_form_input"]'))
    )
    searchBar.clear()
    searchBar.send_keys(name + ' pictures')
    searchBar.send_keys(Keys.ENTER)

    browser.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
    sleep(5)
    browser.execute_script(
        "window.scrollTo({top: 50000, behavior: 'smooth'});")
    sleep(5)

    imageContainers = browser.find_elements_by_xpath(
        '//div[@class="tile  tile--img  has-detail"]')

    datasetPath = createFolder(
        DATASET_PATH, name)
    print(datasetPath)

    i = 0
    for container in imageContainers:
        try:
            url = container.find_element_by_xpath(
                './/img').get_attribute('src')
            print("Image #", i, ", url:", url)
            imageContent = requests.get(url).content
            saveImage(datasetPath, i, imageContent)
        except:
            print('Error')

        i += 1

def openBrowser(browser):
    mainSearchBar = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//input[@id="search_form_input_homepage"]'))
    )
    mainSearchBar.send_keys('images')

    mainSearchButton = browser.find_element_by_xpath(
        '//input[@id="search_button_homepage"]')
    mainSearchButton.click()

    imagesSection = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//a[@data-zci-link="images"]'))
    )
    imagesSection.click()



opts = Options()
opts.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.102')

browser = webdriver.Chrome(
    'D:/Development/Classify/bot/drivers/chromedriver.exe', options=opts)
browser.get('https://duckduckgo.com/')



openBrowser(browser)

for category in CATEGORIES:
    downloadPictures(browser, category)
