# customers.py
# Handles customer database

class CustomerDB:
    def __init__(self):
        self.customers = {}

    def add_customer(self, name, contact):
        self.customers[name] = {'contact': contact, 'orders': []}

    def add_order(self, name, order):
        if name in self.customers:
            self.customers[name]['orders'].append(order)

    def get_customer(self, name):
        return self.customers.get(name, None)

    def list_customers(self):
        return list(self.customers.keys())
