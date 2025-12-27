import datetime
import json
import os

import pandas as pd


class OptimaTransform:
    def __init__(self, drop_file: str = None):
        self.drop_file = drop_file if drop_file else f"{os.getcwd()}/RentScrape/drop/optima/{datetime.datetime.now().strftime('%Y-%m-%d')}/infos.json"
        with open(self.drop_file, "r") as f:
            self.my_dict = json.loads(f.read())

    def transform(self) -> list[pd.DataFrame]:
        units = self.my_dict["data"]["units"]
        units_df = pd.DataFrame(units)
        units_df = units_df[["floor_plan_id","unit_number","display_area","display_price","display_available_on","display_lease_term"]]

        floor_plans = self.my_dict["data"]["floor_plans"]
        floor_plan_df = pd.DataFrame(floor_plans)
        floor_plan_df = floor_plan_df[["id","name","bedroom_count","bathroom_count"]]

        floor_plan_df = pd.merge(floor_plan_df, units_df[["floor_plan_id", "display_area"]], left_on="id", right_on="floor_plan_id")
        floor_plan_df = floor_plan_df.drop_duplicates(keep='first')
        floor_plan_df = floor_plan_df.drop('id', axis=1)

        units_df = units_df[["floor_plan_id","unit_number","display_price","display_available_on","display_lease_term"]]

        return units_df, floor_plan_df
