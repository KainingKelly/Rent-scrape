import pandas as pd


class Loader:
    def load(self, dest_file: str, data: pd.DataFrame):
        data.to_csv(dest_file, index=False)