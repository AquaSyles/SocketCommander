from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import threading
import os
import pickle


def join_party(driver, code):
    party_url = "https://www.geoguessr.com/join" 

    driver.get(party_url) 

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

def main(parameters):
    driver = webdriver.Firefox()

    url = "https://www.geoguessr.com"

    threading.Thread(target=check_running, args=(driver,)).start()

    driver.get(url)

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
    
    join_party(driver, parameters[0])
    
    time.sleep(10000)

def check_running(driver):
    while True:
        try:
            with open(config_path, 'rb') as file:
                data = pickle.load(file)

                if data['status'] == 0:
                    driver.close()
                    exit()
        except:
            pass

def get_parameters():
    with open(config_path, 'rb') as file:
        data = pickle.load(file)
        
        parameters = data['parameters']
        if parameters:
            return parameters

        return 0

config_path = os.path.dirname(__file__) + '/config.pkl'

parameters = get_parameters()

if parameters:
    main(parameters)
