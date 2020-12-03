import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup


counter = 1
user_agent = '''Mozilla/5.0 (Windows NT 10.0; Win64; x64; \
    rv:82.0) Gecko/20100101 Firefox/82.0'''


def soupify(dataframe):
    """
    Converts the markup of a link in a pandas column to a BeautifulSoup Object.

    """
    global counter
    variable_link = dataframe

    product_url = f'''https://www.jumia.com.ng{variable_link}'''

    headers = {'user-agent': user_agent}

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    markup = session.get(product_url, headers=headers, timeout=5).text

    soup = BeautifulSoup(markup, 'lxml')
    print(counter)
    counter += 1
    return soup


def page_scraper(dataframe):
    """
    Parses the markup of a link in a pandas column.

    Returns scraped data.
    """
    soup = soupify(dataframe)

    # Product Name/Title
    try:
        product_name = soup.find_all(
            class_='-fs20 -pts -pbxs')[0].text
    except IndexError:
        product_name = None

    # Product Brand
    try:
        product_brand = soup.find_all(
            'div', class_='-fs14 -pvxs')[0].a.text
    except IndexError:
        product_brand = None

    # Product Type
    try:
        product_type = soup.find_all('a', class_='cbs')[-2].text
    except IndexError:
        product_type = None

    # Product Rating
    try:
        product_rating = soup.find_all(
            'div', class_='-fs29 -yl5 -pvxs')[0].span.text
    except IndexError:
        product_rating = None

    # Product Price
    try:
        product_price = soup.find_all(
            class_='-b -ltr -tal -fs24')[0].text
    except IndexError:
        product_price = None

    # Image link
    try:
        image_link = soup.find_all(
            'img', class_='-fw -fh')[0].get('data-src')
    except IndexError:
        image_link = None

    return product_name, product_brand, product_type,\
        product_rating, product_price, image_link
