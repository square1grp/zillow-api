import requests
from lxml import etree
import json
from config import api_key
import single_listing


def crawl(url):
    session = requests.Session()
    response = session.get(
        'http://api.scraperapi.com/?api_key=%s&url=%s' % (api_key, url))

    if response.status_code != 200:
        return 'Response code is %s' % response.status_code

    response_text = response.text
    tree = etree.HTML(response_text.encode('utf8'))

    single_listing_url_arr = tree.xpath(
        '//ul[@class=\'photo-cards photo-cards_wow photo-cards_short\']/li/article/a/@href')

    data = []
    for single_listing_url in single_listing_url_arr:
        data.append(single_listing.crawl(single_listing_url))

    return data
