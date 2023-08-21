import time
import booking.constants as const
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from booking.booking_filtrations import BookingFiltration
from booking.booking_report import BookingReport


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\webdrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(5)
        self.maximize_window()

    def __exit__(self, exc_type, exc, traceback):
        if self.teardown:
            self.quit()
   
    def land_first_page(self):
        self.get(const.BASE_URL)
        try:
            close_ad = self.find_element(By.CSS_SELECTOR, "#b2indexPage > div.b9720ed41e.cdf0a9297c > div > div > div > div.dd5dccd82f > div.ffd93a9ecb.dc19f70f85.eb67815534.e91f709929 > div > button")
            close_ad.click()
        except:
            pass

    def change_currency(self, currency):
        currency_element = self.find_element(By.CSS_SELECTOR, "#b2indexPage > div:nth-child(4) > div > header > nav.c20fd9b542 > div.aca0ade214.aaf30230d9.c2931f4182.e7d9f93f4d.faf8b5d9a5 > span:nth-child(1) > button")
        currency_element.click()
        selected_currency_element = self.find_element(By.XPATH, f"//div[ text() = '{currency}' ]")
        selected_currency_element.click()
        
    def select_place_to_go(self, place_to_go:str):
        search_field = self.find_element(By.CSS_SELECTOR, "input[name = 'ss']")
        search_field.clear()
        search_field.send_keys(place_to_go)
        WebDriverWait(self, 15).until(
            EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#indexsearch > div.hero-banner-searchbox > div > form > div.ffb9c3d6a3.db27349d3a.cc9bf48a25 > div:nth-child(1) > div > div > div.a7631de79e > div > ul > li:nth-child(1) > div > div > div > div.a3332d346a"),
              str(place_to_go)
            )
        )
        first_result = self.find_element(By.CSS_SELECTOR, "#indexsearch > div.hero-banner-searchbox > div > form > div.ffb9c3d6a3.db27349d3a.cc9bf48a25 > div:nth-child(1) > div > div > div.a7631de79e > div > ul > li:nth-child(1) > div > div > div > div.a3332d346a")
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        current_date = self.find_element(By.CSS_SELECTOR, "#calendar-searchboxdatepicker > div > div.a10b0e2d13.efea941f13 > div > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(2) > span").get_attribute("data-date")
        next_month_button = self.find_element(By.CSS_SELECTOR, "#calendar-searchboxdatepicker > div > div.a10b0e2d13.efea941f13 > button")
        # CHECK_IN
        # year
        if int(check_in_date[:4]) > int(current_date[:4]):
            while int(check_in_date[:4]) != int(current_date[:4]):
                next_month_button.click()
                current_date = self.find_element(By.CSS_SELECTOR, "#calendar-searchboxdatepicker > div > div.a10b0e2d13.efea941f13 > div > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(2) > span").get_attribute("data-date")
        # month
        if int(check_in_date[5:7]) > int(current_date[5:7]):
            while int(check_in_date[5:7]) != int(current_date[5:7]):
                next_month_button.click()
                current_date = self.find_element(By.CSS_SELECTOR, "#calendar-searchboxdatepicker > div > div.a10b0e2d13.efea941f13 > div > div:nth-child(1) > table > tbody > tr:nth-child(4) > td:nth-child(5) > span").get_attribute("data-date")
        # day
        check_in_element = self.find_element(By.CSS_SELECTOR, f"span[data-date = '{check_in_date}']")
        check_in_element.click()
        
        # CHECK_OUT
        # year
        current_date = self.find_element(By.CSS_SELECTOR, "#calendar-searchboxdatepicker > div > div.a10b0e2d13.efea941f13 > div > div:nth-child(2) > table > tbody > tr:nth-child(3) > td:nth-child(3) > span").get_attribute("data-date")
        if int(check_out_date[:4]) > int(current_date[:4]):
            while int(check_out_date[:4]) != int(current_date[:4]):
                next_month_button.click()
                current_date = self.find_element(By.CSS_SELECTOR, "#calendar-searchboxdatepicker > div > div.a10b0e2d13.efea941f13 > div > div:nth-child(2) > table > tbody > tr:nth-child(3) > td:nth-child(3) > span").get_attribute("data-date")
        # month
        if int(check_out_date[5:7]) > int(current_date[5:7]):
            while int(check_out_date[5:7]) != int(current_date[5:7]):
                next_month_button.click()
                current_date = self.find_element(By.CSS_SELECTOR, "#calendar-searchboxdatepicker > div > div.a10b0e2d13.efea941f13 > div > div:nth-child(2) > table > tbody > tr:nth-child(3) > td:nth-child(3) > span").get_attribute("data-date")
        # day
        check_out_element = self.find_element(By.CSS_SELECTOR, f"span[data-date = '{check_out_date}']")
        check_out_element.click()

    def select_adults(self, count=1):
        select_adults_field = self.find_element(By.CSS_SELECTOR, "button.b7d08821c3")
        select_adults_field.click()
        adults_count = self.find_element(By.CSS_SELECTOR, "input.ebb9f563b4").get_attribute("value") # default = 2
        decrease_adults_button = self.find_element(By.CSS_SELECTOR, "#indexsearch > div.hero-banner-searchbox > div > form > div.ffb9c3d6a3.db27349d3a.cc9bf48a25 > div:nth-child(3) > div > div > div > div > div:nth-child(1) > div.bfb38641b0 > button.a83ed08757.c21c56c305.f38b6daa18.d691166b09.ab98298258.deab83296e.bb803d8689.e91c91fa93")
        increase_adults_button = self.find_element(By.CSS_SELECTOR, "#indexsearch > div.hero-banner-searchbox > div > form > div.ffb9c3d6a3.db27349d3a.cc9bf48a25 > div:nth-child(3) > div > div > div > div > div:nth-child(1) > div.bfb38641b0 > button.a83ed08757.c21c56c305.f38b6daa18.d691166b09.ab98298258.deab83296e.bb803d8689.f4d78af12a")
        if count > int(adults_count):
            for _ in range(count - int(adults_count)):
                increase_adults_button.click()
        elif count < int(adults_count):
            for _ in range(int(adults_count) - count):
                decrease_adults_button.click()

    def select_children(self, count=0, ages=[]):
        select_children_field = self.find_element(By.CSS_SELECTOR, "button.b7d08821c3")
        select_children_field.click()
        increase_children_button = self.find_element(By.CSS_SELECTOR, "div.df856d97eb  div.b2b5147b20:nth-of-type(2)  button:nth-of-type(2)")
        for i in range(count):
            increase_children_button.click()
            age_needed = self.find_elements(By.CSS_SELECTOR, f"div[data-testid='kids-ages'] select[name='age']")
            age_needed[i].click()
            child_age = self.find_elements(By.CSS_SELECTOR, f"div[data-testid='kids-ages'] select[name='age']:last-of-type  option[value='{ages[i]}']")
            child_age[i].click()

    def select_rooms(self, count=1):
        select_rooms_field = self.find_element(By.CSS_SELECTOR, "button.b7d08821c3")
        select_rooms_field.click()
        increase_rooms_button = self.find_element(By.CSS_SELECTOR, "div.df856d97eb  div.b2b5147b20:last-of-type  button:nth-of-type(2)")
        for i in range(count - 1):
            increase_rooms_button.click()
        time.sleep(1)
        done_button = self.find_element(By.CSS_SELECTOR, "div.a5da3001f3 > button.d285d0ebe9")
        done_button.click()
    
    def travel_for_work(self,answer=False):
        if answer:
            selection_button = self.find_elements(By.CSS_SELECTOR, "span.aacd9d0b0a")
            selection_button[-1].click()

    def show_vacation_rentals(self,answer=False):
        if answer:
            selection_button = self.find_elements(By.CSS_SELECTOR, "span.aacd9d0b0a")
            selection_button[0].click()

    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR, "button.aa11d0d5cd")
        search_button.click()

    def next_page(self):
        next_button = self.find_element(By.CSS_SELECTOR, "button[aria-label='Next page']")
        WebDriverWait(self, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Next page']"))
            )
        next_button.click()


    def apply_filterations(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(5)

    """
    def report_results(self):
        hotels_section = self.find_element(By.CSS_SELECTOR, "div.d4924c9e74")
        report = BookingReport(hotels_section)
        report.create_cls_tables()
        print("Pulling data to csv file...")
        report.append_to_csv()
        print("Adding data to Excel sheet...")
        report.convert_to_excel()
        print("Done!")
    """
    def report_results(self):
        source_page = self.page_source
        report = BookingReport(source_page)
        report.create_cls_tables()
        print("Pulling data to csv file...")
        report.append_to_csv()
        print("Adding data to Excel sheet...")
        report.convert_to_excel()
        print("Done!")