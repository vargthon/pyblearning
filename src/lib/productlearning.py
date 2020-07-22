#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 09:33:54 2020

@author: vargthon
"""
from lib.collector import Collector
from lib.normalizer import Normalizer
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from datetime import datetime
from lib.linearmodel import LinearModel
class ProductLearning():
    
    def __init__(self):
        self.collector = Collector()
        self.normalize = Normalizer()
        self.model = LinearModel()
        self.product = {}
        self.company = {}
        
            
    def fit_linear_monthly_product(self, codigoProduto, codigoFilial, features=[],target=None):
        self.company = {"cod": codigoFilial}
        df = self.collector.colector_mes(codigoProduto, codigoFilial)
        df = self.normalize.normalizar(df)
        if df.size > 0:
            self.product = {
                   "cod": df.loc[0,"KEY:PRODUTO:CODIGO"]
                }
        real_params = []
        for col in df.columns:
            column = col.split(":")
            if len(column) > 0:
                if column[0] == 'PARAMS':
                    real_params.append(col)
                if column[0] == 'CALENDAR' and column[1] != 'DATE':
                    real_params.append(col)
                if column[0] == 'EVENT':
                    real_params.append(col)
        X = df[real_params].values
        y = df['METRIC:QTD'].values
        if df.size != 0:
            self.model.fit(X,y)
            self.model.params = real_params
            #self.model = self.regression#pickle.dumps(self.regression)
    

        
    

            
                    

        
            
     
        


