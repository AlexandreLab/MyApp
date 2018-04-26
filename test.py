# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 17:14:21 2018

@author: sceac10
"""
import pandas as pd

data = pd.read_csv("dataset.csv")

generation_data = []

technology = data["powersystemresourcetype"].unique()

#print(data.loc[(data["settlementperiod"]==1) & (data["powersystemresourcetype"]=="Solar"), "quantity"].values[0])


for i in range(1, 2, 1):
    for tech in technology:
        #print(i, tech)
        generation = {
                'source': tech,
                'date' : data.loc[(data["settlementperiod"]==i) & (data["powersystemresourcetype"]==tech), "settlementdate"].values[0],
                'period': i,
                'value': data.loc[(data["settlementperiod"]==i) & (data["powersystemresourcetype"]==tech), "quantity"].values[0],
        }
        
    
        generation_data.append(generation)

print(generation)
#print(generation_data)