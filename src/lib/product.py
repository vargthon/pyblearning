from lib.company import Company
class Product():

    def __init__(self, description="", price=0.0, cost=0.0, actual_balance=0.0, 
                        weight=0.0, getin="", cod="",min_sales=0.0, company=Company()):
        self.description= description
        self.price = price 
        self.cost = cost 
        self.actual_balance = actual_balance 
        self.weight = weight
        self.getin = getin 
        self.cod = cod 
        self.min_sales = min_sales 
        self.company = company 