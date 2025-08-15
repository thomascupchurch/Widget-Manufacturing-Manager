# quotes.py
# Handles quoting logic

class Quoter:
    def __init__(self, cost_manager):
        self.cost_manager = cost_manager

    def generate_quote(self, material, material_qty, ink, ink_qty):
        costs = self.cost_manager.get_costs()
        base = (costs['materials'].get(material, 0) * material_qty) + (costs['inks'].get(ink, 0) * ink_qty)
        total = base * (1 + costs['markup'])
        return round(total, 2)
