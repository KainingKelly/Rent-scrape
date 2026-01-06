import datetime
import os

import pandas as pd
import scrapy


class OneElevenTransform:
    def __init__(self, drop_path = None) -> None:
        self.drop_path = drop_path if drop_path else f"{os.getcwd()}/RentScrape/drop/oneeleven/{datetime.datetime.now().strftime('%Y-%m-%d')}/"

    def grab_files(self) ->list[pd.DataFrame]:
        files = [file.path for file in os.scandir(self.drop_path) if file.is_file()]
        floorplan_files = [file for file in files if "floorplan" in file]
        floorplans_df = pd.concat([self.transform_floorplans(fp) for fp in floorplan_files])
        units_df = floorplans_df[["unit_number", "floorplan", "price", "date_available", "building"]]
        units_df["as_of"] = datetime.date.today()
        floorplans_df = floorplans_df.drop(["unit_number", "floorplan", "price", "date_available"], axis=1)
        floorplans_df = floorplans_df.drop_duplicates()
        return [units_df, floorplans_df]
    
    def transform_floorplans(self, unit_file) -> pd.DataFrame:
        with open(unit_file, "r") as f:
            response = scrapy.Selector(text=f.read())
        floorplans = response.xpath('//div[contains(@class,"mt_list_box")]')
        floor_plan_details = []

        for floorplan in floorplans:
            room_number = floorplan.xpath('.//h4[contains(@class,"mt_h4_heading")]/text()').get().strip()
            image_url = floorplan.xpath('.//img/@src').get()
            price = floorplan.xpath('.//span[contains(@class,"mt_txt_sub")]/text()').get()
            square_ft = floorplan.xpath('.//div[label/text()="SQUARE FT"]/span/text()').get().strip()
            bed = floorplan.xpath('.//div[label/text()="BEDS"]/span/text()').get().strip()
            bath = floorplan.xpath('.//div[label/text()="BATH"]/span/text()').get()
            status = floorplan.xpath('.//div[label/text()="Available"]/span/text()').get()
    

            floor_plan_details.append({
                "name": image_url,
                "beds": bed,
                "baths": bath,
                "size": square_ft,
                "img_path": image_url,
                "building": "OneEleven",
                "unit_number": room_number,
                "floorplan": image_url,
                "price": price,
                "date_available": status,
            })
        floorplans_df = pd.DataFrame(floor_plan_details)
        return floorplans_df