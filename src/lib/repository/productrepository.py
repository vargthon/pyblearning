from lib.product import Product 
from lib.repository.dbconnection import DBConnection

class ProductRepository():

    def __init__(self):
        self.dbconn = DBConnection()
    
    def load(cod, company_id): #Code can be getin or product_id
        
