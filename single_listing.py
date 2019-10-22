import requests
from lxml import etree
import json
from config import api_key


def crawl(url):
    session = requests.Session()
    response = session.get(
        'http://api.scraperapi.com/?api_key=%s&url=%s' % (api_key, url))

    if response.status_code != 200:
        return 'Response code is %s' % response.status_code

    response_text = response.text
    tree = etree.HTML(response_text.encode('utf8'))

    data = {
        'address': get_address(tree),
        'address2': get_address2(tree),
        'city': get_city(tree),
        'state': get_state(tree),
        'zip': get_zipcode(tree),
        'price': get_price(tree),
        'beds': get_beds(tree),
        'fullBaths': get_fullbaths(tree),
        'halfBaths': get_halfbaths(tree),
        'sqFoot': get_sqft(tree),
        'type': get_type(tree),
        'yearBuilt': get_yearbuilt(tree),
        'images': get_images(tree)
    }

    return data


def get_address(tree):
    try:
        if tree.xpath('//h1[@class=\'ds-address-container\']/span[1]/text()')[0].endswith(','):
            return tree.xpath('//h1[@class=\'ds-address-container\']/span[1]/text()')[0][:-1]

        return tree.xpath('//h1[@class=\'ds-address-container\']/span[1]/text()')[0]
    except:
        print('======== Error in get_address =========')
        return ''


def get_address2(tree):
    try:
        return tree.xpath('//h1[@class=\'ds-address-container\']/span[2]/text()')[0].replace(u'\xa0', u'')
    except:
        print('======== Error in get_address2 =========')
        return ''


def get_city(tree):
    try:
        return tree.xpath('//h1[@class=\'ds-address-container\']/span[2]/text()')[1].split(',')[0]
    except:
        print('======== Error in get_city =========')
        return ''


def get_state(tree):
    try:
        return tree.xpath('//h1[@class=\'ds-address-container\']/span[2]/text()')[1].split(',')[1].strip().split()[0]
    except:
        print('======== Error in get_state =========')
        return ''


def get_zipcode(tree):
    try:
        return tree.xpath('//h1[@class=\'ds-address-container\']/span[2]/text()')[1].split(',')[1].strip().split()[1]
    except:
        print('======== Error in get_state =========')
        return ''


def get_price(tree):
    try:
        return tree.xpath('//span[@class=\'ds-value\']/text()')[0][1:]
    except:
        print('======== Error in get_state =========')
        return ''


def get_beds(tree):
    try:
        return tree.xpath('//span[contains(text(), \'Bedrooms:\')]/text()')[1]
    except:
        try:
            return tree.xpath('//td[contains(text(), \'Bedrooms\')]/../td[2]/span/text()')[0]
        except:
            pass

        print('======== Error in get_beds =========')
        return ''


def get_fullbaths(tree):
    try:
        return tree.xpath('//span[contains(text(), \'Full bathrooms:\')]/text()')[1]
    except:
        try:
            return tree.xpath('//td[contains(text(), \'Bathrooms\')]/../td[2]/span/text()')[0]
        except:
            pass

        print('======== Error in get_fullbath =========')
        return ''


def get_halfbaths(tree):
    try:
        return tree.xpath('//span[contains(text(), \'1/2 bathrooms:\')]/text()')[1]
    except:
        try:
            return tree.xpath('//td[contains(text(), \'1/2 bathrooms\')]/../td[2]/span/text()')[0]
        except:
            pass

        print('======== Error in get_halfbaths =========')
        return ''


def get_sqft(tree):
    try:
        return tree.xpath('//h3[@class=\'ds-bed-bath-living-area-container\']//span[3]/span/text()')[0]
    except:
        print('======== Error in get_sqft =========')
        return ''


def get_type(tree):
    try:
        return tree.xpath('//li[@class=\'ds-home-fact-list-item\'][1]/span[2]/text()')[0]
    except:
        print('======== Error in get_type =========')
        return ''


def get_yearbuilt(tree):
    try:
        return tree.xpath('//li[@class=\'ds-home-fact-list-item\'][2]/span[2]/text()')[0]
    except:
        print('======== Error in get_yearbuilt =========')
        return ''


def get_images(tree):
    try:
        return tree.xpath('//ul[@class=\'media-stream media-stream--initial\']/li//img/@src')
    except:
        print('======== Error in get_images =========')
        return ''
