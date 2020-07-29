from lib.productlearning import ProductLearning
from lib.product import Product 
from lib.company import Company
from lib.period import Period

class ProductSalesLearned():

    def __init__(self, product=Product(), company=Company()):
        self.product = product
        self.company = company
        self.model = None
        self.product_learning = ProductLearning()

    def load_model(self, product, company, period=Period.MONTHLY):
        self.model = self.product_learning.load_linear(company, product, period)


    
    
