import requests
from bs4 import BeautifulSoup


def link_scraper(pages, section):
    """
    Accepts the number of section pages to be scraped and the product section.

    Returns product page links.
    """

    links = []
    for n in range(1, pages+1):
        markup = requests.get(
            f'https://www.jumia.com.ng/{section}/?page={n}').text
        soup = BeautifulSoup(markup, 'lxml')

        links.extend([a.get('href')
                      for a in soup.find_all('a', class_='core')
                      if a.get('href')])

    return links
