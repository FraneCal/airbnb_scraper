# Program otvori stranicu od smjestaja uzme sve podatke (+ screenshot ) i zatvori tab, zatim ide na sljedeci smjestaj i nakon toga ide na sljedecu stranicu

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

URL = "https://www.airbnb.com/s/San-Francisco--California--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&query=San%20Francisco%2C%20California%2C%20United%20States&place_id=ChIJIQBpAG2ahYAR_6128GcTUEo&date_picker_type=calendar&checkin=2024-05-08&checkout=2024-05-22&source=structured_search_input_header&search_type=autocomplete_click"

driver = webdriver.Chrome()
driver.get(URL)
driver.maximize_window()

time.sleep(4)

# Handle cookies
try:
    accept_cookies = driver.find_element(By.XPATH, '//*[@id="react-application"]/div/div/div[1]/div/div[6]/section/div[2]/div[2]/button')
    accept_cookies.click()
except NoSuchElementException:
    print("No 'Accept cookies' found.")

apartment = driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[2]/div/div/div/div/div[1]/div[1]/div/div[2]/div/div/div/div/div/div[1]/div/div/div[2]/div/div/div/div/a[1]')
apartment.click()

# Switch to the newly opened tab
driver.switch_to.window(driver.window_handles[-1])

time.sleep(4)

page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")

try:
    close_pop_up = driver.find_element(By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[1]/button')
    close_pop_up.click()
except NoSuchElementException:
    print("No pop up element found.")

time.sleep(1)

apartment_name = soup.find('h1', class_='hpipapi').getText()
short_description = soup.find('h2', class_='hpipapi').getText()
rooms_bathrooms = soup.find('div', class_='o1kjrihn').getText()
price_per_night = soup.find('span', class_='_1y74zjx').getText()
host_name = soup.find('div', class_='cm0tib6').find('div', class_='t1pxe1a4').getText().split(' ')[2]

# POPRAVIT ACCOUNT ACTIVE SINCE
#account_active_since = soup.find('div', class_='cm0tib6').find('li', class_='l7n4lsf')
account_active_since = soup.find('li', class_='l7n4lsf').find_next_sibling('li').getText()

driver.execute_script(f"window.scrollTo(0, 100);")

driver.save_screenshot(f'screenshots/{apartment_name.replace(" ", "_")}.png')

print(apartment_name)
print(short_description)
print(rooms_bathrooms)
print(price_per_night)
print(host_name)
print(account_active_since)

# Close the current tab
driver.close()

# Switch back to the main tab
driver.switch_to.window(driver.window_handles[0])

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

time.sleep(2)

driver.quit()
