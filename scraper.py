from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time
import re

URL = "https://www.airbnb.com/s/San-Francisco--California--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&query=San%20Francisco%2C%20California%2C%20United%20States&place_id=ChIJIQBpAG2ahYAR_6128GcTUEo&date_picker_type=calendar&checkin=2024-05-08&checkout=2024-05-22&source=structured_search_input_header&search_type=autocomplete_click"

driver = webdriver.Chrome()
driver.get(URL)
driver.maximize_window()

time.sleep(4)

try:
    accept_cookies = driver.find_element(By.XPATH, '//*[@id="react-application"]/div/div/div[1]/div/div[6]/section/div[2]/div[2]/button')
    accept_cookies.click()
except NoSuchElementException:
    print("No 'Accept cookies' found.")

elements = driver.find_elements(By.XPATH, "//div[@id='site-content']//div[@data-testid='card-container']//div[@class = ' dir dir-ltr']//a[1]")

while True:
    try:
        for element in elements:
            try:
                element.click()
            except StaleElementReferenceException:
                print("No more elements to click.")
                break

            # Switch to the newly opened tab
            driver.switch_to.window(driver.window_handles[-1])

            time.sleep(4)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            try:
                close_pop_up = driver.find_element(By.XPATH,
                                                   '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[1]/button')
                close_pop_up.click()
            except NoSuchElementException:
                print("No pop up element found.")

            try:
                apartment_name = soup.find('h1', class_='hpipapi').getText()
            except AttributeError:
                apartment_name = "Name not specified"

            try:
                short_description = soup.find('h2', class_='hpipapi').getText()
            except AttributeError:
                short_description = "Description not specifed"

            try:
                rooms_bathrooms = soup.find('div', class_='o1kjrihn').getText()
            except AttributeError:
                rooms_bathrooms = "Utilities not specified"

            try:
                price_per_night = soup.find('span', class_='_1y74zjx').getText()
            except AttributeError:
                price_per_night = "Price not specified"

            try:
                host_name = soup.find('div', class_='cm0tib6').find('div', class_='t1pxe1a4').getText()
            except (AttributeError, IndexError):
                host_name = "Host name not specified"

            # popravit account_active
            try:
                account_active_since = soup.find('li', class_='l7n4lsf atm_9s_1o8liyq_keqd55 dir dir-ltr').getText()
            except AttributeError:
                account_active_since = "Active since not specified"

            try:
                guest_favourite_stars = soup.find('div', class_='a8jhwcl').getText()
                guest_favourite_stars = re.search(r'\d+\.\d+', guest_favourite_stars).group()
            except AttributeError:
                guest_favourite_stars = "Not guest favourite"

            try:
                guest_favourite_reviews = soup.find('div', class_='r16onr0j').getText()
            except AttributeError:
                guest_favourite_reviews = "Not guest favourite"

            print("Apartment Name:", apartment_name)
            print("Short Description:", short_description)
            print("Rooms and Bathrooms:", rooms_bathrooms)
            print("Price per Night:", price_per_night)
            print("Host Name:", host_name)
            print("Account Active Since:", account_active_since)
            print("Guest favourite stars:", guest_favourite_stars)
            print("Guest favourite reviews:", guest_favourite_reviews)

            time.sleep(1)

            driver.execute_script(f"window.scrollTo(0, 100);")

            driver.save_screenshot(f'screenshots/{apartment_name.replace(" ", "_")}.png')

            # Close the current tab
            driver.close()

            time.sleep(1)

            # Switch back to the main tab
            driver.switch_to.window(driver.window_handles[0])

    except NoSuchElementException:
        print("No more elements to click. Heading to the next page.")

    try:
        next_page = driver.find_element(By.XPATH, '//*[@id="site-content"]/div/div[3]/div/div/div/nav/div/a[5]')
        next_page.click()
        time.sleep(2)

    except NoSuchElementException:
        print("No more pages to click.")
        break

    elements = driver.find_elements(By.XPATH, "//div[@id='site-content']//div[@data-testid='card-container']//div[@class = ' dir dir-ltr']//a[1]")

driver.quit()
