class Asset:
    def __init__(self, init_qty, real_quantity, name, number):
        self.init_qty = init_qty
        self.name = name
        self.number = number
        self.real_quantity = real_quantity

    def __repr__(self):
        return f"Name: {self.name} Number: {self.number} Init: {self.init_qty}," \
               f" real_quantity: {self.real_quantity}"


