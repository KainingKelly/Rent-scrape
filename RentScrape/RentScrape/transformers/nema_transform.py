import datetime
import os

import pandas as pd
import scrapy


class NemaTransform:
    def __init__(self, drop_path = None) -> None:
        self.drop_path = drop_path if drop_path else f"{os.getcwd()}/RentScrape/drop/nema/{datetime.datetime.now().strftime('%Y-%m-%d')}/"

    def transform(self) -> list[pd.DataFrame]:
        file = f"{self.drop_path}/availability.html"
        with open(file, "r") as f:
            response = scrapy.Selector(text=f.read())
        objects = response.xpath("//div[@class='availabilities-list__item']")
        listing_details = []
        for object in objects:
            room_number = object.xpath('.//div[contains(@class,"cell--unit")]/span[@class="text--num"]/text()').get().replace("#","").strip()
            img_path = object.xpath('.//a[contains(@class, "dl-floorplan")]/@data-image').get()
            price = object.xpath('.//div[contains(@class, "cell--minRent")]/span/text()').get()
            size = object.xpath('.//div[contains(@class, "cell--size")]/span/text()').get()
            infos = object.xpath('.//div[contains(@class,"cell--bet")]//text()').getall()
            infos = " ".join(infos).strip().split("/")
            beds = " ".join(infos[0].split())
            baths = " ".join(infos[1].split())
            date_available = object.xpath('.//div[contains(@class, "cell--viewAvailability")]//text()').getall()
            date_available = " ".join(date_available)
            date_available = " ".join(date_available.split()).split()[0]
            floorplan_name = object.xpath('.//@data-unittype').get()

            listing_details.append({
                'unit_number': room_number,
                'img_path': img_path,
                'price': price,
                'size': size,
                'beds': beds,
                'baths': baths,
                'date_available': date_available,
                'floorplan': floorplan_name,
            })
        listing_df = pd.DataFrame(listing_details)
        listing_df['building'] = 'Nema'
        
        floorplan_df = listing_df[['floorplan', 'beds', 'baths', 'size', 'img_path', 'building']]
        floorplan_df = floorplan_df.drop_duplicates()
        floorplan_df = floorplan_df.rename(columns={'floorplan': 'name'})

        
        unit_df = listing_df[['unit_number', 'floorplan', 'price', 'date_available', 'building']]
        unit_df['as_of'] = datetime.date.today()
        return [unit_df, floorplan_df]

