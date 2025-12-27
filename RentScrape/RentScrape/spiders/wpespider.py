from collections.abc import Iterable
import datetime
import os
from typing import Any
import scrapy
import pandas as pd


class WolfPointEastSpider(scrapy.Spider):
    name="WolfPointEast" # scrapy crawl WolfPointEast
    start_urls = ["https://wolfpointeast.com/floor-plans"]

    def __init__(self, name: str | None = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.drop_path = f"{os.getcwd()}/drop/{datetime.datetime.now().strftime('%Y-%m-%d')}"
        if not os.path.exists(self.drop_path):
            os.mkdir(self.drop_path)
        self.floor_plan_page = 0 # counter
        self.unit_page = 0 # counter


    def parse(self, response):
        with open(f"{self.drop_path}/floorplan_page_{self.floor_plan_page}.html", "w") as f:
            f.write(response.text)
        self.floor_plan_page += 1

        floor_plan_urls = response.xpath('//a[@class="plan-img"]/@href').getall()
            
        # Scrape unit information
        for url in floor_plan_urls:
            if url:
                yield response.follow(url, self.parse_units)    
        
        # Scrape the next page too
        next_url = response.xpath('//a[span[@class="link_arrow"]]/@href').get()
        if next_url:
            yield response.follow(next_url, self.parse)

    def parse_units(self, response):
        with open(f"{self.drop_path}/unit_page_{self.unit_page}.html", "w") as f:
            f.write(response.text)
        self.unit_page += 1