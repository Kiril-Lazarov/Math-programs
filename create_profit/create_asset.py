class Asset:

    def __init__(self, name, qty, base_qty= 0):
        self.name = name
        self.qty = qty
        self.base_qty = base_qty
        self.init_qty = self.base_qty
def get_total_qties():
    total_btc = btc.qty + usdt.qty / base_price
    total_usdt = usdt.qty + btc.qty * base_price
    return total_btc, total_usdt

def change_base_profit_asset(price , base_price):
    if price > base_price:
        usdt.base_qty = usdt.qty + btc.qty * price

    elif price < base_price:
        btc.base_qty = btc.qty + usdt.qty/ price

def take_limits(btc_test_qty, usdt_test_qty):
    down_price = usdt_test_qty / ((btc.base_qty * level) - btc_test_qty)
    up_price = ((usdt.base_qty * level) - usdt_test_qty) / btc_test_qty
    return up_price, down_price

def get_asset_to_cut(price, base_price):
    if price > base_price:
        asset_to_cut = 'USDT'
    else:
        asset_to_cut = 'BTC'
    return asset_to_cut

# def get_coefficient(asset_to_cut, price):

def make_appropriate_transaction(price, asset_to_cut):
    btc_test_qty = btc.qty
    usdt_test_qty = usdt.qty

    for coefficient in range(1, 101):
        coefficient *=0.01
        if asset_to_cut == 'BTC':
            trade_qty = btc_test_qty * coefficient
            btc_test_qty -= trade_qty
            usdt_test_qty += trade_qty * price
        else:
            trade_qty = usdt_test_qty * coefficient
            usdt_test_qty -= trade_qty
            btc_test_qty += trade_qty / price

        up_price, down_price = take_limits(btc_test_qty, usdt_test_qty)
        down_limit = price -2
        up_limit = price + 2
        average = (up_price + down_price) / 2
        if not down_limit<= average <= up_limit:
            btc.qty, usdt.qty = btc_test_qty, usdt_test_qty
            print(f'BTC: {btc.qty}\nUSDT: {usdt.qty}')
            up_diff = up_price - price
            down_diff = price - down_price
            print(f'Up diff: {up_diff}\nDown diff: {down_diff}')
            return up_price, down_price, coefficient
        btc_test_qty = btc.qty
        usdt_test_qty = usdt.qty




base_price = 20000
level = 1.001
usdt = Asset('USDT', 1000)
btc = Asset('BTC', 0.05)
btc.base_qty, usdt.base_qty =  get_total_qties()
btc.init_qty, usdt.init_qty = btc.base_qty, usdt.base_qty
# take_qty = usdt.qty*0.199
# print(btc.base_qty)
# print(usdt.base_qty)
# price = base_price/ level
# print(f'Curr price : {price:.2f}')
# change_base_profit_asset(price, base_price)
# usdt.qty -= take_qty
# btc.qty += take_qty / price
# # usdt.qty += take_qty * price
# down_price = usdt.qty / ((btc.base_qty * level) - btc.qty)
# up_price = ((usdt.base_qty * level) - usdt.qty) / btc.qty
# print(btc.base_qty)
# print(usdt.base_qty)
#
# print('----------------------')
# print(f'Up price: {up_price:.2f}')
# print(f'Diff {up_price - price:.2f}')
# print(f'Down price: {down_price:.2f}')
# print(f'Diff {price- down_price:.2f}')
# print(f'{base_price*level:.2f}')
# change_base_profit_asset(base_price * level, base_price)
# asset_to_cut = get_asset_to_cut(base_price * level, base_price)
# print(make_appropriate_transaction(base_price * level, asset_to_cut))
print(f'Горна цена: {base_price * level:.2f}\nДолна цена: {base_price/level:.2f}')
while True:

    curr_price = float(input('Въведи цена: '))
    change_base_profit_asset(curr_price, base_price)
    asset_to_cut = get_asset_to_cut(curr_price, base_price)
    print(make_appropriate_transaction(curr_price, asset_to_cut))
    base_price = curr_price
    total_btc, total_usdt = get_total_qties()
    print(f'Печалба BTC: {(total_btc/ btc.init_qty - 1) * 100:.2f}%\n'
          f'Печалба USDT: {(total_usdt/ usdt.init_qty -1) * 100:.2f}%')


