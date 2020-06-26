# -*- coding: utf-8 -*-
import scrapy
import json
import urllib
from scrapy.http.request.json_request import JsonRequest

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['ci.minneapolis.mn.us', 'services.arcgis.com', 'opendata.arcgis.com']

    def parse(self, response):
        jsn = json.loads(response.text)
        params = {
                "outFields": "*",
                "returnGeometry": "false",
                "resultOffset": 0,
                "resultRecordCount": 1,
                "f": "json",
                "where": "1=1"
                }
        for obj in jsn['data']:
            attrs = obj['attributes']
            print('{}:{}'.format(attrs'name'], attrs['url']))
            yield scrapy.Request(url=attrs['url'] + '/query?' + urllib.parse.urlencode(params), callback=self.parse_records)

    def parse_records(self, response):
        jsn = json.loads(response.text)
        for record in jsn['features']:
            yield record['attributes']

    def start_requests(self):
        payload = {
                "catalog": {
                    "groupIds": "any(79606f50581f4a33b14a19e61c4891f7)"
                    }
                }
        return [JsonRequest(url='https://opendata.arcgis.com/api/v3/search', method='POST', data=payload)]




     
    
