import csv
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# San Francisco
#URL = "https://www.airbnb.com/s/San-Francisco--California--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&query=San%20Francisco%2C%20California%2C%20United%20States&place_id=ChIJIQBpAG2ahYAR_6128GcTUEo&date_picker_type=calendar&checkin=2024-05-08&checkout=2024-05-22&source=structured_search_input_header&search_type=autocomplete_click"

# New York
#URL = 'https://www.airbnb.com/s/New-York-City--New-York--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2024-05-08&checkout=2024-05-22&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=14&query=New%20York%20City%2C%20New%20York%2C%20United%20States&place_id=ChIJOwg_06VPwokRYv534QaPC8g'

# Los Angeles
#URL = 'https://www.airbnb.com/s/Los-Angeles--California--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2024-05-08&checkout=2024-05-22&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=14&query=Los%20Angeles%2C%20California%2C%20United%20States&place_id=ChIJE9on3F3HwoAR9AhGJW_fL-I'

# Miami
#URL = 'https://www.airbnb.com/s/Miami--Florida--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2024-05-08&checkout=2024-05-22&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=14&query=Miami%2C%20Florida%2C%20United%20States&place_id=ChIJEcHIDqKw2YgRZU-t3XHylv8'

# Chicago
#URL = 'https://www.airbnb.com/s/Chicago--Illinois--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2024-05-08&checkout=2024-05-22&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=14&query=Chicago%2C%20Illinois%2C%20United%20States&place_id=ChIJ7cv00DwsDogRAMDACa2m4K8'

# Las Vegas
#URL = 'https://www.airbnb.com/s/Las-Vegas--Nevada--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2024-05-08&checkout=2024-05-22&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=14&query=Las%20Vegas%2C%20Nevada%2C%20United%20States&place_id=ChIJ0X31pIK3voARo3mz1ebVzDo'

# Paris
#URL = 'https://www.airbnb.com/s/Paris--France/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2024-05-08&checkout=2024-05-22&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=14&query=Paris%2C%20France&place_id=ChIJD7fiBh9u5kcRYJSMaMOCCwQ'

# London
URL = 'https://www.airbnb.com/s/London--United-Kingdom/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2024-05-08&checkout=2024-05-22&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=14&query=London%2C%20United%20Kingdom&place_id=ChIJdd4hrwug2EcRmSrV3Vo6llI'

# Berlin

# Barcelona



driver = webdriver.Chrome()
driver.get(URL)
driver.maximize_window()

time.sleep(4)

try:
    accept_cookies = driver.find_element(By.XPATH, '//*[@id="react-application"]/div/div/div[1]/div/div[6]/section/div[2]/div[2]/button')
    accept_cookies.click()
except NoSuchElementException:
    print("No 'Accept cookies' found.")

page_counter = 0
apartment_counter = 0
# Open CSV file in write mode
with open('london.csv', 'a', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write header row
    csv_writer.writerow(["Apartment Name", "Short Description", "Rooms and Bathrooms", "Price per Night", "Host Name", "Account Active Since", "Guest favourite stars", "Guest favourite reviews"])

    while True:
        try:
            elements = driver.find_elements(By.XPATH, "//div[@id='site-content']//div[@data-testid='card-container']//div[@class = ' dir dir-ltr']//a[1]")
            for element in elements:
                apartment_counter += 1
                print(f"Currently at apartment number {apartment_counter}.")
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

                # This variable needs to be fixed
                try:
                    account_active_since = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@data-section-id="HOST_OVERVIEW_DEFAULT"]//li[contains(text(), "hosting")]'))).text
                except NoSuchElementException:
                    print("Element not found")
                except TimeoutException:
                    print("Timeout occurred while waiting for the element")
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

                # Write data to CSV file
                csv_writer.writerow([apartment_name, short_description, rooms_bathrooms, price_per_night, host_name, account_active_since, guest_favourite_stars, guest_favourite_reviews])

                time.sleep(1)

                driver.execute_script(f"window.scrollTo(0, 100);")

                driver.save_screenshot(f'screenshots_london/{apartment_name.replace(" ", "_")}.png')

                # Close the current tab
                driver.close()

                time.sleep(1)

                # Switch back to the main tab
                driver.switch_to.window(driver.window_handles[0])

        except NoSuchElementException:
            print("No more elements to click. Heading to the next page.")

        try:
            page_counter += 1
            print(f"Currently at page {page_counter}.")
            next_page = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')
            next_page.click()
            time.sleep(2)

        except NoSuchElementException:
            print("No more pages to click.")
            break

driver.quit()
