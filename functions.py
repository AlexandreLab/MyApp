# -*- coding: utf-8 -*-
import requests
import pandas as pd
from xml.etree import ElementTree
from datetime import timedelta


def get_request(url, **kwargs):
    try:
        req = requests.get(url, **kwargs)
        response_code = req.status_code
        print(response_code)
        if response_code == 204:
            print("No content returned, but no error reported.")

        elif response_code != 200:
            print("No data returned. Error reported.")

    except requests.exceptions.RequestException as e:
        print(e)
    return req


def xml_to_pd(req):
    tree = ElementTree.fromstring(req.text)
    data = []
    index = []
    period = ""
    print(tree[0][0].text)
    for branch in tree.iter('item'):
        source = branch.find('powerSystemResourceType').text.replace('"', "")
        quantity = float(branch.find('quantity').text)
        period = branch.find('settlementPeriod').text
        index.append(source)
        data.append(quantity)
    return pd.DataFrame(index=index, columns=[period], data=data)


def time_details(time):
    period = time.hour*2+time.minute//30
    date = time.strftime("%Y-%m-%d")
    if period == 0:
        period = 48
        date = (time-timedelta(days=1)).strftime("%Y-%m-%d")
    return date, period
