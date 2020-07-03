# -*- coding: utf-8 -*-
import scrapy
import json
import urllib
from scrapy.http.request.json_request import JsonRequest

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['ci.minneapolis.mn.us', 'services.arcgis.com', 'opendata.arcgis.com']
   
    def __init__(self, *args, **kwargs):
        super(ExampleSpider, self).__init__(*args, **kwargs)
        # Mapping from name of dataset to data entries
        self.datasets = {}

    def parse(self, response):
        jsn = json.loads(response.text)
        # Params used to get data entries from API
        params = {
            "outFields": "*",
            "returnGeometry": "false",
            "resultOffset": 0,
            "resultRecordCount": 10,
            "f": "json",
            "where": "1=1"
        }
        for obj in jsn['data']:
            # Attributes contain the name of the dataset and URL, among other things
            attrs = obj['attributes']
            # Request data entries from API
            yield scrapy.Request(
                url=attrs['url'] + '/query?' + urllib.parse.urlencode(params),
                callback=self.parse_records,
                meta={'name': attrs['name']}
            )

    def parse_records(self, response):
        jsn = json.loads(response.text)
        # 'features' contains data entries
        for record in jsn['features']:
            attrs = record['attributes']
            # Add dataset to mapping if not there 
            dataset = self.datasets.setdefault(response.meta['name'], [])
            # Add data entry to dataset
            dataset.append(attrs)

    def start_requests(self):
        # ID of Minneapolis datasets. Gotten from Chrome Dev Tools
        payload = {
            "catalog": {
                "groupIds": "any(79606f50581f4a33b14a19e61c4891f7)"
            }
        }
        return [
            JsonRequest(
                url='https://opendata.arcgis.com/api/v3/search', 
                method='POST', 
                data=payload
            )
        ]



     
    
