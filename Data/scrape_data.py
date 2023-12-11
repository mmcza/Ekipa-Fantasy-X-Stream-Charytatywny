from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def scroll_to_bottom(driver):
    # Scrolluj na sam dół strony
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    # Poczekaj, aż strona się załaduje
    time.sleep(1)

def click_show_more(driver):
    show_more_button_xpath = "//div[@class='sc-byUoaA cjFWkT']//button[@data-testid='button-load-more-button-donation-list-box-subject-supporters-section-fundraise-page']"

    while True:
        try:
            # Sprawdź, czy przycisk "Pokaż więcej" jest dostępny
            show_more_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, show_more_button_xpath))
            )
            # Kliknij przycisk, jeśli jest dostępny
            show_more_button.click()
            # Poczekaj 1 sekundę
            time.sleep(0.1)
        except Exception as e:
            # Jeśli przycisk nie jest już dostępny, przerwij pętlę
            print(f"Error: {e}")
            break

def scrape_donations_info(driver):
    donations_info = []

    # XPath do każdej dotacji
    donations_xpath = "//li[contains(@data-testid, 'donation-list-item-')]"

    # Sprawdź, czy przynajmniej jedna dotacja jest dostępna
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, donations_xpath))
        )
    except Exception as e:
        print(f"Error: {e}")
        return donations_info

    # Pobierz informacje z każdej dotacji
    donations_elements = driver.find_elements(By.XPATH, donations_xpath)
    for donation_element in donations_elements:
        name = donation_element.get_attribute("aria-label").replace("Wpłata od - ", "")
        amount = donation_element.find_element(By.XPATH, ".//span[@class='sc-hhpBdf bVGfl']").text
        date_time = donation_element.find_element(By.XPATH, ".//time[@class='sc-dAfKBC kinJVg']").get_attribute("datetime")

        # Sprawdź, czy element 'message' istnieje
        message_element = donation_element.find_elements(By.XPATH, ".//p[@class='sc-jxLbor dtGjUS']")
        message = message_element[0].text if message_element else "Null"

        donation_info = {
            'name': name,
            'amount': amount,
            'date_time': date_time,
            'message': message,
            'goal': 1
        }
        donations_info.append(donation_info)

    return donations_info

# Poniżej znajduje się kod do użycia funkcji w kontekście Twojego problemu
url = "https://www.siepomaga.pl/x-stream-charytatywny-ekipy-fantasy"
path = r"C:\Users\marci\Downloads\chromedriver-win64\chromedriver.exe"  # Update file extension to .exe

options = webdriver.ChromeOptions()
options.add_argument(f"webdriver.chrome.driver:{path}")

driver = webdriver.Chrome(options=options)
driver.get(url)

# Scrolluj na sam dół strony
scroll_to_bottom(driver)

# Kliknij przycisk "Pokaż więcej" tak długo, jak jest dostępny
click_show_more(driver)

# Scrolluj na sam dół strony po kliknięciu "Pokaż więcej"
scroll_to_bottom(driver)

# Wywołaj funkcję i pobierz informacje o dotacjach
donations_info = scrape_donations_info(driver)

# Zamień listę słowników na DataFrame Pandas
df = pd.DataFrame(donations_info)

# Zapisz DataFrame do pliku CSV
df.to_csv('donations_data.csv', index=False, mode='a')

# Dodatkowe działania, jeśli są potrzebne

# Zatrzymaj okno przeglądarki otwarte do momentu wprowadzenia danych przez użytkownika
input("Naciśnij Enter, aby zamknąć przeglądarkę...")

# Wyskakuje error przy tym pierwszym :/
# Traceback (most recent call last):
#   File "C:\Users\marci\Documents\GitHub\Ekipa-Fantasy-X-Stream-Charytatywny\Data\scrape_data.py", line 90, in <module>
#     donations_info = scrape_donations_info(driver)
#   File "C:\Users\marci\Documents\GitHub\Ekipa-Fantasy-X-Stream-Charytatywny\Data\scrape_data.py", line 52, in scrape_donations_info
#     amount = donation_element.find_element(By.XPATH, ".//span[@class='sc-hhpBdf bVGfl']").text
#   File "C:\Users\marci\AppData\Local\Programs\Python\Python39\lib\site-packages\selenium\webdriver\remote\webelement.py", line 90, in text
#     return self._execute(Command.GET_ELEMENT_TEXT)["value"]
#   File "C:\Users\marci\AppData\Local\Programs\Python\Python39\lib\site-packages\selenium\webdriver\remote\webelement.py", line 395, in _execute
#     return self._parent.execute(command, params)
#   File "C:\Users\marci\AppData\Local\Programs\Python\Python39\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 348, in execute
#     self.error_handler.check_response(response)
#   File "C:\Users\marci\AppData\Local\Programs\Python\Python39\lib\site-packages\selenium\webdriver\remote\errorhandler.py", line 229, in check_response
#     raise exception_class(message, screen, stacktrace)
# selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found