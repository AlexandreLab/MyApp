import pandas as pd
from xml.etree import ElementTree
import datetime
import requests 

def get_rounded_time(date, base=5):
    time = date.time()
    minute = time.minute
    hour = time.hour
    minute = int(base * round(float(minute)/base))
        
    if minute==60:
        minute = 0
        hour =(hour+1)
        if hour == 24:
            hour = 0
            date = date+datetime.timedelta(days=1)
    return date, hour, minute

  
def get_time_params(fullTime):
    period = fullTime.hour*2+fullTime.minute//30
    date = fullTime.date()
    if period == 0:
        period = 48
        fulldate = (fullTime-datetime.timedelta(days=1))
    return date, period

def get_request(url, params):
    try:
        req=requests.get(url,params=params) 
        response_code = req.status_code
        print(response_code)
        if response_code == 204:
            print("No content returned, but no error reported.")

        elif response_code != 200:
            print("No data returned. Error reported.")

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        #sys.exit(1)
    return req 

class ElexonAPI(object):
    XML_MAPPING = None
    
    def __init__(self, apikey=None, url=None):
        self.version = 'v1'
        self.apikey = apikey
        self.url = url+"{}".format(self.version)
        date_time = datetime.datetime.now()-datetime.timedelta(hours=2) #Default time
        self.date_time = date_time
        self.data = pd.DataFrame()
        
    def get_data(self, params={}):
        return
        
    def request_data(self, params):
        params.update({
            'APIKey': self.apikey,
            'ServiceType':'xml'
        })
        print(params)
        response = get_request(self.url, params)
#         print(response.text)
        response_df = self.xml_to_df(response)
        return response_df
    
    def clear_data(self):
        self.data = pd.DataFrame()

    def get_full_historical_data(self, startDate):
        self.clear_data()
        self.get_historical_data(startDate, datetime.datetime.now())
        
    def get_historical_data(self, startDate, endDate):
        return
    
    def post_cleanup(self, df):
        return df
    
    def xml_to_df(self, req):
        tree = ElementTree.fromstring(req.text)
        data = []
        if tree[0][0].text == "200":
            for branch in tree.iter('item'):
                row=[]
                for col in self.XML_MAPPING:
                    #print(col)
                    row.append(branch.find(col).text.replace('"', ""))
                data.append(row)
            return pd.DataFrame(columns=self.XML_MAPPING, data=data)    
        else: return False
    
# Get data at 5min resolution
class FUELINST(ElexonAPI):
    """ Instant Generation by Fuel Type """
    XML_MAPPING = [
        #'recordType',
        #'startTimeOfHalfHrPeriod',
        'publishingPeriodCommencingTime',
        'settlementPeriod',
        'ccgt',
        'oil',
        'coal',
        'nuclear',
        'wind',
        'ps',
        'npshyd',
        'ocgt',
        'other',
        'intfr',
        'intirl',
        'intned',
        'intew',
        #'activeFlag'
    ]
    
    def __init__(self, apikey):
        report = 'FUELINST'
        url = "https://api.bmreports.com/BMRS/{}/".format(report.upper())
        super(FUELINST, self).__init__(apikey, url)                
       
    def get_historical_data(self, startDate, endDate):

        self.clear_data()
        fromDate, fromHour, fromMinute = get_rounded_time(startDate)
        toDate, toHour, toMinute = get_rounded_time(endDate)
                    
        params = {
            'FuelType':'',
            'FromDateTime': fromDate.strftime("%Y-%m-%d")+ " {:02d}:{:02d}:00".format(fromHour, fromMinute),
            'ToDateTime': toDate.strftime("%Y-%m-%d")+ " {:02d}:{:02d}:00".format(toHour, toMinute),
        }
        response_df = self.request_data(params)
        self.data = pd.concat([self.data, self.post_cleanup(response_df)], axis=1) 
        dt64 = self.data['publishingPeriodCommencingTime'].tail(1).values[0]
        
        #Add 5 minutes to the datetime of the last row
        self.date_time = pd.to_datetime(str(dt64))+datetime.timedelta(minutes=5) 

    #Return only the last set of data received
    def get_data(self):

        inDate, inHour, inMinute = get_rounded_time(self.date_time)

        params = {
            'FuelType':'',
            'FromDateTime': inDate.strftime("%Y-%m-%d")+ " {:02d}:{:02d}:00".format(inHour, inMinute),
            'ToDateTime': inDate.strftime("%Y-%m-%d")+ " {:02d}:{:02d}:00".format(inHour, inMinute),
        }
            
        response_df = self.request_data(params)
        if isinstance(response_df, pd.DataFrame):
            self.data = pd.concat([self.data, self.post_cleanup(response_df)], axis=0)
            
            dt64 = self.data['publishingPeriodCommencingTime'].tail(1).values[0]
            
            #Add 5 minutes to the datetime of the last row
            self.date_time = pd.to_datetime(str(dt64))+datetime.timedelta(minutes=5) 
            return True
        else: 
            print("No data currently available")
            return False
        
    def post_cleanup(self, df):
        #print(df)
        df.loc[:, 'settlementPeriod':] = df.loc[:, 'settlementPeriod':].apply(pd.to_numeric)
        df['publishingPeriodCommencingTime'] = pd.to_datetime(
                                                        df['publishingPeriodCommencingTime'], 
                                                        format="%Y-%m-%d %H:%M:%S"
                                                    )
        df.sort_values('publishingPeriodCommencingTime', inplace=True)
        return df

#Get data at 30min resolution
class B1620(ElexonAPI):
    
    #List of parameters to extract from the response
    XML_MAPPING = [
        'powerSystemResourceType',
        'quantity',
        'settlementPeriod',
        'settlementDate',
    ]
    
    def __init__(self, apikey):
        report = 'B1620'
        url = "https://api.bmreports.com/BMRS/{}/".format(report.upper())
        super(B1620, self).__init__(apikey, url)
    
    def get_historical_data(self, startDate, endDate):
        self.date_time = startDate
        date, period = get_time_params(startDate)
        self.clear_data()
        duration = endDate-startDate
        seconds = duration.seconds
        days = duration.days
        period = (seconds//60 + days*24*60) // 30
        count = 0

        while count <= period:
            count = count+1
            if not self.get_data():
                break
                
        
    def get_data(self, params={}):
        if not params:
            date, period = get_time_params(self.date_time )
            
            params = {
                'SettlementDate': date.strftime("%Y-%m-%d"),
                'Period': period,
            }
        response_df = self.request_data(params)
        if isinstance(response_df, pd.DataFrame):
            response_df = self.post_cleanup(response_df)
            response_df = response_df.set_index(["settlementDate","settlementPeriod", "powerSystemResourceType"]).unstack()
            response_df.reset_index(inplace=True)
            response_df.columns= ["Date", "Period"]+ list(response_df.columns.get_level_values(1).values)[2:]
            
            print(response_df)
            self.data = pd.concat([self.data, response_df], axis=0)
            
            self.date_time = self.date_time+datetime.timedelta(minutes=30)
        else: 
            print("No content returned, but no error reported. Retry later.")
            return False

        
    def post_cleanup(self, df):
        df.loc[:, ['quantity', 'settlementPeriod']] = df.loc[:, ['quantity', 'settlementPeriod']].apply(pd.to_numeric)
        df['settlementDate'] = pd.to_datetime(df['settlementDate'], format="%Y-%m-%d")
        return df
