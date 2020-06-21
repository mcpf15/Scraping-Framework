import requests
import re

params = {
        "outFields": "*",
        "returnGeometry": "false",
        "resultOffset": 0,
        "resultRecordCount": 5,
        "f": "json",
        "where": "1=1"
        }
resp = requests.get("https://services.arcgis.com/afSMGVsC7QlRK1kZ/arcgis/rest/services/Police_Incidents_2018_PIMS/FeatureServer/0/query", params=params)
jsn = resp.json()

for obj in jsn['features']:
    print(obj['attributes'])

