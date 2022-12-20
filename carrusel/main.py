from carrusel.asset import Asset
from carrusel.methods import Methods


from binance.client import Client
import time

api_key = 'TQwbBNQgAYe0Ub0PV8EGs16BU47j53Y1Cyk5pte3OcMITlNWUW9H8308AOvLC8ku'
api_secret = 'vCVxEPomFRSDhoVm0BB8osyuiICHwLUWRcJOJ212v3NcKRfQ9922BsbYIWRLBUjY'

client = Client(api_key, api_secret)
method = Methods

eur = Asset(200, 'EUR')
eth = Asset(0.128466, 'ETH', True)
busd = Asset(203.94,'BUSD', True)

objects = [eth, eur, busd]
profit_percentage = 1.0015
transactions_count = 0
print('Processing...')
while True:
    if eth.on_charge:
        for obj in objects:
            if obj.name != 'ETH' and not obj.on_charge:
                price = float(client.get_symbol_ticker(symbol = f'ETH{obj.name}')['price'])
                if method.check_for_profit(eth.real_quantity, obj.real_quantity, price, profit_percentage, 'mltp'):
                    transactions_count +=1
                    method.execution(eth, obj,'mltp', objects, transactions_count)

    if eur.on_charge:
        for obj in objects:
            if obj.name != 'EUR' and not obj.on_charge:
                if obj.name == 'ETH':
                    price = float(client.get_symbol_ticker(symbol=f'{obj.name}EUR')['price'])
                    operation = 'dvsn'
                else:
                    price = float(client.get_symbol_ticker(symbol=f'EUR{obj.name}')['price'])
                    operation = 'mltp'
                if method.check_for_profit(eur.real_quantity, obj.real_quantity, price, profit_percentage, operation):
                    transactions_count +=1
                    method.execution(eur, obj,operation, objects, transactions_count)
    if busd.on_charge:
        for obj in objects:
            if obj.name != 'BUSD' and not obj.on_charge:
                price = float(client.get_symbol_ticker(symbol = f'{obj.name}BUSD')['price'])
                if method.check_for_profit(busd.real_quantity, obj.real_quantity, price, profit_percentage, 'dvsn'):
                    transactions_count += 1
                    method.execution(busd, obj, 'dvsn', objects, transactions_count)
    time.sleep(5)


