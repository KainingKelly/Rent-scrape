import datetime
import os

import pandas as pd
import scrapy


class OneChicagoTransform:
    def __init__(self, drop_path = None) -> None:
        self.drop_path = drop_path if drop_path else f"{os.getcwd()}/RentScrape/drop/onechicago/{datetime.datetime.now().strftime('%Y-%m-%d')}/"

    def grab_files(self) ->list[pd.DataFrame]:
        files = [file.path for file in os.scandir(self.drop_path) if file.is_file()]
        unit_files = [file for file in files if "unit" in file]
        floorplan_files = [file for file in files if "frontpage" in file]
        return [pd.concat([self.transform_units(unit) for unit in unit_files]), pd.concat([self.transform_floorplan(fp) for fp in floorplan_files])]
    
    def transform_units(self, unit_file) -> pd.DataFrame:
        with open(unit_file, "r") as f:
            response = scrapy.Selector(text=f.read())
        units = response.xpath('//tr[contains(@class,"unit-availability__row")]')
        floorplan = response.xpath('//div[contains(@class,"unit-availability__info-col")]/text()').getall()[1]
        building = response.xpath('//a[contains(@href, "/buildings/")]/text()').get()
        unit_details = []
        for unit in units:
            infos = unit.xpath('.//td/text()').getall()
            if not infos:
                continue
            room_number = infos[0]
            rent = infos[1]
            available = infos[2]

            unit_details.append({
            "unit_number":room_number,
            'as_of':datetime.date.today(),
            'floorplan': floorplan,
            'price': rent,
            'date_available': available,
            'building': building
            })
        return pd.DataFrame(unit_details)
    
    def transform_floorplan(self, floorplan_file) -> pd.DataFrame:
        with open(floorplan_file, 'r') as f:
            response = scrapy.Selector(text=f.read())
        floorplans = response.xpath('//tr[contains(@class,"unit-list__row")]')
        floor_plan_details = []
        for floorplan in floorplans:
            building=floorplan.xpath('.//td[1]/a/text()').get()
            if not building:
                continue
            img = floorplan.xpath('.//img/@src').get()
            room=floorplan.xpath('.//td[2]/text()').get()
            description=floorplan.xpath('.//td[contains(@class, "unit-list__col--rooms")]/text()').get().strip()
            size=floorplan.xpath('.//td[contains(@class, "unit-list__col--sf")]/text()').get().strip().replace('"', "")

            fp = {
                "name":room,
                "beds": description.split("/")[0].strip(),
                "baths": description.split("/")[1].strip(),
                "size": size,
                "img_path": img,
                "building": building
            }

            floor_plan_details.append(fp)

        return pd.DataFrame(floor_plan_details)
