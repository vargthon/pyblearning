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
            self.dbconn.create_connection()
            self.dbconn.conn.cursor().execute(SQL.format(product_id=model.product["cod"], 
                company_id=model.company["cod"],valid_from=datetime.fromtimestamp(model.valid_from), 
                valid_to=model.valid_to, model=model.encoded, params=params ))
            self.dbconn.conn.commit()
        except Exception as error:
            print(error)
        finally:
            self.dbconn.close()

    def load_valid(self, product_id, company_id):
        SQL =  """ 
            SELECT 
                product_id,
                company_id,
                model,
                params,
                valid_from,
                valid_to,
                id
            FROM 
                linear_model
            WHERE 
                valid_to is null  
                and company_id='{company_id}'
                and product_id='{product_id}'
			order by id desc
            limit 1
        """ 
        try:
            self.dbconn.create_connection()
            cursor = self.dbconn.conn.cursor()
            cursor.execute(SQL.format(company_id=company_id,product_id=product_id))
            model = LinearModel()
            for record in cursor.fetchall():
                model.params = record[3]
                model.product = {"cod": record[0]}
                model.company = {"cod": record[1]}
                model.model = model.decode(record[2])
                model.valid_from = record[4]
                model.valid_to = record[5]
                model.id = record[6]
            return model
        except Exception as error:
            print(error)
        finally:
            cursor.close()        

    def load_by_id(self, id):
        SQL =  """ 
            SELECT 
                product_id,
                company_id,
                model,
                params,
                valid_from,
                valid_to,
                id
            FROM 
                linear_model
            WHERE 
                id = {id} 
                and valid_to is null   
        """ 
        try:
            self.dbconn.create_connection()
            cursor = self.dbconn.conn.cursor()
            cursor.execute(SQL.format(id=id))
            model = LinearModel()
            for record in cursor.fetchall():
                model.params = record[3]
                model.product = {"cod": record[0]}
                model.company = {"cod": record[1]}
                model.model = model.decode(record[2])
                model.valid_from = record[4]
                model.valid_to = record[5]
                model.id = record[6]
            
            return model
        except Exception as error:
            print(error)
        finally:
            cursor.close()
    
    def update(self, model):
        params_list = str(model.params)
        params = params_list.replace('[','{').replace(']','}').replace('\'','\"')
        SQL = """ 
            UPDATE linear_model SET 
                valid_to = '{valid_to}',
                model = '{model}',
                valid_from = '{valid_from}',
                params='{params}'         
            WHERE
                id = {id}
        """
        try:
            self.dbconn.create_connection()
            self.dbconn.conn.cursor().execute(SQL.format(valid_to=datetime.fromtimestamp(model.valid_to),
             id=model.id, model= model.encoded, valid_from=model.valid_from, params=params ))
            self.dbconn.conn.commit()
        except Exception as error:
            print(error)
        finally:
            self.dbconn.close()

    def finish_model(self, model):
        now = datetime.now().timestamp()
        model.valid_to = now 
        self.update(model)
        
