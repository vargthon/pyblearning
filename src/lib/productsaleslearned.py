from lib.productlearning import ProductLearning
from lib.salesproduct import SalesProduct 
from lib.salescompany import SalesCompany

class ProductSalesLearned():

    def __init__(self, product=SalesProduct(), company=SalesCompany()):
        self.product = product
        self.company = company
        self.model = None

    def load_model(self, product, company):
        learning = ProductLearning()
        self.model = learning.load_linear(company, product)


    
    
