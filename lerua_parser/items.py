# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def prepare_data(value):
    price = int(value.replace(' ', ''))
    return price


def prepare_foto(value):
    try:
        photo = value.replace('w_82,h_82', 'w_1200,h_1200')
        print(photo)
        return photo
    except Exception:
        return value


class LeruaParserItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(prepare_data))
    article = scrapy.Field()
    text = scrapy.Field()
    photo = scrapy.Field(input_processor=MapCompose(prepare_foto))
