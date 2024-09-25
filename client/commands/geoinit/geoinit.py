from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import threading
import os

driver = webdriver.Firefox()

url = "https://www.geoguessr.com"
driver.get(url)

def join_party(driver):
    party_url = url + "/join"

    driver.get(party_url)

    code = "8RC8"

    code_input_field = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[2]/main/div/div[2]/div/div/div[1]'))
    )
    letter_fields = code_input_field.find_elements(By.TAG_NAME, 'input')

    for i, letter_field in enumerate(letter_fields):
        letter_field.send_keys(code[i])

    name = "TEST"

    name_field = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[2]/main/div/div[2]/form/div[1]/div/div/input'))
    )
    name_field.send_keys(name + Keys.ENTER)

def main():
    # Press custom on ads
    try:
        ad_custom_btn = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='sn-b-custom']"))
        )

        ad_custom_btn.click()
    except:
        print("Couldn't find ad_custom_btn")
    
    # Decline ads
    try:    
        ad_save_btn = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="sn-b-save"]'))
        )

        ad_save_btn.click()
    except:
        print("Couldn't find ad_save_btn")
    
    join_party(driver)
    
    time.sleep(10000)  # Sleep to avoid busy-waiting

def check_running(driver):
    running_path = os.path.dirname(__file__) + '/running'

    while True:
        with open(running_path, 'r') as file:
            for line in file:
                if line == '0':
                    driver.close()
                    exit()

threading.Thread(target=check_running, args=(driver,)).start()
main()
