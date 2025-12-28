import argparse
import datetime
import os
from RentScrape.RentScrape.loaders.load import Loader
from RentScrape.RentScrape.transformers.onechicago_transform import OneChicagoTransform


def dag(crawl: bool, tl: bool):
    #Extract
    if crawl:
        os.system("cd RentScrape; scrapy crawl OneChicago")

    if tl:
        #Transform
        transformer = OneChicagoTransform()
        units, floorplans = transformer.grab_files()

        #Load
        result_path = f"{os.getcwd()}/RentScrape/result/onechicago/{datetime.datetime.now().strftime('%Y-%m-%d')}"
        if not os.path.exists(result_path):
            os.mkdir(result_path)

        loader = Loader()
        loader.load(f"{result_path}/units.csv",units)
        loader.load(f"{result_path}/floorplans.csv", floorplans)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--crawl", action="store_true")
    parser.add_argument("--tl", action="store_true")

    args = parser.parse_args()

    dag(args.crawl, args.tl)
        