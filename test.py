# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 17:14:21 2018

@author: sceac10
"""
import pandas as pd

import config as conf
import random
import ElexonAPI
from datetime import datetime, timedelta


#api = ElexonAPI.ElexonAPI(conf.APIKEY)
#
#date=datetime.now()-timedelta(hours=4)
#
#startDate=datetime.now()-timedelta(hours=10)
#endDate=datetime.now()-timedelta(hours=4)
#api.get_historical_data(startDate, endDate)


test= -5

#print(api.data.loc[api.data.index == "Solar", :].values.tolist()[0])
#print(api.data.loc[api.data.index == "Solar", :].values.tolist()[0][test:])

#series = []
#for tech in api.data.index:
#    generation = {
#            'name': tech,
#            'data': api.data.loc[api.data.index == tech, :].values.tolist()[-30],
#    }
#    series.append(generation)
#
#print(series)

#print(api.data.columns[-30])




startDate = datetime.now() - timedelta(hours=30)

duration = datetime.now()-startDate
seconds = duration.seconds
days = duration.days
period = (duration.seconds//60 + days*24*60) // 30
print(period)


