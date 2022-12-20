money = {"Binance": {"USDT": 0.0, "BTC": 0.025}, "Coinbase": {"USDT": 1000.0, "BTC": 0.0}}

discount = 0.995


def check_money(money, current_price_binance, current_price_coinbase):
    if current_price_binance * money["Binance"]["BTC"] > 0 and current_price_coinbase * money["Coinbase"]["USDT"] > 0:
        money["Binance"]["USDT"] = money["Binance"]["BTC"] * current_price_binance * discount
        money["Binance"]["BTC"] = 0
        money["Coinbase"]["BTC"] = (money["Coinbase"]["USDT"] / current_price_coinbase) * discount
        money["Coinbase"]["USDT"] = 0
        print(f'Binance USDT: {money["Binance"]["USDT"]:.2f}')
        print(f'Coinbase BTC: {money["Coinbase"]["BTC"]:.6f}')
    elif current_price_binance * money["Binance"]["USDT"] > 0 and current_price_coinbase * money["Coinbase"]["BTC"] > 0:
        money["Binance"]["BTC"] = (money["Binance"]["USDT"] / current_price_binance) * discount
        money["Binance"]["USDT"] = 0
        money["Coinbase"]["USDT"] = money["Coinbase"]["BTC"] * current_price_coinbase * discount
        money["Coinbase"]["BTC"] = 0
        print(f'Binance BTC: {money["Binance"]["BTC"]:.6f}')
        print(f'Coinbase USDT: {money["Coinbase"]["USDT"]:.2f}')
    else:
        print("Transaction not possible!")
    price_inputs()


def price_inputs():
    current_price_binance = float(input("Enter price binance"))
    current_price_coinbase = float(input("Enter price coin base"))
    check_money(money, current_price_binance, current_price_coinbase)


price_inputs()
