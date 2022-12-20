class Asset:
    def __init__(self, name, qty):
        self.name = name
        self.qty = qty
        self.init_qty = qty
        self.buffer_qty = 0

    def __str__(self):
        if self.init_qty != 0:
            ratio = (self.qty/ self.init_qty - 1) * 100
            return f'-------------\n {self.qty} {self.name}\n' \
                   f'Печалба: {ratio:.2f}%'
        return f'{self.name}: {self.init_qty}'