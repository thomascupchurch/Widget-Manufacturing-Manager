# main.py
# Entry point for the production management system

from inventory import Inventory
from customers import CustomerDB
from costs import CostManager
from quotes import Quoter

# Initialize system
inventory = Inventory()
customers = CustomerDB()
costs = CostManager()
quoter = Quoter(costs)

# Example usage (replace with UI or CLI as needed)
if __name__ == "__main__":
    # Add inventory
    inventory.add_material('paper', 100)
    inventory.add_ink('black', 50)

    # Set costs and markup
    costs.set_material_cost('paper', 2.0)
    costs.set_ink_cost('black', 0.5)
    costs.set_markup(0.2)  # 20% markup

    # Add customer
    customers.add_customer('Acme Corp', 'acme@example.com')

    # Generate quote
    quote = quoter.generate_quote('paper', 10, 'black', 5)
    print(f"Quote for Acme Corp: ${quote}")
