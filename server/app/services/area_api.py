from tenacity import retry, stop_after_attempt, wait_fixed
from urllib.parse import urlencode
from typing import Callable
import requests



class AreaApi:
    def __init__(self, exception_class: Callable):
        self.exception_class = exception_class
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def get(self, url, params={}, headers={}):
        try:
            r = requests.get(url=url, params=params, headers=headers)
            
            if r.status_code != 200:
                raise self.exception_class(f"Can't access resource (link = {url + "?" + urlencode(params)}, header = {headers})")
            
            return r.json()
        except requests.exceptions.ConnectionError:
            raise self.exception_class(f"Can't connect to the website \"{url}\"")
