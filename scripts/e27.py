from datetime import datetime
from lib.utils import format_date
import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}


def format_dates(events):
    for event in events:
        event["datestart"] = format_date(event["datestart"], "%Y-%m-%d %H:%M:%S")
        event["dateend"] = format_date(event["dateend"], "%Y-%m-%d %H:%M:%S")
    return events


def get_events():
    url = "https://e27.co/api/event/get/landing/?page=1&locations%5Bc383%5D=Philippines&datestart&upcoming=1"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        events = format_dates(response.json()["data"]["events"])
        for event in events:
            event["image"] = event["leadimage"]["large"]
            del event["leadimage"]
        print(events)
        return events
    else:
        print(f"Failed to retrieve events. Status code: {response.status_code}")
        return None
