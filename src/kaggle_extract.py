import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions



#### archiving old datasets ####
# moving the old csv files to archiv folder


#### EXTRACTING Kaggle datasets  with selenium #####

driver = webdriver.Chrome(r"D:\SeleniumDriver\chromedriver.exe")

# login into Kaggle to be able to download the csv files
mail = os.environ.get('Mail')
kaggle_pw = os.environ.get('Kaggle-PW')

login_url = str('https://www.kaggle.com/account/login?phase=emailSignIn')
driver.get(login_url)

WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.NAME, 'email')))

driver.find_element(By.NAME, 'email').send_keys(mail)
driver.find_element(By.NAME, 'password').send_keys(kaggle_pw)

WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'button.sc-gkJlnC biOnsZ')))
driver.find_element(By.CSS_SELECTOR, 'button.sc-gkJlnC biOnsZ').click()


# downlaoding the csv files
# stadiums_url = 'https://www.kaggle.com/datasets/tobycrabtree/nfl-scores-and-betting-data?resource=download&select=nfl_stadiums.csv'
# teams_url = 'https://www.kaggle.com/datasets/tobycrabtree/nfl-scores-and-betting-data?resource=download&select=nfl_teams.csv'
# spread_scores = 'https://www.kaggle.com/datasets/tobycrabtree/nfl-scores-and-betting-data?resource=download&select=spreadspoke_scores.csv'
# dl_button_xpath = '/html/body/main/div[1]/div/div[5]/div[2]/div[5]/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/i'



# driver.get(stadiums_url)
# WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, dl_button_xpath)))
# button = driver.find_element(By.XPATH, f'{dl_button_xpath}')
# button.click()

# df = pd.read_csv('/Users/simon/Downloads/nfl_stadiums.csv')
# print(df.head)

# # unzipping the spread_score file