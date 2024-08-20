from lib.utils import get_html_content, format_date
from bs4 import BeautifulSoup
import json


def get_all_events(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    not_featured_events = soup.find_all('div', class_='row columns is-mobile')
    featured_events = soup.find_all('div', class_='row columns is-mobile featured')
    events = not_featured_events + featured_events
    event_data = []

    for div_tag in events:
        for script in div_tag.find_all('script'):
            try:
                script_content = script.get_text().strip().replace('\n', '')
                script_json = json.loads(script_content)
                script_json["endDate"] = format_date(script_json["endDate"], "%Y-%m-%dT%H:%M:%S.%f%z")
                script_json["startDate"] = format_date(script_json["startDate"], "%Y-%m-%dT%H:%M:%S.%f%z")
                del script_json["@context"]
                del script_json["@type"]
                del script_json["performer"]
                event_data.append(script_json)
            except json.JSONDecodeError:
                continue

    return event_data


def scrape():
    url = "https://dev.events/AS/PH"
    html_content = get_html_content(url)

    events = get_all_events(html_content)
    print(events)
    return events