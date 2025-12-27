import datetime
import os

import pandas as pd
import scrapy


class WolfPointEastTransform:
    def __init__(self, drop_path = None) -> None:
        self.drop_path = drop_path if drop_path else f"{os.getcwd()}/drop/{datetime.datetime.now().strftime('%Y-%m-%d')}/"

    def grab_files(self) -> list[pd.DataFrame]:
        files = [file.path for file in os.scandir(self.drop_path) if file.is_file()]
        unit_files = [file for file in files if "unit" in file]
        floorplan_files = [file for file in files if "floorplan" in file]
        return [pd.concat([self.transform_units(unit) for unit in unit_files]), pd.concat([self.transform_floorplans(fp) for fp in floorplan_files])]

    def transform_units(self, unit_file) -> pd.DataFrame:
        with open(unit_file, "r") as f:
            response = scrapy.Selector(text=f.read())
        units = response.xpath('//div[contains(@class, "plan-details")]')
        unit_details = []
        for unit in units:
            number = unit.xpath('.//h2[span]/span/text()').get()
            floorplan = unit.xpath('.//h3[span]/span/text()').get()
            infos = unit.xpath('.//li[span]/span/text()').getall()
            price = infos[0].strip()
            available = infos[1].strip()

            unit_details.append({
                'unit_number': number,
                'as_of': datetime.date.today(),
                'floorplan': floorplan,
                'price': price,
                'date_available': available
            })
        return pd.DataFrame(unit_details)

    def transform_floorplans(self, floorplan_file) -> pd.DataFrame:
        with open(floorplan_file, 'r') as f:
            response = scrapy.Selector(text=f.read())
        floorplans = response.xpath('//div[contains(@class, "result-box")]')
        floor_plan_details = []
        for floorplan in floorplans:
            name = floorplan.xpath('.//h2/span/text()').get()
            infos = floorplan.xpath('.//li/text()').getall()
            rooms_descriptor = infos[0].strip().replace("\t","").replace("\n","").replace("B", " B").replace(" /", "/")
            beds = rooms_descriptor.split("/")[0]
            baths = rooms_descriptor.split("/")[1]
            size = infos[1].strip().replace("\t","").replace("\n","").replace("SQ.FT.", "")
            img = floorplan.xpath('.//img/@src').get()

            floor_plan_details.append({
                'name': name, 
                'beds': beds, 
                'baths': baths,
                'size': size,
                'img_path': img
                })
        return pd.DataFrame(floor_plan_details)