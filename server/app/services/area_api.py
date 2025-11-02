from urllib.parse import urlencode
from typing import Callable
import requests



class AreaApi:
    def __init__(self, exception_class: Callable):
        self.exception_class = exception_class
    
    def get(self, url, params={}, headers=None, good_status_code=[200]):
        try:
            r = requests.get(url=url, params=params, headers=headers)

            if r.status_code not in good_status_code:
                raise self.exception_class(f"Can't access resource (link = {url + "?" + urlencode(params)}, header = {headers})")
            
            return r.json()
        except requests.exceptions.ConnectionError:
            raise self.exception_class(f"Can't connect to the website \"{url}\"")

    def post(self, url, data=None, auth=None, headers=None, good_status_code=[200]):
        try:
            r = requests.post(url, json=data, auth=auth, headers=headers)
            
            if r.status_code not in good_status_code:
                raise self.exception_class(f"Can't access resource (link = {url}, header = {headers}), data = {data}, auth = {auth}, res = {r.content}, error code = {r.status_code}")
            
            return r.json()
        except requests.exceptions.ConnectionError:
            raise self.exception_class(f"Can't connect to the website \"{url}\"")
