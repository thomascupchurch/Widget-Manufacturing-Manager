# costs.py
# Handles cost and markup management

class CostManager:
    def __init__(self):
        self.material_costs = {'paper': 0.0, 'vinyl': 0.0}
        self.ink_costs = {'black': 0.0, 'white': 0.0}
        self.markup = 0.0

    def set_material_cost(self, material, cost):
        if material in self.material_costs:
            self.material_costs[material] = cost

    def set_ink_cost(self, color, cost):
        if color in self.ink_costs:
            self.ink_costs[color] = cost

    def set_markup(self, markup):
        self.markup = markup

    def get_costs(self):
        return {'materials': self.material_costs, 'inks': self.ink_costs, 'markup': self.markup}
