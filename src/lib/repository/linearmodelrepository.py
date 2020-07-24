from lib.repository.dbconnection import DBConnection
from lib.linearmodel import LinearModel
from datetime import datetime
class LinearModelRepository():
    def __init__(self):
        self.dbconn = DBConnection()
    
    def save(self, model=LinearModel()):
        params_list = str(model.params)
        params = params_list.replace('[','{').replace(']','}').replace('\'','\"')
        SQL = """ 
            INSERT INTO linear_model (
                product_id, 
                company_id,
                params, 
                valid_from, 
                valid_to, 
                model)
            VALUES
            ('{product_id}', '{company_id}','{params}', '{valid_from}', NULL, '{model}')
        """
        try:
            self.dbconn.conn.cursor().execute(SQL.format(product_id=model.product["cod"], 
                company_id=model.company["cod"],valid_from=datetime.fromtimestamp(model.valid_from), 
                valid_to=model.valid_to, model=model.encoded, params=params ))
            self.dbconn.conn.commit()
        except Exception as error:
            print(error)
        self.dbconn.close()

    def load_model(self, model_id):
        return None

