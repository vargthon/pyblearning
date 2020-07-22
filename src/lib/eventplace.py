#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 14:09:27 2020

@author: vargthon
"""

from datetime import datetime
import numpy as np
import pandas as pd
import calendar

class EventPlace():
    def event_search(self, initial_date, final_date):
        initial = []
        final = []
        desc = []
       # initial.append(datetime.strptime('2020-03-20', '%Y-%m-%d'))
       # initial.append(datetime.strptime('2020-03-20', '%Y-%m-%d'))
       # initial.append(datetime.strptime('2020-04-01', '%Y-%m-%d'))
        initial.append(datetime.strptime('2020-03-20', '%Y-%m-%d'))
       # initial.append(datetime.strptime('2020-06-01', '%Y-%m-%d'))
        final.append(None)
       # final.append(datetime.strptime('2020-03-30', '%Y-%m-%d'))
       # final.append(datetime.strptime('2020-04-30', '%Y-%m-%d'))
       # final.append(None)
       # final.append(datetime.strptime('2020-06-30', '%Y-%m-%d'))
        desc.append('COVID-19')
       # desc.append('DECRETO 1')
       # desc.append('DECRETO 2')
       # desc.append('AUXÍLIO GOVERNO')
       # desc.append('SEGUNDA PARCELA')
        dic = { 'EVENT': desc, 'INITIAL': initial, 'FINAL': final }
        df = pd.DataFrame(dic)
        return df
  
 #   def percent_effect(events, datas):
  #       for i, events in events.iterrows():
    
    def date_impact(self, init_date, end_date , start_event, end_event):
         if pd.isnull(end_event):
             end_event = datetime.now()
         if start_event > end_date or end_event < init_date:
             return 0
         else:
             if start_event >= init_date:
                 i = start_event 
             else:
                 i = init_date
             if end_event <= end_date:
                f = end_event
             else:
                 f = end_date
             return f - i
        
    def month_impact(self,month, start_event, end_event):
        init_date = datetime(datetime.now().year, month, 1)
        end_date = datetime(datetime.now().year, month, calendar.monthrange(datetime.now().year,month)[1])
        delta = end_date - init_date
        r = self.date_impact(init_date, end_date, start_event, end_event)
        if r == 0:
            return 0
        else:
            return round(r.days/delta.days,2)
    
    def apply_events(self, df):
        df_events = self.event_search(datetime.now(), datetime.now())
        if df.size != 0:
            for i, r in df_events.iterrows():
                df['EVENT:' + r.at['EVENT']] = df.apply(lambda row : self.month_impact(int(row['CALENDAR:MONTH']), r.at['INITIAL'], r.at['FINAL'] ), axis=1)
        
        return df
        