dolars = 100   #Това е права схема на търговия, т.е. обмяна на валута по печелившия курс|
BTC = 0.002041   #ако биткойна расте, се обменя биткойн; ако биткойна пада се обменя долар
price = 49000
start_d = 200
start_b = 0.004082
quotient_amount = 2/5
price_up = price * 1.03
price_down = price / 1.03
count = 0
while True:
    action = input()
    count += 1
    if action == '*':
        dolars += quotient_amount * BTC * price_up
        BTC*= (1 - quotient_amount)
        total_dollars = dolars + BTC * price_up
        total_BTC = BTC + dolars / price_up
        price = price_up
        print(f'{dolars:.2f}, {BTC:.6f}, долари: {total_dollars:.2f}/{total_dollars/start_d *100 - 100:.2f}%, '
              f'биткойн: {total_BTC:.6f}/{total_BTC/start_b*100 - 100:.2f}%, цена: {price}, брой:{count}')

    elif action == '/':
        BTC += quotient_amount * dolars / price_down
        dolars *= (1 - quotient_amount)
        total_dollars = dolars + BTC * price_down
        total_BTC = BTC + dolars / price_down
        price = price_down
        print(f'{dolars:.2f}, {BTC:.6f}, долари: {total_dollars:.2f}/{total_dollars / start_d *100 - 100:.2f}%, '
              f'биткойн: {total_BTC:.6f}/{total_BTC / start_b * 100 - 100:.2f}%, цена: {price}, брой:{count}')
    price_up = price * 1.03
    price_down = price / 1.03


# *
# /
# *
# /
# *
# /
# *
# /
# *
# /
# *
# /
# *
# /
# *
# /
# *
# /
# *
# /
# *
# /
# *
# /