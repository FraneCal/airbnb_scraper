import asyncio
import csv
import re
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import os

# Function to process rooms and bathrooms
def process_rooms_bathrooms(room_bathroom_str):
    guest_number = "Not specified"
    bedroom_number = "Not specified"
    bed_number = "Not specified"
    bath_number = "Not specified"
    
    if room_bathroom_str:
        parts = [part.strip() for part in room_bathroom_str.split("·")]
        for part in parts:
            if "guest" in part:
                guest_number = part.split()[0]
            elif "bedroom" in part:
                bedroom_number = part.split()[0]
            elif "bed" in part:
                bed_number = part.split()[0]
            elif "bath" in part:
                bath_number = part.split()[0]
                
    return guest_number, bedroom_number, bed_number, bath_number

# Sanitize filename
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Extract city name from URL
def extract_city_from_url(url):
    match = re.search(r'/s/([^/]+?)(--|%2C)', url)
    if match:
        return match.group(1).replace('--', ' ').replace('%2C', ' ')
    return "unknown_city"

# Close pop-up if present
async def close_pop_up_if_present(page):
    try:
        await page.wait_for_selector('button[aria-label="Close"]', timeout=2500)
        close_pop_up = await page.query_selector('button[aria-label="Close"]')
        if close_pop_up:
            await close_pop_up.click()
            await page.wait_for_timeout(1000)
    except:
        print("No pop-up element found.")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        
        url = "https://www.airbnb.com/s/London--United-Kingdom/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&query=London%2C%20United%20Kingdom&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=5&adults=1&location_bb=Qk6wez4X1FpCTYouvrPzpw%3D%3D"
        await page.goto(url)
        await page.wait_for_timeout(4000)

        city_name = extract_city_from_url(url)
        csv_filename = f'{city_name}_playwright.csv'
        screenshots_directory = f'screenshots_{city_name}_playwright'

        try:
            accept_cookies = await page.query_selector('button:has-text("Accept")')
            if accept_cookies:
                await accept_cookies.click()
        except Exception as e:
            print(f"No 'Accept cookies' button found: {e}")

        page_counter = 0
        apartment_counter = 0

        fieldnames = ['Apartment Name', 'Short Description', 'Guest Number', 'Bedroom Number', 'Bed Number', 'Bath Number', 'Price per Night', 'Host Name', 'Account Active Since']
        
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writeheader()

            while True:
                try:
                    elements = await page.query_selector_all("//div[@id='site-content']//div[@data-testid='card-container']//div[@class = ' dir dir-ltr']//a[1]")
                    for element in elements:
                        apartment_counter += 1
                        print(f"Currently at apartment number {apartment_counter}.")
                        try:
                            await element.click()
                        except Exception as e:
                            print("Error clicking element:", e)
                            continue

                        await page.wait_for_timeout(4000)
                        new_page = context.pages[-1]
                        await close_pop_up_if_present(new_page)
                        page_source = await new_page.content()
                        soup = BeautifulSoup(page_source, "html.parser")

                        try:
                            apartment_name = soup.find('h1', class_='hpipapi').get_text()
                        except AttributeError:
                            apartment_name = "Name not specified"

                        try:
                            short_description = soup.find('h2', class_='hpipapi').get_text()
                        except AttributeError:
                            short_description = "Description not specified"

                        try:
                            rooms_bathrooms = soup.find('div', class_='o1kjrihn').get_text()
                        except AttributeError:
                            rooms_bathrooms = "Utilities not specified"

                        guest_number, bedroom_number, bed_number, bath_number = process_rooms_bathrooms(rooms_bathrooms)

                        try:
                            price_per_night = soup.find('span', class_='_1y74zjx').get_text()
                        except AttributeError:
                            price_per_night = "Price not specified"

                        try:
                            host_name = soup.find('div', class_='cm0tib6').find('div', class_='t1pxe1a4').get_text()
                        except (AttributeError, IndexError):
                            host_name = "Host name not specified"

                        try:
                            account_active_since = await new_page.locator('//div[@data-section-id="HOST_OVERVIEW_DEFAULT"]//li[contains(text(), "hosting")]').text_content()
                        except Exception as e:
                            account_active_since = "Active since not specified"

                        csv_writer.writerow({
                            'Apartment Name': apartment_name,
                            'Short Description': short_description,
                            'Guest Number': guest_number,
                            'Bedroom Number': bedroom_number,
                            'Bed Number': bed_number,
                            'Bath Number': bath_number,
                            'Price per Night': price_per_night,
                            'Host Name': host_name,
                            'Account Active Since': account_active_since,
                        })

                        sanitized_apartment_name = sanitize_filename(apartment_name)
                        os.makedirs(screenshots_directory, exist_ok=True)
                        await new_page.screenshot(path=f'{screenshots_directory}/{sanitized_apartment_name}.png')
                        await new_page.close()
                        page = context.pages[0]

                except Exception as e:
                    print("Error occurred:", e)
                    break

                try:
                    page_counter += 1
                    print(f"Currently at page {page_counter}.")
                    next_page = await page.query_selector('//a[@aria-label="Next"]')
                    if next_page:
                        await next_page.click()
                        await page.wait_for_timeout(2000)
                    else:
                        print("No more pages to click.")
                        break
                except Exception as e:
                    print("Error moving to the next page:", e)
                    break

        await browser.close()

asyncio.run(main())
