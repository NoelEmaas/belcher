import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime


def get_html_content(url, verify=True, headers={}):
    response = requests.get(
        url = url, 
        headers = headers, 
        verify = verify
    )

    if response.status_code == 200:
        return response.content
    else:
        sys.exit(f"Failed to get html content. Status code: {response.status_code}")


def format_date(date, format):
    return datetime.strptime(date, format).strftime("%B %d, %Y %I:%M %p")
