from lib.utils import get_html_content
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}


def extract_event_ids(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    div_tags = soup.find_all('div', class_='conf-list elist active')
    return [div_tag.get('data-val') for div_tag in div_tags if div_tag.get('data-val')]


def extract_event_details_by_ids(ids):
    events = []

    for event_id in ids:
        event_url = "https://internationalconferencealerts.com/eventdetails.php?id=" + event_id
        html_content = get_html_content(url=event_url, headers=headers)
        soup = BeautifulSoup(html_content, 'html.parser')

        title = soup.find('h1').get_text(strip=True)
        description = soup.find('h5', text='Objective of the Conference').find_next('p').get_text(strip=True)
        location = soup.find('b').find_all('i')[1].next_sibling.strip()
        link = ''
        start_date = ''
        organizer = ''
        contact_person = ''
        registration_deadline = ''
        
        for row in soup.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 2 and cells[0].get_text(strip=True) == "Event Start Date":
                start_date = cells[1].get_text(strip=True)
            elif len(cells) == 2 and cells[0].get_text(strip=True) == "Organized By":
                organizer = cells[1].get_text(strip=True)
            elif len(cells) == 2 and cells[0].get_text(strip=True) == "Contact Person":
                contact_person = cells[1].get_text(strip=True)
            elif len(cells) == 2 and cells[0].get_text(strip=True) == "Registration Deadline":
                registration_deadline = cells[1].get_text(strip=True)
            elif len(cells) == 2 and cells[0].get_text(strip=True) == "Visit Website":
                link = cells[1].find('a')['href']
        
        events.append({
            'event_id': event_id,
            'title': title,
            'description': description,
            'location': location,
            'start_date': start_date,
            'organizer': organizer,
            'contact_person': contact_person,
            'registration_deadline': registration_deadline,
            'link': link
        })

    return events


def scrape():
    url = "https://internationalconferencealerts.com/philippines/information-technology"
    html_content = get_html_content(url=url, headers=headers)

    event_ids = extract_event_ids(html_content)
    events = extract_event_details_by_ids(event_ids)

    print(events)
    return events