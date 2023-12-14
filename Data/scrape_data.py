from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import pandas as pd

def scroll_to_bottom(driver):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(0.01)

def click_show_more(driver):
    show_more_button_xpath = "//button[@data-testid='button-load-more-button-donation-list-box-subject-supporters-section-fundraise-page']"

    try:
        show_more_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, show_more_button_xpath))
        )
        show_more_button.click()
        time.sleep(0.01)
    except Exception as e:
        print(f"Error: {e}")

def scrape_recent_donations(driver, count=6):
    recent_donations_info = []

    donations_xpath = "//li[contains(@data-testid, 'donation-list-item-')]"

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, donations_xpath))
        )
    except Exception as e:
        print(f"Error: {e}")
        return recent_donations_info

    while True:
        donations_elements = driver.find_elements(By.XPATH, donations_xpath)
        for donation_element in donations_elements:
            try:
                name = donation_element.get_attribute("aria-label").replace("Wpłata od - ", "")
                amount = donation_element.find_element(By.XPATH, ".//span[@class='sc-spCdH ktssxh']").text
                date_time = donation_element.find_element(By.XPATH, ".//time[@class='sc-khrQBJ jVFOmt']").get_attribute("datetime")

                message_element = donation_element.find_elements(By.XPATH, ".//p[@class='sc-eTOxzm eoQJpi']")
                message = message_element[0].text if message_element else "Null"

                donation_info = {
                    'name': name,
                    'amount': amount,
                    'date_time': date_time,
                    'message': message,
                    'goal': 1
                }
                recent_donations_info.append(donation_info)

            except StaleElementReferenceException as e:
                print(f"Stale Element Reference Exception: {e}")
                continue

        for donation_element in donations_elements[-count:]:
            driver.execute_script("arguments[0].remove();", donation_element)

        try:
            scroll_to_bottom(driver)
            time.sleep(0.01)
        except Exception as e:
            print(f"Error while scrolling: {e}")
            break

        if len(recent_donations_info) >= count:
            return recent_donations_info

url = "https://www.siepomaga.pl/x-stream-charytatywny-ekipy-fantasy-cel-x"
path = r"C:\Users\marci\Downloads\chromedriver-win64\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument(f"webdriver.chrome.driver:{path}")

driver = webdriver.Chrome(options=options)
driver.get(url)

all_donations_info = []

scroll_to_bottom(driver)

while True:
    click_show_more(driver)
    recent_donations_info = scrape_recent_donations(driver, count=6)
    all_donations_info.extend(recent_donations_info)

    if len(all_donations_info) >= 180:
        break

df = pd.DataFrame(all_donations_info)
df.to_csv('donations_data_2.csv', index=False, mode='a')

input("Naciśnij Enter, aby zamknąć przeglądarkę...")
