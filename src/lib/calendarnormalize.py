#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 16:01:05 2020

@author: vargthon
"""

import numpy as np
import pandas as pd

class CalendarNormalize():
    def month_to_fitures(self, df, month_column):
        return pd.get_dummies(df, columns=[month_column], prefix_sep=':')
        