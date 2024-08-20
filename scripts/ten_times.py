from lib.utils import get_html_content
from bs4 import BeautifulSoup

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
}


def get_event_cards(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    event_cards = soup.find_all('tr', class_='event-card')
    return event_cards


# WIP. (Not working yet)
def scrape():
    url = "https://10times.com/philippines/technology"
    html_content = get_html_content(url, headers=headers)
    event_cards = get_event_cards(html_content)
    print(event_cards)
    return event_cards
