#This file will include a class with instance methods.
#That will be responsible to intract with our website
#After we have some results, to apply filtrations.
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

class BookingFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver
    
    def apply_star_rating(self, *star_value):
        for star in star_value:
            star_element = self.driver.find_element(By.XPATH, f"//div[text()='{star} stars']")
            star_element.click()