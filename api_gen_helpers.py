import _pickle as pickle
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from product_info_scraper import user_agent
import numpy as np


def list_of_dict(list_of_tuples, page_tuple):
    """
    Converts a list of tuples to a list of dictionary types.
    """
    keys = ('id', 'product_link', 'product_name', 'product_brand',
            'product_type', 'product_rating', 'product_price', 'image_link')
    list_of_dict = [dict(zip(keys, values))
                    for values in list_of_tuples if values[2] != page_tuple[0]]
    return list_of_dict


def page_scraper(link_url):
    """
    Scrapes specific information from the page of a url given.
    """
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    headers = {'user-agent': user_agent}

    try:
        markup = session.get(link_url, headers=headers, timeout=5).text
    except requests.exceptions.MissingSchema:
        link_url = 'https://' + link_url
        markup = session.get(link_url, headers=headers, timeout=5).text

    soup = BeautifulSoup(markup, 'lxml')

    try:
        product_name = soup.find_all(
            class_='-fs20 -pts -pbxs')[0].text
    except IndexError:
        product_name = ''

    # Product Type
    try:
        product_type = soup.find_all('a', class_='cbs')[-2].text
    except IndexError:
        product_type = ''

    return product_name, product_type


def pipeline(page_tuple):
    """
    Converts text into vectors.
    """
    name_vectorizer = pickle.load(open("product_name_vectorizer.bin", "rb"))
    type_vectorizer = pickle.load(open("product_type_vectorizer.bin", "rb"))

    name_array = name_vectorizer.transform([page_tuple[0]]).toarray()
    type_array = type_vectorizer.transform([page_tuple[1]]).toarray()

    combined_array = np.column_stack((name_array, type_array))
    variance_selector = pickle.load(open("variance_threshold.bin", "rb"))
    reduced_array = variance_selector.transform(combined_array)

    return reduced_array
