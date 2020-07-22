#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 20:46:31 2020

@author: vargthon
"""

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from lib.eventplace import EventPlace
from lib.calendarnormalize import CalendarNormalize


class Normalizer():
    
        
    def normalizar(self, df):
        eventplace = EventPlace()
        calendarnormalize = CalendarNormalize()
        length = df['CALENDAR:DATE'].size
        seq = []
        for x in range(length):
            seq.append(x+1)
        dic = { 'PARAMS:SEQ': seq }
        df2 = pd.DataFrame(dic)
        df = self.add_months(df)
        df = eventplace.apply_events(df)
        df = calendarnormalize.month_to_fitures(df, 'CALENDAR:MONTH')
        return df.join(df2)
    
    #def event_add(self, df):
        
    def add_months(self, df):
        months = []
        for i, row in df.iterrows():
            months.append(datetime.fromtimestamp(row.at['CALENDAR:DATE']).month)
        dic = {'CALENDAR:MONTH': months}
        df2 = pd.DataFrame(dic)
        ndf = df.join(df2)   
     
        return ndf
    
    