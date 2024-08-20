from lib.utils import get_html_content
from bs4 import BeautifulSoup


def get_all_event_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    div_tags = soup.find_all('div', class_='ht-eb-card__left')
    href_values = [a_tag.get('href') for div_tag in div_tags for a_tag in div_tag.find_all('a') if a_tag.get('href')]
    return href_values


def get_all_events_by_links(links):
    events = []

    for link in links:
        html_content = get_html_content(url=link, verify=False)
        soup = BeautifulSoup(html_content, 'html.parser')

        title = soup.find('h1', class_='event__title').get_text(strip=True)
        description = soup.find('div', class_='event-description__text').find('p').get_text(strip=True)
        organizer = soup.find('div', class_='event__organizer').find('a').get_text(strip=True)
        event_link = soup.find('a', class_='button large').get('href')
        location = soup.find('div', class_='event__info event__info--location').get_text(strip=True)
        date = soup.find('div', class_='event__info event__info--date').get_text(strip=True)

        events.append({
            'event_link': event_link,
            'title': title,
            'description': description,
            'organizer': organizer,
            'location': location,
            'date': date
        })

    return events


def scrape():
    # Replace the url to: https://www.hackathon.com/country/philippines in the future
    # Keep the url for now since the link for the upcoming events is currently empty

    url = "https://www.hackathon.com/country/philippines/2022"
    html_content = get_html_content(url, verify=False)

    event_links = get_all_event_links(html_content)
    events = get_all_events_by_links(event_links)
    
    print(events)
    return events
