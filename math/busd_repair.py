from collections import deque
import time
from binance.client import Client

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)

transaction_count = [0]
init_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])  # Взимане на първоначалната цена от борсата
number_trades = 10
percentage = 1.0005  # Процент за нивата на цените
profit_percentage = (percentage ** 2 + percentage ** 3) / 2  # Определя процентът печалба от чакащите количества на база
# като средноаритметичното между цените на третата и четврътата поред транзацкии.
# floating_system_profit_percentage = 1.001  # Процент печалба за системата без фиксирани печалби
busd_quantity = [1630, True]  # True или False определя дали бусд е главна валута
btc_quantity = [0]
repo_asset = deque()  # Съдържа чакащите печалба суми - може да са биткойн, може да са бусд. Ще се добавят речници.
list_traded_prices = deque([])  # Дек с цените на които е търгувано до момента
traded_busd_qty = deque()  # Два списъка за сранение.
traded_btc_qty = deque()
asset_on_charge = ''  # Указава коя от валутите е главна към момента

# Променливи за принта
initial_qty_busd = busd_quantity[0]  # Първоначални количества
initial_qty_btc = btc_quantity[0]
overall_busd = btc_quantity[0] * init_price + initial_qty_busd  # Обща равностойност на пъвоначалните количества
overall_btc = busd_quantity[0] / init_price + initial_qty_btc
last_quantyties = {"Last BUSD": overall_busd, "Last BTC": overall_btc}
is_profit = [False]


# Проверява дали текущата цена е в обхвата на вече търгуваните цени
def check_price(curr_price):
    if not list_traded_prices:  # Ако това е първата транзакция ще се търгува по текущата цена
        return [curr_price, True]
    down_limit = list_traded_prices[0]  # Определят дали на текущата цена може да се тръгува съобразно списъка с
    # вече търгуваните цени
    up_limit = list_traded_prices[-1]
    if curr_price < down_limit:
        if curr_price <= down_limit / percentage:  # Определя да се тръгува само ако текущата цена е по-малка от послед-
            # ната търгувана цена раделена на процента за нивата на цените
            return [down_limit / percentage, True]  # Връща на каква цена ще се търгува
    elif curr_price > up_limit:
        if curr_price >= up_limit * percentage:  # Тук се умножава цената по процента
            return [up_limit * percentage, True]
    return [curr_price, False]  # Връщането на False казва, че на текущата цена НЯМА да се търгува, но в execution_order
    # трябва да се провери за печалба от чакащи количества на текущата цена


def define_factor(repo_asset):
    return 1 / (number_trades - len(repo_asset))


def print_func(exec_info):
    transaction_count[0] += 1

    print(f'Транзакция номер: {transaction_count[0]}')

    print(f'len(repo) = {len(repo_asset)}')

    print(f'Списък с цени  {list_traded_prices}')
    # print(f'Репо: {repo_asset}')
    print()
    first_qty, asset, second_qty = exec_info
    if asset == 'BUSD':
        print(f'{first_qty:.2f} {asset} -> {second_qty:.6f} BTC на цена {trading_price[0]}')
    else:
        print(f'{first_qty:.6f} {asset} -> {second_qty:.2f} BUSD на цена {trading_price[0]}')
    total_busd = busd_quantity[0] + btc_quantity[0] * curr_price
    total_btc = btc_quantity[0] + busd_quantity[0] / curr_price
    print(f'Наличност активи BUSD: {busd_quantity[0]:.2f}')
    print(f'Наличност актив BTC: {btc_quantity[0]:.6f}  ')
    print(f'Тотална равностойност BUSD: {total_busd:.2f}    Печалба: {(total_busd / overall_busd - 1) * 100:.2f}%')
    print(f'Тотална равностойност BTC: {total_btc:.6f}    Печалба: {(total_btc / overall_btc - 1) * 100:.2f}%')
    if asset == 'BUSD':
        minimal_price = sum(traded_busd_qty) / btc_quantity[0]
        print(f'Минимално ниво на цена за връщане на търгувания BUSD: {minimal_price:.2f}')
    else:
        minimal_price = busd_quantity[0] / sum(traded_btc_qty)
        print(f'Минимално ниво на цена за връщане на търгувания BTC: {minimal_price:.2f}')
    print()


# Проверка дали някое от тоталните количества е по-голямо от съответното последно количество умножено по процент
def check_for_profit(is_profit, repo_asset):
    curr_total_amount_BUSD = (btc_quantity[0] * curr_price) + busd_quantity[0]
    curr_total_amount_BTC = btc_quantity[0] + busd_quantity[0] / curr_price
    empty_repo = False
    if curr_total_amount_BUSD >= last_quantyties["Last BUSD"] * profit_percentage:
        print()
        print('ПЕЧАЛБА!!!!')
        print()
        print(f'Последен BUSD: {last_quantyties["Last BUSD"]:.2f} -> Сегашен BUSD: {curr_total_amount_BUSD:.2f}')
        print(f'Печалба: {(curr_total_amount_BUSD / last_quantyties["Last BUSD"] - 1) * 100:.2f}%')
        print(f'Печалба спрямо началното количество: {(curr_total_amount_BUSD / overall_busd - 1) * 100:.2f}%')
        print()
        last_quantyties["Last BUSD"] = curr_total_amount_BUSD
        last_quantyties['Last BTC'] = curr_total_amount_BTC
        busd_quantity[0] = curr_total_amount_BUSD
        busd_quantity[1] = True
        btc_quantity[0] = 0
        is_profit[0] = True
        repo_asset = deque()
        empty_repo = True

    if curr_total_amount_BTC >= last_quantyties['Last BTC'] * profit_percentage:
        print()
        print('ПЕЧАЛБА!!!!')
        print()
        print(f'Последен BTC: {last_quantyties["Last BTC"]:.8f} -> Сегашен BTC: {curr_total_amount_BTC:.8f}')
        print(f'Печалба: {(curr_total_amount_BTC / last_quantyties["Last BTC"] - 1) * 100:.2f}%')
        print(f'Печалба спрямо началното количество: {(curr_total_amount_BTC / overall_btc - 1) * 100:.2f}%')
        print()
        last_quantyties['Last BTC'] = curr_total_amount_BTC
        last_quantyties["Last BUSD"] = curr_total_amount_BUSD
        btc_quantity[0] = curr_total_amount_BTC
        busd_quantity[1] = False
        busd_quantity[0] = 0
        is_profit[0] = True
        repo_asset = deque()
        empty_repo = True

    if asset_on_charge == 'BUSD' and not empty_repo:
        for qty, price_level in repo_asset[0].items():
            if curr_price >= price_level:
                print()
                print(f'Частична печалба от BUSD: {qty * price_level:.2f} цена: {curr_price}')
                print()
                busd_quantity[0] += qty * price_level
                btc_quantity[0] -= qty
                repo_asset.popleft()
                list_traded_prices.popleft()
                print(
                    f'Печалба спрямо началното количество: {(curr_total_amount_BUSD / overall_busd - 1) * 100:.2f}%')



    elif asset_on_charge == 'BTC' and not empty_repo:
        for qty, price_level in repo_asset[-1].items():
            if curr_price <= price_level:
                print()
                print(f'Частична печалба от BTC: {qty / price_level:.8f} цена: {curr_price}')
                print()
                btc_quantity[0] += qty / price_level
                busd_quantity[0] -= qty
                repo_asset.pop()
                list_traded_prices.pop()
                print(
                    f'Печалба спрямо началното количество: {(curr_total_amount_BTC / overall_btc - 1) * 100:.2f}%')


# Функция за ипзълнение на поръчките в зависимост от главната валута  и вече опрелената цена за търговия
def execution_order(asset_on_charge, trading_price, is_valid_price, btc_quantity, busd_quantity):
    curr_trade_info = []
    if asset_on_charge == 'BUSD':
        if is_valid_price:
            busd_trade_qty = busd_quantity[0] * define_factor(repo_asset)  # Количество BUSD, което ще се търгува
            transaction = busd_trade_qty / trading_price  # Пресмята количеството на обмененото BUSD
            profit_level = trading_price * profit_percentage  # Пресмята нивото на цената за печалба от тази транзакция
            if len(list_traded_prices) == 0:
                list_traded_prices.append(float(f'{trading_price:.2f}'))
                traded_busd_qty.append(busd_trade_qty)
                repo_asset.append({transaction: profit_level})
                # Тук се добавя новото количество биткойн с неговата профит цена
            else:
                if trading_price > list_traded_prices[-1]:
                    list_traded_prices.append(float(f'{trading_price:.2f}'))
                    traded_busd_qty.append(busd_trade_qty)
                    repo_asset.append({transaction: profit_level})
                elif trading_price < list_traded_prices[0]:
                    list_traded_prices.appendleft(float(f'{trading_price:.2f}'))
                    traded_busd_qty.appendleft(busd_trade_qty)
                    repo_asset.appendleft({transaction: profit_level})
            btc_quantity[0] += busd_trade_qty / trading_price  # Добавяне на търгуваното количество бусд към кол.биткойн
            busd_quantity[0] -= busd_trade_qty
            curr_trade_info = [busd_trade_qty, 'BUSD',
                               transaction]  # Пренася в списък текущото търгувано количество валута
            # видът на валутата и полученото количество валута след транзакцията

        # qty = 0
        # profit_price = 0
        # for k, v in repo_asset[0].items():
        #     qty = k
        #     profit_price = v
        #
        # # Проверка дали цената за печалба на първия в редицата от чакащите печалба и достигната от текущата цена.
        # if trading_price >= profit_price:
        #     repo_asset.popleft()  # Отстраняване на първия в редицата
        #     profit = qty * profit_price
        #     busd_quantity[0] += profit  # Добавяне на печалбата към количеството BUSD
        #     del list_traded_prices[0]  # Отстраняване на първата цена от търгуваните цени в списъка на търгуваните цени
        #     del traded_busd_qty[0]
        #     btc_quantity[0] -= qty
        #     print()
        #     print('ПЕЧАЛБА!!!')
        #     print(f'{qty:.6f} BTC -> {profit:.2f} BUSD')

    else:
        if is_valid_price:
            btc_trade_qty = btc_quantity[0] * define_factor(repo_asset)
            transaction = btc_trade_qty * trading_price
            profit_level = trading_price / profit_percentage
            if len(list_traded_prices) == 0:
                list_traded_prices.append(float(f'{trading_price:.2f}'))
                traded_btc_qty.append(btc_trade_qty)
                repo_asset.append({transaction: profit_level})
            else:
                if trading_price < list_traded_prices[0]:
                    list_traded_prices.appendleft(float(f'{trading_price:.2f}'))
                    traded_btc_qty.appendleft(btc_trade_qty)
                    repo_asset.appendleft({transaction: profit_level})
                elif trading_price > list_traded_prices[-1]:
                    list_traded_prices.append(float(f'{trading_price:.2f}'))
                    traded_btc_qty.append(btc_trade_qty)
                    repo_asset.append({transaction: profit_level})
            busd_quantity[0] += btc_trade_qty * trading_price
            btc_quantity[0] -= btc_trade_qty
            curr_trade_info = [btc_trade_qty, 'BTC', transaction]

    #     qty = 0
    #     profit_price = 0
    #     for k, v in repo_asset[-1].items():
    #         qty = k
    #         profit_price = v
    #
    #     if trading_price <= profit_price:
    #         repo_asset.pop()
    #         profit = qty / profit_price
    #         btc_quantity[0] += profit
    #         del list_traded_prices[-1]
    #         del traded_btc_qty[0]
    #         busd_quantity[0] -= qty
    #         print()
    #         print('ПЕЧАЛБА!!!')
    #         print(f'{qty:.2f} BUSD -> {profit:.6f} BTC')
    #
    # if asset_on_charge == 'BUSD':
    #     # Проверка дали BUSD е свършил и трябва да започне да се търгува BTC като главна валута
    #     if busd_quantity[0] == 0:
    #         busd_quantity[1] = False
    #
    # else:
    #     if btc_quantity[0] == 0:
    #         busd_quantity[1] = True

    return curr_trade_info


def change_main_asset_msg(asset_on_charge):
    print()
    print('СМЯНА!!!')
    print('Смяна на главната валута: ', end='')
    if asset_on_charge == 'BUSD':
        print('BUSD -> BTC')
    else:
        print('BTC -> BUSD')
    print(f'Наличност BUSD: {busd_quantity[0]:.2f}')
    print(f'Наличност BTC: {btc_quantity[0]:.6f})')
    print()


print("Processing...")
while True:
    curr_price = float(client.get_symbol_ticker(symbol="BTCBUSD")["price"])
    if is_profit[0]:
        list_traded_prices = deque()
        repo_asset = deque()  # нулиране на репото и дековете с досега търгуванте количества BUSD и BTC
        traded_btc_qty = deque()
        traded_busd_qty = deque()
        is_profit[0] = False
    if busd_quantity[1] == True:  # Определя дали ще се търгува BUSD
        asset_on_charge = 'BUSD'
    else:  # Определя дали ще се търгува BTC
        asset_on_charge = 'BTC'
    if len(repo_asset) == number_trades - 1:
        # Смяна на на главната валута, последна транзакция с останалата валута, нулиране на repo-то и нулиране на
        # списъка с нивата на цените
        if asset_on_charge == 'BUSD':
            busd_quantity[1] = False
            btc_quantity[0] += busd_quantity[0] / check_price(curr_price)[0]
            busd_quantity[0] = 0
            change_main_asset_msg(asset_on_charge)
            asset_on_charge = 'BTC'
        else:
            busd_quantity[1] = True
            busd_quantity[0] += btc_quantity[0] * check_price(curr_price)[0]
            btc_quantity[0] = 0
            change_main_asset_msg(asset_on_charge)
            asset_on_charge = 'BUSD'
        repo_asset = deque()
        list_traded_prices = deque()
        traded_btc_qty = deque()
        traded_busd_qty = deque()

    trading_price = check_price(curr_price)  # Списък с цена за тръгуване и дали трябва да се търгува на нея
    exec_info = execution_order(asset_on_charge, trading_price[0], trading_price[1], btc_quantity, busd_quantity)
    if trading_price[1]:
        print_func(exec_info)
    check_for_profit(is_profit,repo_asset)
    time.sleep(1)
