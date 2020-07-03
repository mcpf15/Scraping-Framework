# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class BasePipeline:
    def close_spider(self, spider):
        for name, records in spider.datasets.items():
            # Store each dataset as its own file
            with open('{}.json'.format(name), 'w') as f:
                json.dump(records, f, indent=4)
