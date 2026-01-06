import argparse
import datetime
import os

from RentScrape.RentScrape.loaders.csv_load import CsvLoader
from RentScrape.RentScrape.transformers.optima_transform import OptimaTransform

def dag(crawl: bool, tl: bool):
    # Extract
    if crawl:
        os.system("cd RentScrape; scrapy crawl Optima")

    if tl:
        # Transform
        transformer = OptimaTransform()
        units, floorplans = transformer.transform()

        # Load
        result_path = f"{os.getcwd()}/RentScrape/result/optima/{datetime.datetime.now().strftime('%Y-%m-%d')}"
        if not os.path.exists(result_path):
            os.mkdir(result_path)

        loader = CsvLoader()
        loader.load(f"{result_path}/units.csv", units)
        loader.load(f"{result_path}/floorplans.csv", floorplans)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--crawl", action="store_true")
    parser.add_argument("--tl", action="store_true")

    args = parser.parse_args()

    dag(args.crawl, args.tl)