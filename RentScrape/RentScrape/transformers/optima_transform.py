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
        floor_plan_df = floor_plan_df[["id","name","bedroom_count","bathroom_count", "image_url"]]

        floor_plan_df = pd.merge(floor_plan_df, units_df[["floor_plan_id", "display_area"]], left_on="id", right_on="floor_plan_id")
        units_df = pd.merge(floor_plan_df[["id", "name"]].rename(columns={"name": "floorplan"}), units_df, left_on="id", right_on="floor_plan_id")
        floor_plan_df = floor_plan_df.drop_duplicates(keep='first')
        floor_plan_df = floor_plan_df.drop('id', axis=1)

        units_df = units_df[["floorplan","unit_number","display_price","display_available_on"]]

        units_df = units_df.rename(columns={"display_price":"price", "display_available_on":"date_available"})
        units_df["as_of"] = datetime.date.today()
        units_df["building"] = "Optima"

        floor_plan_df = floor_plan_df.rename(columns={"bedroom_count":"beds", "bathroom_count":"baths", "display_area":"size", "image_url":"img_path"})
        floor_plan_df = floor_plan_df.drop("floor_plan_id", axis=1)
        floor_plan_df["building"] = "Optima"

        return units_df, floor_plan_df
