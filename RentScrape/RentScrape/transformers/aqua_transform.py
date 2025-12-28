import datetime
import json
import os

import pandas as pd


class AquaTransform:
    def __init__(self, drop_file: str = None):
        self.drop_file = drop_file if drop_file else f"{os.getcwd()}/RentScrape/drop/aqua/{datetime.datetime.now().strftime('%Y-%m-%d')}/infos.json"
        with open(self.drop_file, "r") as f:
            self.my_dict = json.loads(f.read())

    def transform(self) -> list[pd.Dataframe]:
        layouts = self.my_dict["units_data"]["layouts"]
        floorplan_df = pd.DataFrame(layouts)
        floorplan_df = floorplan_df[["area", "bathrooms", "bedrooms", "name"]]
        units = self.my_dict["units_data"]["units"]
        units_df = pd.DataFrame(units)
        units_df = units_df[["area","availableOn","layoutName","name","price"]]

        return units_df, floorplan_df