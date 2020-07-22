from lib.repository.dbconnection import DBConnection
from lib.linearmodel import LinearModel

class LinearModelRepository():
    def __init__(self):
        self.dbconn = DBConnection()
    
    def save(self, model=LinearModel()):
        SQL = """ 
            INSERT INTO linear_model (
                product_id, 
                company_id,
                params, 
                valid_from, 
                valid_to, 
                model)
            VALUES
            ({product_id}, {company_id},{params}, {valid_from}, {valid_to}, {model})
        """
        self.dbconn.conn.cursor.execute(SQL.format(product_id=model.product.cod, 
            company_id=model.company.cod,valid_from=model.valid_from, 
            valid_to=model.valid_to, model=model.model ))
        self.dbconn.close()

    def load(self, model_id):
        
