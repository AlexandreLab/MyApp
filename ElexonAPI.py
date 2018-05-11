import pandas as pd
from xml.etree import ElementTree
from datetime import datetime, timedelta
import requests


def xml_to_df(req):
    tree = ElementTree.fromstring(req.text)
    data = []
    index = []
    period = ""
    if tree[0][0].text == "200":
        for branch in tree.iter('item'):
            source = branch.find('powerSystemResourceType').text.replace('"', "")
            quantity = float(branch.find('quantity').text)
            period = branch.find('settlementPeriod').text
            date = branch.find('settlementDate').text
            index.append(source)
            data.append(quantity)
        return pd.DataFrame(index=index, columns=[date+" "+period], data=data)
    else:
        return False


def get_time_params(time):
    period = time.hour*2+time.minute//30
    date = time.date()
    if period == 0:
        period = 48
        date = (time-timedelta(days=1))
    return date, period


def get_request(url, params):
    try:
        req = requests.get(url, params=params)
        response_code = req.status_code
        print(response_code)
        if response_code == 204:
            print("No content returned, but no error reported.")

        elif response_code != 200:
            print("No data returned. Error reported.")

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        return False
    else:
        return req


class ElexonAPI(object):

    def __init__(self, apikey=None, report=None):
        self.report = 'B1620'
        self.version = 'v1'
        self.apikey = apikey
        self.url = "https://api.bmreports.com/BMRS/{}/{}".format(self.report.upper(), self.version)
        date, period = get_time_params(datetime.now())
        self.last_date = date
        self.last_period = period
        self.data = pd.DataFrame()

    def get_data(self):
        print("get date", self.last_date.strftime("%Y-%m-%d"), self.last_period)
        params = {
            'SettlementDate': self.last_date.strftime("%Y-%m-%d"),
            'Period': self.last_period,
            'APIKey': self.apikey,
            'ServiceType': 'xml'
        }
        response = get_request(self.url, params)
        temp_df = xml_to_df(response)

        if isinstance(temp_df, pd.DataFrame):
            self.data = pd.concat([self.data, temp_df], axis=1)
            if (self.last_period+1) > 48:
                self.last_period = 1
                self.last_date = self.last_date+timedelta(days = 1)
            else:
                self.last_period = self.last_period+1
            return True
        else:
            print("No content returned, but no error reported. Retry later.")
            return False

    def clear_data(self):
        self.data = pd.DataFrame()

    def get_full_historical_data(self, startDate):
        self.clear_data()
        self.get_historical_data(startDate, datetime.now())

    def get_historical_data(self, startDate, endDate):
        date, period = get_time_params(startDate)
        self.clear_data()
        self.last_date = date
        self.last_period = period
        duration = endDate-startDate
        seconds = duration.seconds
        days = duration.days
        period = (seconds//60 + days*24*60) // 30
        count = 0

        while count <= period:
            count = count+1
            print(self.last_date, self.last_period, count, period)
            if not self.get_data():
                break
