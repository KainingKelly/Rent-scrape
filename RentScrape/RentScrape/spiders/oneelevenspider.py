import datetime
import os
from typing import Any
import scrapy


class OneElevenSpider(scrapy.Spider):
    name = "OneEleven"
    start_urls = ["https://www.oneelevenchicago.com/floor-plans/"]

    def __init__(self):
        self.drop_path = f"{os.getcwd()}/drop/oneeleven/{datetime.datetime.now().strftime('%Y-%m-%d')}"
        if not os.path.exists(self.drop_path):
            os.mkdir(self.drop_path)
        self.floor_plan_page = 0


    def parse(self, response):
        with open(f"{self.drop_path}/floorplan_page_{self.floor_plan_page}.html","w") as f:
            f.write(response.text)
        self.floor_plan_page += 1

        nextpage_url=response.xpath('//a[contains(@class,"mt_pag_right")]/@href').get()
        if nextpage_url and "https" in nextpage_url:
            yield response.follow(nextpage_url, self.parse)