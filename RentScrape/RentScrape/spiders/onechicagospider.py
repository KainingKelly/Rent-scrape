import datetime
import os
from typing import Any
import scrapy


class OneChicagoSpider(scrapy.Spider):
    name = "OneChicago"
    start_urls = ["https://liveonechicago.com/floor-plans"]

    def __init__(self, name: str | None = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.drop_path = f"{os.getcwd()}/drop/onechicago/{datetime.datetime.now().strftime('%Y-%m-%d')}"
        if not os.path.exists(self.drop_path):
            os.mkdir(self.drop_path)
        self.floor_plan_page = 0
        self.unit_page = 0


    def parse(self, response):
        with open(f"{self.drop_path}/frontpage.html","w") as f:
            f.write(response.text)

        fp_uris= response.xpath('//button/@data-view-url').getall()
        floor_plan_urls = [f"https://liveonechicago.com{fp_uri}" for fp_uri in fp_uris if fp_uri]

        # Scrape unit information
        for url in floor_plan_urls:
            if url:
                yield response.follow(url, self.parse_units)

    def parse_units(self, response):
        with open(f"{self.drop_path}/unit_page_{self.unit_page}.html","w") as f:
            f.write(response.text)
        self.unit_page += 1


        


        
