import datetime
import json
import os
import pandas as pd
import scrapy


class AquaSpider(scrapy.Spider):
    name="Aqua"
    start_urls=["https://doorway-api.knockrentals.com/v1/property/2028221/units"]

    def __init__(self, name = None, **kwargs):
        super().__init__(name, **kwargs)
        self.drop_path = f"{os.getcwd()}/drop/aqua/{datetime.datetime.now().strftime('%Y-%m-%d')}"
        if not os.path.exists(self.drop_path):
            os.mkdir(self.drop_path)

    def parse(self, response):
        # print(f'\n\nResponse: {response.json()}\n\n')
        my_dict = response.json()
        with open(f"{self.drop_path}/infos.json","w") as f:
            f.write(json.dumps(my_dict))
        