# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 17:14:21 2018

@author: sceac10
"""
import pandas as pd
import random

data = pd.read_csv("dataset.csv")

series = []

technology = data["powersystemresourcetype"].unique()

print(data.loc[(data["powersystemresourcetype"]=="Nuclear") & (data["settlementperiod"]==5), "quantity"].values[0])

#print(data.loc[data["powersystemresourcetype"]=="Solar", "quantity"].values)

index = random.randint(0,9)

for tech in technology:
    generation = {
            'name': tech,
            'data': data.loc[(data["powersystemresourcetype"]==tech) & (data["settlementperiod"]==index), "quantity"].values[0]
    }
    series.append(generation)
        


xAxis = {"categories": [str(x) for x in range(1,3,1)]}
    

data["Hour"]= ((data["settlementperiod"]-1)*30//60%24).map('{:02.0f}'.format)
data["Minute"]= ((data["settlementperiod"]-1)*30%60).map('{:02.0f}'.format)
data["settlementdate"]=data["settlementdate"].map(str)
data["full date"] = pd.to_datetime(data["settlementdate"]+" "+data["Hour"]+":"+data["Minute"], format="%Y-%m-%d %H:%M")
data["full date"]=pd.to_datetime(data["full date"], unit='ms')

data["full date"]=data["full date"]

print(data["full date"].dt.microsecond)