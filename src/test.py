from lib.linearmodel import LinearModel
from lib.repository.dbconnection import DBConnection
from lib.collector import Collector
linear = LinearModel()

db = DBConnection()



collector = Collector()
print(collector.colector_mes('0100102000', '020101'))

print(linear.to_dict())

