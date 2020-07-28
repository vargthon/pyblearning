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
from lib.repository.linearmodelrepository import LinearModelRepository
from lib.period import Period
class ProductLearning():
    
    def __init__(self):
        self.collector = Collector()
        self.normalize = Normalizer()

    
    def load_linear(self, company, product):
        repository = LinearModelRepository()
        model = repository.load_valid(product,company)
        if len(model.params) > 0:
            model = model
            product = model.product
            company = model.company 
        else:
            model = self.fit_linear_product(product,company)
            model.company = {"cod": company}
            model.product = {"cod": product}
            repository.save(model)
        
        return model 
    
            
    def fit_linear_product(self, codigoProduto, codigoFilial, features=[],target=None, training_date_from=datetime.now().timestamp(),
        training_date_to=datetime.now().timestamp(), period=Period.MONTHLY):
        company = {"cod": codigoFilial}
        df = self.collector.colector_mes(codigoProduto, codigoFilial)
        df = self.normalize.normalizar(df)
        model = LinearModel()
        if df.size > 0:
            product = {
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
            model.fit(X,y)
            model.params = real_params
            model.training_date_from = training_date_from
            model.training_date_to = training_date_to
            model.period = period
            #self.model = self.regression#pickle.dumps(self.regression)
        
        return model
    

        
    

            
                    

        
            
     
        


