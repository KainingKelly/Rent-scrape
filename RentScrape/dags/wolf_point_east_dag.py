import argparse
import datetime
import os

from RentScrape.RentScrape.loaders.wolf_point_east_load import WolfPointEastLoader
from RentScrape.RentScrape.transformers.wolf_point_east_transform import WolfPointEastTransform



def dag(crawl: bool, tl: bool):
    # Extract
    if crawl:
        os.system("scrapy crawl WolfPointEast")

    if tl:
        # Transform
        transformer = WolfPointEastTransform()
        units, floorplans = transformer.grab_files()


        # Load
        result_path = f"{os.getcwd()}/result/{datetime.datetime.now().strftime('%Y-%m-%d')}"
        if not os.path.exists(result_path):
                os.mkdir(result_path)

        loader = WolfPointEastLoader()
        loader.load(f"{result_path}/units.csv", units)
        loader.load(f"{result_path}/floorplans.csv", floorplans)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--crawl", action="store_true")
    parser.add_argument("--tl", action="store_true")

    args = parser.parse_args()

    dag(args.crawl, args.tl)