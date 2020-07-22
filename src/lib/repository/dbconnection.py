import psycopg2
from lib.repository.dbconfig import config
class DBConnection():

    def __init__(self):
        self.params = config()
        self.conn = None
        self.create_connection()
        

    def create_connection(self):
        try:
            self.conn = psycopg2.connect(**self.params)
        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while connecting to PostgreSQL", error)

    def close(self):
        self.conn.close()