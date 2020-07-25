#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 20:37:32 2020

@author: vargthon
"""

#from elasticsearch import Elasticsearch
#from elasticsearch import helpers
from lib.repository.dbconnection import DBConnection
from datetime import datetime
from lib.linearmodel import LinearModel
import numpy as np
import pandas as pd


class Collector:
    #def __init__(self):
        #self.es_client = Elasticsearch(http_compress=True, http_auth=('elastic', 'changeme'))

    def colector_mes(self, produto, empresa):
      db = DBConnection()
      cursor = db.conn.cursor()
      cursor.execute(
            """ 
            select 
              d.year,
              d.month,
              f.id_produto,
              sum(f.quantidade) as quantidade
            from 
              fact_sales_by_product as f, dim.date as d
            where 
              f.date_id = d.date_id
              and f.id_produto = '{0}'
              and f.id_empresa = '{1}'
              and f.date_id < '20200701'
              
            group by 
              d.year, d.month, f.id_produto
            order by
            d.year , d.month          
          """.format(produto, empresa, '2020', '06')
      )

      qtd = []
      data = []
      produtos = []
      for record in cursor:
        qtd.append(record[3])
        produtos.append(record[2])
        data.append(int(datetime(record[0], record[1], 1).timestamp()))
      dic = {'KEY:PRODUTO:CODIGO': produtos,
               'CALENDAR:DATE': data, 'METRIC:QTD': qtd}
      df = pd.DataFrame(dic)
      db.conn.close()
      return df

    