from lib.productlearning import ProductLearning
from lib.salesproduct import SalesProduct 
from lib.salescompany import SalesCompany
from lib.period import Period

class ProductSalesLearned():

    def __init__(self, product=SalesProduct(), company=SalesCompany()):
        self.product = product
        self.company = company
        self.model = None
        self.product_learning = ProductLearning()

    def load_model(self, product, company, period=Period.MONTHLY):
        self.model = self.product_learning.load_linear(company, product, period)


    
    
