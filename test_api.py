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
# resp = requests.get("https://services.arcgis.com/afSMGVsC7QlRK1kZ/arcgis/rest/services/Police_Incidents_2018_PIMS/FeatureServer/0/query", params=params)
payload = {
    "catalog": {
        "groupIds" : "any(79606f50581f4a33b14a19e61c4891f7)" 
    }
}
resp = requests.post("https://opendata.arcgis.com/api/v3/search", json=payload)
jsn = resp.json()
for obj in jsn['data']:
    print('{}:{}'.format(obj['attributes']['name'], obj['attributes']['url']))
    resp2 = requests.get(obj['attributes']['url'] + '/query', params=params)
    for record in resp2.json().get('features', []):
        print(record['attributes'])

