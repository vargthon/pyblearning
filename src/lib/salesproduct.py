from lib.salescompany import SalesCompany
class SalesProduct():

    def __init__(self, description="", price=0.0, cost=0.0, actual_balance=0.0, 
                        weight=0.0, getin="", cod="",min_sales=0.0, company=SalesCompany()):
        self.description= description
        self.price = price 
        self.cost = cost 
        self.actual_balance = actual_balance 
        self.weight = weight
        self.getin = getin 
        self.cod = cod 
        self.min_sales = min_sales 
        self.company = company 