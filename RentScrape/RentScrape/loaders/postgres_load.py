import pandas as pd


class PostgresLoader:
    def __init__(self, engine):
        self.engine = engine

    def load(self, table_name: str, data: pd.DataFrame, if_exists: str="append"):
        if data.empty:
            return
    
        data.to_sql(table_name, self.engine, if_exists=if_exists, index=False)