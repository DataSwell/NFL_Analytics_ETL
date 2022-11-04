import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from zipfile import ZipFile


#### EXTRACTING Kaggle datasets  with Selenium #####
# login credentials from our environment variables
mail = os.environ.get('Mail')
kaggle_pw = os.environ.get('Kaggle-PW')

driver = webdriver.Chrome(r"D:\SeleniumDriver\chromedriver.exe")
login_url = str('https://www.kaggle.com/account/login?phase=emailSignIn')
driver.get(login_url)

WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.NAME, 'email')))
print('Page loaded')
driver.find_element(By.NAME, 'email').send_keys(mail)
driver.find_element(By.NAME, 'password').send_keys(kaggle_pw)
print('Entered mail and pw')
WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="site-container"]/div/div[3]/form/div[2]/div[3]/button')))                                                                     
print('found button')
driver.find_element(By.XPATH, '//*[@id="site-container"]/div/div[3]/form/div[2]/div[3]/button').click()
print('login successful')

time.sleep(5)

# downlaoding the csv file
spread_scores_url = 'https://www.kaggle.com/datasets/tobycrabtree/nfl-scores-and-betting-data?resource=download&select=spreadspoke_scores.csv'
dwl_btn_xpath = '//*[@id="site-content"]/div[2]/div[2]/div/div[1]/div/a/button'
                
driver.get(spread_scores_url)
print('changed to spread_scores URL')
WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, dwl_btn_xpath)))
print('Button located')
driver.find_element(By.XPATH, dwl_btn_xpath).click()
print('Download successful')

time.sleep(10)

# deleting the old data in the download folder
if os.path.exists('C:/Users/simon/Downloads/archive.zip'):
  print('File exists')
else:
  print("The file does not exist")

# unzipping the downloaded file
# loading the archive.zip and creating a zip object
with ZipFile('C:/Users/simon/Downloads/archive.zip', 'r') as zip_object:

    # extracting the spreadspoke_score.csv file
    zip_object.extract('spreadspoke_scores.csv', path='D:/Projekte/Football_Analytics/data')

zip_object.close()

print('Zipfile extracted and moved')

# deleting the zip file in the download folder
if os.path.exists('C:/Users/simon/Downloads/archive.zip'):
  os.remove('C:/Users/simon/Downloads/archive.zip')
else:
  print("The file does not exist")