class Asset:
    def __init__(self, init_qty, name, number):
        self.init_qty = init_qty
        self.name = name
        self.number = number

        self.total_quantity = self.init_qty

    def __repr__(self):
        return f"Name: {self.name} Number: {self.number} Init: {self.init_qty}," \
               f" total_quantity: {self.total_quantity}"


