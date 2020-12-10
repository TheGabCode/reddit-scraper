from bs4 import BeautifulSoup
import requests
import random
from common import Constants

class RequestManager:
    def __init__(self):
        self.agents = Constants.agents

    def getRedditSoup(self, url):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US, en; q=0.9",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": self.agents[random.randint(0, len(self.agents))]
        }
        
        response = requests.get(url, headers = headers)
    
        if (response.status_code != 200):
            return BeautifulSoup("", "html.parser")

        return BeautifulSoup(response.text, "html.parser")


    def postRedditSoup(self, url, payload):
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US, en; q=0.9",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": self.agents[random.randint(0, len(self.agents))]
        }
    
        response = requests.post(url, headers = headers, data = payload)
    
        if (response.status_code != 200):
            return BeautifulSoup("", "html.parser")

        return BeautifulSoup(response.text, "html.parser")