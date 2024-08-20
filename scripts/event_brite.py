from bs4 import BeautifulSoup
from lib.utils import get_html_content

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}


def get_all_event_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    a_tags = soup.find_all('a', class_='event-card-link')
    href_values = list(set([a_tag.get('href') for a_tag in a_tags if 'event-card-link' in a_tag.get('class', [])]))
    return href_values


def get_all_events_by_links(links):
    events = []

    for link in links:
        html_content = get_html_content(url=link, verify=False)
        soup = BeautifulSoup(html_content, 'html.parser')

        title = soup.find('h1', class_='event-title').get_text(strip=True)
        start_date = soup.find('time', class_='start-date').get_text(strip=True)
        full_date = soup.find('span', class_='date-info__full-datetime').get_text(strip=True)
        description = soup.find('p', class_='summary').get_text(strip=True)
        location = soup.find('p', class_='location-info__address-text').get_text(strip=True)
        organizer = soup.find('a', class_='descriptive-organizer-info-mobile__name-link').get_text(strip=True)
        price = soup.find('div', class_='conversion-bar__panel-info').get_text(strip=True) if soup.find('div', class_='conversion-bar__panel-info') else ''

        events.append({
            'link': link,
            'title': title,
            'start_date': start_date,
            'full_date': full_date,
            'description': description,
            'location': location,
            'organizer': organizer,
            'price': price
        })

    return events


def scrape():
    url = "https://www.eventbrite.com/d/philippines--manila/technology/"
    html_content = get_html_content(url, headers=headers)

    soup = BeautifulSoup(html_content, 'html.parser')
    pagination = soup.find('li', {'data-testid': 'pagination-parent'}).get_text(strip=True)
    num_pages = int(pagination.split(' ')[1])

    all_event_links = []

    for page in range(1, num_pages + 1):
        paginated_url = f"{url}?page={page}"
        page_content = get_html_content(paginated_url, headers=headers)
        event_links = get_all_event_links(page_content)
        all_event_links.extend(event_links)

    events = get_all_events_by_links(all_event_links)

    print(events)
    return events