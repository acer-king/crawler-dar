import requests
import random
from typing import List


class UrlMgr:
    def __init__(self, proxies: List):
        self.proxies = proxies

    def choose_proxy(self):
        proxy = random.randint(0, len(self.proxies) - 1)
        return self.proxies[proxy]

    def url_request(self, url_path: str, max_try=3) -> str:
        limit = 0
        while True:
            if limit > max_try:
                return None
            try:
                proxy = self.choose_proxy()
                proxies = {"http": proxy}
                response = requests.get(url_path, proxies=proxies, timeout=5)
                break
            except Exception as err:
                print(err)
                print("trying with other proxy")
            limit += 1
        return response.text

