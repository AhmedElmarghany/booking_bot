# This file is going to include method that will parse
# The specific data that we need from each one of the deal boxes.

from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from prettytable import PrettyTable
import pandas as pd
import openpyxl

class BookingReport:
    def __init__(self, source_page):
        self.page = source_page
        self.soup = self.soup_page()
        self.deal_boxes = self.pull_deal_boxes()
        self.data = self.pull_data()

    def soup_page(self):
        return BeautifulSoup(self.page, "lxml")
    
    def pull_deal_boxes(self):
        return self.soup.find_all('div', {"class": "da89aeb942"})
    

    def pull_data(self):
        collection = []
        for deal_box in self.deal_boxes:
            hotel_name = deal_box.find("div",{"class": "a23c043802"}).text.strip()
            try:
                price = deal_box.find("span",{"data-testid": "price-and-discounted-price"}).text.strip()
            except:
                price = "Not priced"
            try:
                rating = deal_box.find("div", {"class": "d86cee9b25"}).text.strip()
            except:
                rating = "not rated"
            collection.append([hotel_name, price, rating])
        return collection
    
    def create_cls_tables(self):
        data = self.data
        table = PrettyTable(
            field_names=['Hotel Name', "Price", "Rating"]
        )
        table.add_rows(data)
        print(table)
    
    def append_to_csv(self):
        csv_file = pd.read_csv(r"C:\Users\Ahmad\Desktop\projects\booking bot v 1.1\booking\final\Hotels.csv", index_col=0)
        data = self.data
        for hotel in data:
            new_record = pd.DataFrame({"Hotel name": [hotel[0]],
                                       "Price": [hotel[1]],
                                       "Rating": [hotel[2]]})
            csv_file = pd.concat([csv_file, new_record], ignore_index=True)
        csv_file.to_csv(r"C:\Users\Ahmad\Desktop\projects\booking bot v 1.1\booking\final\Hotels.csv")

    def convert_to_excel(self):
        csv_file = pd.read_csv(r"C:\Users\Ahmad\Desktop\projects\booking bot v 1.1\booking\final\Hotels.csv", index_col=0)
        writer = pd.ExcelWriter(r"C:\Users\Ahmad\Desktop\projects\booking bot v 1.1\booking\final\hotels.xlsx")
        csv_file.to_excel(writer)
        writer.save()