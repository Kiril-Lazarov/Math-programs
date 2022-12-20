def initialize_price_levels(ground_price, asset, init_step_percentage):
    final_list = [ground_price]
    if asset == 'BTC':
        for i in range(12):
            if i < 2:
                init_step_percentage = init_step_percentage
            elif i< 5:
                init_step_percentage += 0.0003
            elif i < 8:
                init_step_percentage += 0.0005
            else:
                init_step_percentage += 0.008
            final_list.append(final_list[i] * init_step_percentage)
    else:
        for i in range(10):
            if i < 2:
                init_step_percentage = init_step_percentage
            elif i < 5:
                init_step_percentage += 0.0003
            else:
                init_step_percentage += 0.0005
            final_list.append(final_list[i] / init_step_percentage)
    return final_list

print(initialize_price_levels(30000, 'BTC', 1.005))