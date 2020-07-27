#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 10:11:13 2020

@author: vargthon
"""
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle
import codecs

class LinearModel():
    
    def __init__(self, id=0,product={}, company={} , model=LinearRegression(), error=0, params=[], valid_from=(datetime.now().timestamp()), valid_to=None):
        self.id = id
        self.model = model
        self.params = params
        self.valid_from = valid_from 
        self.valid_to = valid_to 
        self.product = product
        self.company = company
        self.error = error
    
    @property
    def model(self):
     #   return pickle.loads(codecs.decode(self._model.encode(), "base64"))
        return self._model
    @model.setter
    def model(self, model):
    #    self._model = self.encode(model)
        self._model = model
    @property
    def encoded(self):
        return codecs.encode(pickle.dumps(self._model), "base64").decode()
    
    
    def decode(self, model):
        return pickle.loads(codecs.decode(model.encode(), "base64"))

    def to_dict(self):
        return {
            "linear_model": self.encoded,
            "valid_from": self.valid_from,
            "valid_to": self.valid_to,
            "product": self.product,
            "company": self.company,
            "params": self.params
        }
    def params_value(self, params=[]):
        predict_array = []
        for x in range(len(self.params)):
            value = 0
            for y in range(len(params)):
                if self.params[x] == params[y]["param"]:
                    value = params[y]["value"]
            predict_array.append(value)

        return predict_array

    def predict_model(self, params=[]):
        if len(self.model.coef_) == 0:
            return 0
        predict = self.model.predict([self.params_value(params)])[0]
        if predict > 0:
            return predict 
        return 0
    def fit(self, X,y):
        self.model.fit(X,y)