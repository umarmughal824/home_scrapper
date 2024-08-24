import time
from selenium.webdriver.common.by import By
from itertools import cycle

from hotel_scrapper.webdriver_utils import get_webdriver
from hotel_scrapper.csv_utils import save_to_csv


class Scraper:
    def __init__(self, proxies=None):
        self.proxies = proxies if proxies else []
        self.proxy_pool = cycle(self.proxies)
        self.category_urls = []

    def scrape_url(self, url):
        proxy = None  # You can replace this with `next(self.proxy_pool)` if proxies are used
        print(f"Using proxy: {proxy}")
        driver = get_webdriver(proxy)

        try:
            driver.get(url)
            driver.implicitly_wait(10)
            categories = driver.find_elements(By.CSS_SELECTOR,
                                              "main section div.flex div.relative div.absolute div.relative ul.w-max "
                                              "> li > a")
            for index, category in enumerate(categories, start=1):
                self.category_urls.append(category.get_attribute('href'))
        except Exception as e:
            print(f"Error with proxy {proxy}: {e}")
        finally:
            driver.quit()

    def get_room_details(self, room):
        room_section = room.find_elements(By.TAG_NAME, "div")
        points = room_section[0].find_elements(By.TAG_NAME, "div")[0].text
        pricing_section = room_section[0].find_element(By.XPATH, './span[1]').text.replace("\n", "")
        return points, pricing_section

    def get_room_prices(self, name, location, ratings, room_type, room):
        room_type_details = room_type.find_elements(By.TAG_NAME, "li")
        category = room_type_details[0].text
        category_details = room_type_details[1].text

        room_details = room.find_elements(By.TAG_NAME, "li")
        for room_detail in room_details:
            points, pricing = self.get_room_details(room_detail)
            save_to_csv(name, location, ratings, category, category_details, points, pricing)

    def get_hotel_details(self, hotel):
        try:
            details = hotel.find_elements(By.CSS_SELECTOR, "div.w-\\[630px\\] a")
            name = details[0].find_element(By.CSS_SELECTOR, "h2[itemprop='name']").text
            location = details[0].find_element(By.CSS_SELECTOR, "p").text

            ratings = details[1].text.replace("\n", "")

            room_types = hotel.find_elements(By.CSS_SELECTOR, "ul.mr-2\\.5")
            rooms = hotel.find_elements(By.CSS_SELECTOR, "ul.w-3\\/5")

            for counter in range(len(rooms)):
                if counter == 10:
                    break
                self.get_room_prices(name, location, ratings, room_types[counter], rooms[counter])

        except Exception as e:
            print(f"Error {e}")

    def scrape_category_url(self, url):
        proxy = None  # Get the next proxy from the pool
        print(f"Using proxy: {proxy}")
        driver = get_webdriver(proxy)
        # driver = get_webdriver()

        try:
            driver.get(url)
            driver.implicitly_wait(10)

            # open all the rooms section
            view_all_rooms = driver.find_elements(By.CSS_SELECTOR,
                                                  "section .relative section > div.relative div.flex button")
            for view_all_room in view_all_rooms:
                try:
                    view_all_room.click()
                except Exception as e:
                    print(f"Error in the button click: {e}")
            # fetch the hotel details
            hotels = driver.find_elements(By.CSS_SELECTOR, "section.relative[itemprop='itemListElement']")
            for hotel in hotels:
                self.get_hotel_details(hotel)

        except Exception as e:
            print(f"Error with proxy {proxy}: {e}")
        finally:
            driver.quit()  # Close the browser session

    def run(self, urls):
        for url in urls:
            self.scrape_url(url)
            time.sleep(3)  # Optional: Add a delay between requests to avoid detection
            if self.category_urls:
                for category_url in self.category_urls:
                    self.scrape_category_url(category_url)
