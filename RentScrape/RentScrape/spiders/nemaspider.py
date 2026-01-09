import datetime
import os
import scrapy


class NemaSpider(scrapy.Spider):
    name = "Nema"
    start_urls = ["https://www.rentnemachicago.com/availability"]

    def __init__(self):
        self.drop_path = f"{os.getcwd()}/drop/nema/{datetime.datetime.now().strftime('%Y-%m-%d')}"
        os.makedirs(self.drop_path, exist_ok = True)

    def parse(self, response):
        with open(f"{self.drop_path}/availability.html","w") as f:
            f.write(response.text)
