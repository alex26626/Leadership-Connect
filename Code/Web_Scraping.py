from tqdm import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from bs4 import BeautifulSoup as bs
import selenium
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import chromedriver_autoinstaller

import urllib.request
import requests
import ssl

import re
import cv2

import warnings
warnings.filterwarnings('ignore')
import shutil
import time


'''
The following function allows to download images from Google Images.
Furthermore, it generates a file, where, for each downloaded image, the following attributes are provided:
- File Name: The name with which the downloaded image is saved.
- src: The src code of the image, which is an unique identifier allowing for the download of the image.
- Origin: The source from which the image is downloaded. 
It requires the following inputs:
- names: The list of names which will be written in the search bar of Google Images.
- folder: The directory of the folder where the images will be downloaded.
- n: The number of images which will be downloaded for each name. If n = 10, then the first 10 images will be downloaded.
- destination_name: The name of the csv file which will be generated.
'''

def download_n(names, folder, n, destination_name):
    #chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path='C:/Users/jing/Documents/Bocconi/DSBA/Leadership Connect/Image Scraping/chromedriver-win32/chromedriver-win32/chromedriver.exe', options=options)
    #Careful: usually "driver = webdriver.Chrome()" should work. Otherwise, it's necessary to insert the directory of the folder where the webdriver has been downloaded, like above.
    driver.set_page_load_timeout(60)
    driver.get('https://images.google.com/')
    cookie = driver.find_element(By.ID, 'L2AGLb')
    cookie.click()
    
    final_names = []
    origins_list = []
    src_list = []
    
    for i in tqdm(range(len(names))):
        full_name = names[i]
        while '/' in full_name:
            full_name.remove('/')
        
        search_bar = driver.find_element(By.CLASS_NAME, 'gLFyf')
        search_bar.send_keys(full_name)
        search_bar.send_keys(u'\ue007')
        
        time.sleep(2)
        
        all_images = driver.find_elements(By.XPATH, "//img[contains(@class,'Q4LuWd')]")
        all_origins = driver.find_elements(By.CLASS_NAME, 'LAA3yd')

        for j in range(min(n, len(all_images))):
            #print(j)
            src = all_images[j].get_attribute('src')
            src_list.append(src)
            origins_list.append(all_origins[j].text)
            final_name = full_name + '_' + str(j) +'.jpg'
            final_names.append(final_name)
            final_folder = folder + '/' + full_name + '_' + str(j) +'.jpg'
            urllib.request.urlretrieve(str(src), final_folder)
        driver.get('https://images.google.com/')
        
    final_dataset = pd.DataFrame()
    final_dataset['File Name'] = final_names
    final_dataset['src'] = src_list
    final_dataset['Origin'] = origins_list
    final_dataset.to_csv(destination_name)
    driver.close()

'''
The following function allows to download images from LinkedIn. It looks for at most 5 images for each person.
It returns three outputs:
- all_names: The list of the names of the downloaded images.
- all_images: The list of src codes of the images.
- all_experiences: The list of working experiences for each searched person.
NB: The order across the three lists is consistent.
It requires the following inputs:
- email: The email of the LinkedIn account.
- password_text: The password of the LinkedIn account.
- names: The list of names to be downloaded.
'''

def linkedin_scraping(email, password_text, names):
    
    start = time.time()
    ssl._create_default_https_context = ssl._create_unverified_context

    all_images = []
    all_experiences = []
    all_names = []

    driver =  webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    #options.add_argument('— incognito')
    options.add_argument('--disable-dev-shm-usage')
    #options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    driver.get('https://www.linkedin.com/feed/')
    account = driver.find_element(By.CLASS_NAME, 'main__sign-in-link')
    account.click()
    time.sleep(1)
    username = driver.find_element(By.ID, 'username')
    username.send_keys(email)
    time.sleep(1)
    password = driver.find_element(By.ID, 'password')
    password.send_keys(password_text)
    time.sleep(1)
    password.send_keys(u'\ue007')
    time.sleep(1)

    #Careful: The following two lines of code are necessary to deal with the "Accept Cookies" button.
    #accept = driver.find_element(By.CLASS_NAME, 'artdeco-button__text')
    #accept.click() 

    for i in tqdm(range(len(names))):
        #Insertion of the name
        full_name = names[i]
        first_name = full_name.split(' ')[0]
        last_name = full_name.split(' ')[-1]
        time.sleep(1)
        search_field = driver.find_element(By.XPATH, '//*[@id="global-nav-typeahead"]/input')
        search_field.send_keys(full_name)
        search_field.send_keys(u'\ue007')

        time.sleep(4)

        #Selection of the list of all individuals
        elements = driver.find_elements(By.CLASS_NAME, 'app-aware-link')
        for i in range(len(elements)):
            if elements[i].text == 'Vedi tutti i risultati - Persone':
                elements[i].click()
                break
        time.sleep(4)


        wait = WebDriverWait(driver, 10)
        all_people = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'app-aware-link')))
        all_people = driver.find_elements(By.CLASS_NAME, 'app-aware-link')
        clickable = []
        for i in range(len(all_people)):
            name = all_people[i].text.lower()
            if first_name.lower() in name or last_name.lower() in name:
                if all_people[i].get_attribute('href') not in clickable:
                    clickable.append(all_people[i].get_attribute('href'))
        time.sleep(2)

        for j in range(min(5, len(clickable))):
            driver.get(clickable[j])
            time.sleep(4)

            all_el = driver.find_elements(By.XPATH, "//*[contains(@id, 'ember')]")
            els = []
            for el in all_el:
                attempts_counter = 0
                while attempts_counter < 5: 
                    try:
                        #time.sleep(1)
                        els.append(el.text)
                        break
                    except StaleElementReferenceException:
                        attempts_counter += 1
                    except  WebDriverException:
                        attempts_counter += 1
            time.sleep(2)

            for h in range(len(els)):
                if els[h][:10] == 'Esperienza':
                    exp = np.unique(np.array(els[h].split('\n')))
                    exp = [el.lower() for el in exp]
                    break

            time.sleep(2)

            if h < len(els) - 1:
                attempt = 0
                while attempt < 5:
                    try:
                        image = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[1]/div[1]/div/button/img')))
                        image = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[1]/div[1]/div/button/img')
                        src = image.get_attribute('src')
                        name = full_name + '_' + str(j)
                        all_names.append(name)
                        all_images.append(str(src))
                        all_experiences.append(exp)
                        break
                    except TimeoutException:
                        driver.get(clickable[j])
                        attempt += 1
                    except NoSuchElementException:
                        driver.get(clickable[j])
                        attempt += 1
    
        driver.get('https://www.linkedin.com/feed/')
    driver.close()

    end = time.time()
    print(f'Total Time for {len(names)} people: {end-start} seconds')
    return all_names, all_images, all_experiences

'''
The following function cleans the list of experiences provided by the linkedin_scraping function.
It takes the list of experiences as an input, and it outputs the list of cleaned experiences.
The order is preserved.
'''

def exp_cleaning(all_experiences):
    
    for i in tqdm(range(len(all_experiences))):
        while '' in all_experiences[i]:
            all_experiences[i].remove('')
        for j in range(len(all_experiences[i])):
            all_experiences[i][j] = all_experiences[i][j].lower()
            if all_experiences[i][j][0] == ' ':
                all_experiences[i][j] = all_experiences[i][j][1:]
            if all_experiences[i][j][-1] == ' ':
                all_experiences[i][j] = all_experiences[i][j][:-1]
                
    return all_experiences

'''
The following function generates a dataframe with the outputs obtained from the linkedin_scraping function:
- Code Name: The specific name of the downloaded image (ex. Name_Surname_0.jpg).
- Full Name: The full name of the person in the image (ex. Name_Surname).
- Image: The src code of the image.
- Experience: The working experience of the person in the image.
The function needs as inputs the three outputs of the linkedin_scraping function.
'''

def link_data(all_names, all_experiences, all_images):
    
    linkedin = pd.DataFrame()
    simple_names = [all_names[i][:-2] for i in range(len(all_names))]
    exps = ['/'.join(all_experiences[i]) for i in range(len(all_experiences))]
    linkedin['Code Name'] = all_names
    linkedin['Full Name'] = simple_names
    linkedin['Image'] = all_images
    linkedin['Experience'] = exps
    
    linkedin = linkedin[linkedin['Image'] != 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'].reset_index(drop = True)
    linkedin = linkedin.drop_duplicates('Image').reset_index(drop = True)
    
    return linkedin


