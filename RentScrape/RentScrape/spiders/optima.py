import datetime
import json
import os
import pandas as pd
import scrapy


class OptimaSpider(scrapy.Spider):
    name = "Optima"
    start_urls = ["https://sightmap.com/app/api/v1/z40vlqnwle5/sightmaps/197"]

    def __init__(self, name = None, **kwargs):
        super().__init__(name, **kwargs)
        self.drop_path = f"{os.getcwd()}/drop/optima/{datetime.datetime.now().strftime('%Y-%m-%d')}"
        if not os.path.exists(self.drop_path):
            os.mkdir(self.drop_path)

    def parse(self, response):
        my_dict = response.json()
        with open(f"{self.drop_path}/infos.json", "w") as f:
            f.write(json.dumps(my_dict))

