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

    def acompanhamento_mes(self, produto, empresa):
        response = self.es_client.search(
            index='loja_venda_item_produto',
            body={
                  "query": {
                      "bool": {
                          "must": [],
                          "filter": [
                              {
                                  "term": {
                                      "codigo.keyword": produto
                                  }
                              },
                              {
                                  "term": {
                                      "filial.keyword": empresa
                                  }
                              },
                              {
                                  "range": {
                                      "@timestamp": {
                                          "time_zone": "-03:00",
                                          "gte": "2020-06-01",
                                          "lt": "2020-07-01"
                                      }
                                  }
                              }

                          ]
                      }
                  },
                "size": 0,
                "aggs": {
                      "quantidade_vendida": {
                          "date_histogram": {
                              "field": "@timestamp",
                              "time_zone": "-03:00",
                              "calendar_interval": "day"
                          },
                          "aggs": {
                              "qtd": {
                                  "sum": {
                                      "field": "quantidade"
                                  }
                              }
                          }
                      }
                  }
            }
        )
        qtd = []
        data = []
        produtos = []
        for bucket in response['aggregations']['quantidade_vendida']['buckets']:
            #data.append(datetime.fromtimestamp((bucket['key']/1000) + (60 * 60 * 3)))
            data.append(datetime.fromtimestamp((bucket['key']/1000)))
            qtd.append(bucket['qtd']['value'])
            produtos.append(produto)
        dic = {'KEY:PRODUTO:CODIGO': produtos,
               'CALENDAR:DATE': data, 'METRIC:QTD': qtd}
        df = pd.DataFrame(dic)
        return df

    def produtos(self, produto, empresa):
        response = self.es_client.search(
            index='loja_venda_item_produto',
            body={
                "query": {
                    "bool": {
                        "must": [
                        ],
                        "filter": [
                            {
                                "term": {
                                    "filial.keyword": empresa
                                }
                            },
                            {
                                "term": {
                                    "descricao": produto
                                }
                            }
                        ]
                    }
                },
                "size": 0,
                "aggs": {
                    "produtos": {

                        "terms": {

                            "field": "descricao.keyword",
                            "min_doc_count": 1,
                            "size": 10000,
                            "order": {
                                "_count": "desc"
                            }

                        }, "aggs": {

                            "valor_total": {
                                "sum": {
                                    "field": "valor"
                                }

                            },
                            "quantidade_total": {
                                "sum": {
                                    "field": "quantidade"
                                }

                            },
                            "other_fields": {
                                "top_hits": {
                                    "size": 1,
                                    "_source": {
                                        "includes": ["codigo", "descricao", "loja", "filial"]
                                    }
                                }
                            }
                        }

                    }
                }

            }
        )
        codigo = []
        descricao = []
        filial = []
        for bucket in response['aggregations']['produtos']['buckets']:
            codigo.append(bucket["other_fields"]["hits"]
                          ["hits"][0]["_source"]["codigo"])
            descricao.append(bucket["key"])
            filial.append(bucket["other_fields"]["hits"]
                          ["hits"][0]["_source"]["filial"])
        dic = {'KEY:PRODUTO:CODIGO': codigo,
               'KEY:PRODUTO:DESCRICAO': descricao, 'KEY:PRODUTO:FILIAL': filial}
        df = pd.DataFrame(dic)
        return df

    def load_model(self, filialCode, productCode):
        response = self.es_client.search(
            index='monthly_models',
            body={
                "size": 1,
                  "query": {
                      "bool": {
                          "must_not": [
                              {
                                  "exists": {
                                      "field": "MONTHLY.valid_to"
                                  }
                              }
                          ],
                          "filter": [
                              {
                                  "term": {
                                      "PRODUCT.cod": productCode
                                  }
                              },
                              {
                                  "term":
                                  {
                                      "COMPANY.cod": filialCode
                                  }
                              }
                          ]
                      }
                  }
            }
        )

        if len(response["hits"]["hits"]) == 0:
            return None
        else:
            rs = response["hits"]["hits"][0]["_source"]
            linear = LinearModel(product=rs["PRODUCT"], company=rs["COMPANY"],
                                 params=rs["MONTHLY"]["params"], valid_from=rs["MONTHLY"]["valid_from"],
                                 valid_to=rs["MONTHLY"]["valid_to"])
            linear.model = linear.decode(rs["MONTHLY"]["linear_model"])
            return linear

    def save_model(self, model):
        helpers.bulk(self.es_client, [model])
