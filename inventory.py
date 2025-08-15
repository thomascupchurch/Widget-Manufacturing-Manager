# inventory.py
# Handles material and ink inventory management

class Inventory:
    def __init__(self):
        self.materials = {'paper': 0, 'vinyl': 0}
        self.inks = {'black': 0, 'white': 0}

    def add_material(self, material, amount):
        if material in self.materials:
            self.materials[material] += amount

    def use_material(self, material, amount):
        if material in self.materials and self.materials[material] >= amount:
            self.materials[material] -= amount
            return True
        return False

    def add_ink(self, color, amount):
        if color in self.inks:
            self.inks[color] += amount

    def use_ink(self, color, amount):
        if color in self.inks and self.inks[color] >= amount:
            self.inks[color] -= amount
            return True
        return False

    def get_inventory(self):
        return {'materials': self.materials, 'inks': self.inks}
