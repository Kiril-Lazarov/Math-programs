# # class Person:
# #     def __init__(self, name, age):
# #         self.name = name
# #         self.age = age
# #         self.friends = []
# #
# # at = Person('a', 34)
# #
# #
# # '<__main__.Person object at 0x01AB3CA0>'
# #
# # with open('data.txt', 'w') as file:
# #     file.write(f'{id(at)}')
# # #
# # with open('data.txt') as file:
# #     r = eval(file.readline())
# #
# # print(r.name)
#
# # btc_qty = 0.1
# # btc_init_qty = btc_qty
# # trade_btc_qty = btc_qty/8
# # price = 20000
# # usdt_init_qty = btc_qty*price
# # usdt_qty = 0
# # while btc_qty>0:
# #     price/= 1.001
# #     usdt_qty += trade_btc_qty * price
# #     btc_qty -= trade_btc_qty
# #     total_btc = usdt_qty / price + btc_qty
# #     total_usdt = usdt_qty + btc_qty*price
# #     print('-------------------------------------')
# #     print(f'Price: {price:.2f}')
# #     print(f'Total BTC: {total_btc:.5f}\nTotal USDT: {total_usdt:.2f}')
# #     btc_profit = float(f'{(total_btc/btc_init_qty - 1)*100:.2f}')
# #     print(f'Печалба BTC: {(total_btc/btc_init_qty - 1)*100:.2f}%')
# #     print(f'Печалба USDT: {(total_usdt/usdt_init_qty - 1)*100:.2f}%')
# #     if btc_profit>= 0.08:
# #         print(f'НАПОМПВАНЕ')
# #         usdt_qty += 2*trade_btc_qty * price
# #         btc_qty -= 2 * trade_btc_qty
# #         print(f'Печалба BTC: {(total_btc / btc_init_qty - 1) * 100:.2f}%')
# #         print(f'Печалба USDT: {(total_usdt / usdt_init_qty - 1) * 100:.2f}%')
import pickle

class example_class:
    a_number = 35
    a_string = "hey"
    a_list = [1, 2, 3]
    a_dict = {"first": "a", "second": 2, "third": [1, 2, 3]}
    a_tuple = (22, 23)
class Numbers:
    def __init__(self, name, value):
        self.name = name
        self.value = value

a1 = Numbers('a1', 7)
a2 = Numbers('a2', 9)


my_object = example_class()
my_object.a_list = [a1, a2]
print(f'my_object: {my_object}')
my_pickled_object = pickle.dumps(my_object)  # Pickling the object
print(f"This is my pickled object:\n{my_pickled_object}\n")

my_object.a_dict = None

my_unpickled_object = pickle.loads(my_pickled_object)  # Unpickling the object
print(
    f"This is a_dict of the unpickled object:\n{my_unpickled_object.a_dict}\n")


