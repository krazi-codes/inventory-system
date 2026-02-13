class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

    def get_product_id(self):
        return self.product_id

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def search_product(products, product_id):
        for product in products:
            if product.get_product_id() == product_id:
                return product
        return None
        
class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def get_customer_id(self):
        return self.customer_id

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def search_customer(customers, customer_id):
        for customer in customers:
            if customer.get_customer_id() == customer_id:
                return customer
        return None

class Order:
    def __init__(self, order_id, customer, product, quantity):
        self.order_id = order_id
        self.customer = customer
        self.product = product
        self.quantity = quantity

    def get_order_id(self):
        return self.order_id

    def calculate_total(self):
        return self.product.get_price() * self.quantity
    
    def display_order(order):
        return f"Order ID: {order.get_order_id()}, Customer: {order.customer.get_name()}, Total: {order.calculate_total()}"

class Employee:
    def __init__(self, employee_id, name, position):
        self.employee_id = employee_id
        self.name = name
        self.position = position

    def get_employee_id(self):
        return self.employee_id

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position
