# def decorator_function(original_function):
#     def wrapper_function(*args, **kwargs):
#         print(f'This is printed before {original_function.__name__} function run')
#         return original_function(*args, **kwargs)
#
#     return wrapper_function
#
#
# @decorator_function
# def display_function():
#     print('This is a display function')
#
#
# @decorator_function
# def display_info_function(name, age):
#     print(f'This is display_info_function({name}, {age})')
#
#
# display_function()
# # hi_func = decorator_function(display_function)
# # hi_func()
# display_info_function('John', 35)


def my_logger(orig_func):
    import logging
    logging.basicConfig(filename=f'{orig_func.__name__}.log',  level=logging.INFO)

    def wrapper(*args, **kwargs):
        logging.info(
            f'Ran with args: {args} and kwargs: {kwargs}'
        )
        return orig_func(*args, **kwargs)

    return wrapper

def my_timer(orig_func):
    import time

    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time() - t1
        print(f'{orig_func.__name__} ran in {t2:.10f} sec')
        return result
    return wrapper


# @my_logger
@my_timer
def display_info_function(name, age):
    import time
    time.sleep(2)
    print(f'This is display_info_function({name}, {age})')


display_info_function('John', 25)
