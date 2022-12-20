import asyncio
import time

# from binance.client import Client

api_key = ""
api_secret = ""

# client = Client(api_key, api_secret)
print('Processing...')
number_to_div = 3
percentage = 1.0025
# initial_price = client.get_symbol_ticker(symbol="BTCUSDT")
initial_price = {"price":"32736.39"}
commission = 1
upper_limit = float(initial_price['price']) * percentage
lower_limit = float(initial_price['price'])/ percentage
price_dict = {"Init": initial_price, "Low": lower_limit,
              "Up": upper_limit}  # Речник с долна и горна граница за търговия
quantities_dict = {"USDT": 848.55, "BTC": 0.025986}  # Речник с наличности BTC/USDT
start_sum_usdt = float(f'{quantities_dict["USDT"] * 2:.2f}')
start_sum_btc = float(f'{quantities_dict["BTC"] * 2:.6f}')
start_bgn = start_sum_usdt * 1.73
start_usdt = quantities_dict['USDT']
start_btc = quantities_dict["BTC"]
waiting_bitcoin_trades = []  # Списък с чакащите печалба търгувани количества USDT
waiting_usdt_trades = []  # СПисък с чакащите печалба търгувани количества BTC
count = [0]


def execution_report(quantity, side, is_first, price):
    profit_list = []
    if is_first:
        is_first = False
        count[0] += 1
    elif not is_first:
        count[0] += 1
    print(f'Транзакция номер: {count[0]}')
    if side == "Sell":
        print("SELL!!!")
        profit_quantity = quantity * price * commission
        print(f'Транзакция {quantity:.6f} BTC -> {profit_quantity:.2f} USDT на цена {price_dict["Init"]}')

    elif side == "Buy":
        print("BUY!!!")
        profit_quantity = quantity / price * commission
        print(f'Транзакция {quantity:.2f} USDT -> {profit_quantity:.6f} BTC на цена {price_dict["Init"]}')

    print(f'Списък биткойн: {waiting_bitcoin_trades}')
    print(f'Списък USDT: {waiting_usdt_trades}')
    print(f'Следваща горна граница-цена: {price_dict["Up"]:.2f}')
    print(f'Следваща долна граница-цена: {price_dict["Low"]:.2f}')
    profit_activ_usdt = ((2 * quantities_dict["USDT"] / start_sum_usdt) - 1) * 100
    profit_activ_btc = ((2 * quantities_dict["BTC"] / start_sum_btc) - 1) * 100
    profit_list.append(profit_activ_usdt)
    profit_list.append(profit_activ_btc)
    print(f'Наличност USDT: {quantities_dict["USDT"]:.2f}       печалба: {profit_activ_usdt:.2f}%')
    print(f'Наличност BTC: {quantities_dict["BTC"]:.6f}       печалба: {profit_activ_btc:.2f}%')

    sum_usdt = quantities_dict["USDT"] + quantities_dict["BTC"] * price_dict["Init"] * commission
    sum_btc = quantities_dict["BTC"] + quantities_dict["USDT"] / price_dict["Init"] * commission
    sum_bgn = sum_usdt * 1.73

    profit_usdt = (sum_usdt / start_sum_usdt - 1) * 100
    profit_btc = (sum_btc / start_sum_btc - 1) * 100
    profit_bgn = (sum_bgn / start_bgn - 1) * 100
    profit_list.append(sum_usdt)
    profit_list.append(profit_usdt)
    profit_list.append(sum_btc)
    profit_list.append(profit_btc)
    profit_list.append(sum_bgn)
    profit_list.append(profit_bgn)
    print(f'Обща сума USDT: {sum_usdt:.2f}         печалба: {profit_usdt:.2f}%')
    print(f'Обща сума BTC: {sum_btc:.6f}         печалба: {profit_btc:.2f}%')
    print(f'Обща сума BGN: {sum_bgn:.2f}         печалба: {profit_bgn:.2f}%')
    print()
    print()


# Дели наличната сума BTC или USDT на две, нулира списъците с чакащите печалба суми, за да може цикълът
# да зпочне отново.
# Ако asset е USDT това означава, че USDT е изчерпано за търговия и ще се дели на две наличният BTC. И обратно.
def split_func(price, asset):
    waiting_usdt_trades.clear()
    waiting_bitcoin_trades.clear()
    if asset == "USDT":
        current_btc = quantities_dict['BTC'] / 2  # Дели на две BTC.
        quantities_dict['BTC'] /= 2
        new_quantity_usdt = current_btc * price
        quantities_dict['USDT'] = new_quantity_usdt  # Определяне на новото количество USDT
    elif asset == "BTC":
        current_usdt = quantities_dict['USDT'] / 2  # Дели на две USDT.
        quantities_dict['USDT'] /=2
        new_quantity_btc = current_usdt / price
        quantities_dict['BTC'] = new_quantity_btc
    print("Split!!!!")
    print(f'Количество USDT: {quantities_dict["USDT"]}')
    print(f'Количество BTC: {quantities_dict["BTC"]}')
    print()


def calculate_new_quantities(asset, quantity, price, transaction_type):
    if asset == "USDT":
        quantities_dict[
            "BTC"] += quantity / price * commission  # Добавяне на търгуваното количество USDT към наличния BTC
        quantities_dict["USDT"] -= quantity  # Изваждане на търгуваното количество USDT от наличния USDT
        if transaction_type != "Take profit":
            waiting_bitcoin_trades.append(
                quantity / price * commission)  # Добавяне на чакащо печалба количество USDT към BTC списъка
    elif asset == "BTC":
        quantities_dict[
            "USDT"] += price * quantity * commission  # Добавяне на търгуваното количество BTC към наличното USDT
        quantities_dict["BTC"] -= quantity  # Изваждане на търгуваното количество BTC от наличния BTC
        if transaction_type != "Take profit":
            waiting_usdt_trades.append(
                quantity * price * commission)  # Добавяне на чакащо печалба количество BTC към USDT списъка


# Определяне на количеството криптовалута, което ще бъде търгувано
def define_quantity(crypto, price, transaction_type):
    quantity = 0
    if crypto == "USDT":
        index = len(waiting_bitcoin_trades)
        if index == number_to_div:
            split_func(price, "USDT")
            index = 0
        factor = (1 / (number_to_div - index))  # Множител за цената
        quantity = quantities_dict["USDT"] * factor  # Количество USDT, което ще бъде търгувано
        calculate_new_quantities("USDT", quantity, price, transaction_type)
    elif crypto == "BTC":
        index = len(waiting_usdt_trades)
        if index == number_to_div:
            split_func(price, "BTC")
            index = 0
        factor = (1 / (number_to_div - index))  # Множител за цената
        quantity = quantities_dict["BTC"] * factor  # Количество BTC, което ще бъде търгувано
        calculate_new_quantities("BTC", quantity, price, transaction_type)

    return quantity


# Изпълнение. Проверка дали има чакащи печалби поръчки в писъците за биткойн и долар.
def order_execution(price, side):
    is_first = True
    transaction_type = ''  # Тип транзакция - дали идва като печалба на предишна транзацкия или не
    if side == "Buy":
        if len(waiting_usdt_trades) == 0:
            quantity = define_quantity("USDT", price, transaction_type)
        else:
            if len(waiting_usdt_trades) == number_to_div: # Проверява дали дължината на списъка е равна на избраното
                # число
                quantity = define_quantity("USDT", price, transaction_type)
            else:
                transaction_type = 'Take profit'
                quantity = waiting_usdt_trades[-1]
                calculate_new_quantities("USDT", quantity, price, transaction_type)
                del waiting_usdt_trades[-1]
    else:
        if len(waiting_bitcoin_trades) == 0:
            quantity = define_quantity("BTC", price, transaction_type)
        else:
            if len(waiting_bitcoin_trades) == number_to_div:
                quantity = define_quantity("BTC", price, transaction_type)
            else:
                transaction_type = 'Take profit'
                quantity = waiting_bitcoin_trades[-1]
                calculate_new_quantities("BTC", quantity, price, transaction_type)
                del waiting_bitcoin_trades[-1]
    price_dict["Init"] = price  # Промяна на стара цена с нова цена
    price_dict["Low"] = price / percentage  # Промяна на долна граница за търговия
    price_dict["Up"] = price * percentage  # промяна на горна граница за търговия

    execution_report(quantity, side, is_first, price)


async def check_price(price):
    price = float(price)
    if price >= price_dict["Up"]:
        price = price_dict['Up'] # Цената за търговия се приравнява на горната граница на миналата цена
        order_execution(price, "Sell")

    elif price <= price_dict["Low"]:
        price = price_dict["Low"] # Цената за търговия се приравнява на долната граница на миналата цена
        order_execution(price, "Buy")


async def main():
    while True:
        # info = client.get_symbol_ticker(symbol="BTCUSDT")
        info = {'price': "31849"}
        await check_price(info["price"])
        time.sleep(1)


asyncio.run(main())
