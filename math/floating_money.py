init_busd = 999
active_money = ''
repo_btc = 0
deletion_factor = 0.1
while True:
    curr_price = float(input("Въведи цена: "))
    if active_money == 'BUSD':
        curr_qty_order = init_busd * deletion_factor # Константно количество, с което ще се търгува
        number_trades = 0 # Брояч за транзакциите
        compare_btc_start_qty = init_busd * curr_qty_order # Равностойност в BTC на начланият BUSD
        while number_trades <= 10:
            init_busd -= init_busd
            repo_btc += curr_qty_order / curr_price
            number_trades +=1
        if repo_btc > compare_btc_start_qty:
            active_money = "BTC"
        elif repo_btc * curr_price > curr_qty_order * 10:
            init_busd = repo_btc * curr_price
    else:
        pass
