from playwright.async_api import async_playwright
import asyncio
import csv
import re
from bs4 import BeautifulSoup
import os

def sanitize_filename(filename):
    # Remove or replace invalid characters
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

async def close_pop_up_if_present(page):
    try:
        # Wait for the pop-up button to appear
        await page.wait_for_selector('button[aria-label="Close"]', timeout=2500)
        close_pop_up = await page.query_selector('button[aria-label="Close"]')
        if close_pop_up:
            await close_pop_up.click()
            await page.wait_for_timeout(1000)  
    except:
        print("No pop-up element found.")

async def main():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        
        # Create context with viewport size set to large dimensions
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        
        # Open a new page
        page = await context.new_page()
        
        # Navigate to the URL
        await page.goto("https://www.airbnb.com/s/San-Francisco--California--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&query=San%20Francisco%2C%20California%2C%20United%20States&place_id=ChIJIQBpAG2ahYAR_6128GcTUEo&date_picker_type=calendar&checkin=2024-05-08&checkout=2024-05-22&source=structured_search_input_header&search_type=autocomplete_click")

        # Wait for the page to load
        await page.wait_for_timeout(4000)

        # Accept cookies if the button is present
        try:
            accept_cookies = await page.query_selector('button:has-text("Accept")')
            if accept_cookies:
                await accept_cookies.click()
        except Exception as e:
            print(f"No 'Accept cookies' button found: {e}")

        page_counter = 0
        apartment_counter = 0

        with open('london_playwright.csv', 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Apartment Name", "Short Description", "Rooms and Bathrooms", "Price per Night", "Host Name", "Account Active Since", "Guest favourite stars", "Guest favourite reviews"])

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

                        # Wait for the new page to load
                        await page.wait_for_timeout(4000)

                        # Switch to the newly opened tab
                        new_page = context.pages[-1]

                        # Close pop-up if it appears
                        await close_pop_up_if_present(new_page)

                        # Scrape data from the new page
                        page_source = await new_page.content()
                        soup = BeautifulSoup(page_source, "html.parser")

                        # Extract data from the page
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

                        try:
                            guest_favourite_stars = soup.find('div', class_='a8jhwcl').get_text()
                            guest_favourite_stars = re.search(r'\d+\.\d+', guest_favourite_stars).group()
                        except AttributeError:
                            guest_favourite_stars = "Not guest favourite"

                        try:
                            guest_favourite_reviews = soup.find('div', class_='r16onr0j').get_text()
                        except AttributeError:
                            guest_favourite_reviews = "Not guest favourite"

                        # Write data to CSV file
                        csv_writer.writerow([apartment_name, short_description, rooms_bathrooms, price_per_night, host_name, account_active_since, guest_favourite_stars, guest_favourite_reviews])

                        # Sanitize the apartment name for use in a filename
                        sanitized_apartment_name = sanitize_filename(apartment_name)

                        # Ensure the directory exists
                        os.makedirs('screenshots_london_playwright', exist_ok=True)

                        # Take a screenshot
                        await new_page.screenshot(path=f'screenshots_london_playwright/{sanitized_apartment_name}.png')

                        # Close the current tab
                        await new_page.close()

                        # Switch back to the main tab
                        page = context.pages[0]

                except Exception as e:
                    print("Error occurred:", e)
                    break

                # Move to the next page
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

# Run the script
asyncio.run(main())
