# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class LeruaParserPipeline:
    def process_item(self, item, spider):
        return item


class ImagesLoader(ImagesPipeline):

    def get_media_requests(self, item, info):
        photo = item['photo']
        if photo:
            for img in photo:
                try:
                    yield scrapy.Request(img)

                except TypeError as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        directory = item['name'][0].replace('/', '_')
        split_url = request.url.split('/')
        file_name = split_url[len(split_url) - 1]
        return f'{directory}/{file_name}'

    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0]]
        return item
