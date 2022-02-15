from dotenv import load_dotenv
from pathlib import Path

import requests
import json

URL = {
    'fusion_base' : 'https://api.yelp.com/v3{url}',
    'businesses' : '/businesses/search',
    'id' : '/buisnesses/{id}',
    'autocomplete' : '/autocomplete',
    'ipstack_base' : 'http://api.ipstack.com/{url}',
}

class BASE_API(object):
    def __init__(self):
        pass

    def __request(self, api_url, params={}):
        args = {}
        if('access_key' in params.keys()):
            base_url = URL['ipstack_base']
        else:
            base_url = URL['fusion_base']

        response = requests.get(base_url.format(url=api_url), params=args)
        return response.json()
    
    def __request_json(self, api_url, data, params={}):
        header={'Content-type': 'application/json', 'Authorization' : 'Bearer {}'.format(self.api_key)}
        if('access_key' in params.keys()):
            base_url = URL['ipstack_base']
        else:
            base_url = URL['fusion_base']
        url = base_url.format(url=api_url)
        response = requests.get(
            url, 
            params=params,
            headers=header
        )
        return response.json()

class FUSION_API(BASE_API):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key

    def get_autocomplete(self, search_query, long, lat):
        api_url = URL['autocomplete']
        params = {
            'text' : search_query, 
            'latitude' : lat, 
            'longitude' : long
        }
        payload = {}
        return self._BASE_API__request_json(api_url, payload, params)
    
    def search_buisness(self, search_query, long, lat):
        api_url = URL['businesses']
        payload = {}
        params = {
            'term' : search_query,
            'latitude' : lat,
            'longitude' : long,
            'limit' : 20
        }
        return self._BASE_API__request_json(api_url, payload, params)


class IPSTACK_API(BASE_API):

    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
    
    def get_ip_data(self, ip):
        api_url = ip
        payload = {}
        params = {'access_key' : self.api_key}
        return self._BASE_API__request_json(api_url, payload, params)