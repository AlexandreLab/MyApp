# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 17:14:21 2018

@author: sceac10
"""
import pandas as pd

data = pd.read_csv("dataset.csv")

series = []

technology = data["powersystemresourcetype"].unique()

#print(data.loc[(data["settlementperiod"]==1) & (data["powersystemresourcetype"]=="Solar"), "quantity"].values[0])

#print(data.loc[data["powersystemresourcetype"]=="Solar", "quantity"].values)

for i in range(1, 2, 1):
    for tech in technology:
        #print(i, tech)
        generation = {
                'name': tech,
                'data': data.loc[data["powersystemresourcetype"]==tech, "quantity"].values.tolist(),
        }
        
        
        
        
        series.append(generation)


xAxis = {"categories": [str(x) for x in range(1,3,1)]}
    

data["full date"] = data["settlementdate"]+" "+data["settlementperiod"].astype(str)


xAxis = {"categories": data["full date"].unique().tolist()}

print(xAxis)