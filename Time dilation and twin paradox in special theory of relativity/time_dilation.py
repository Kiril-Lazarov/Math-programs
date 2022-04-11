from math import sqrt as sq


def pythagoras(x, y):
    return sq(x ** 2 + y ** 2)


def calculate_times_for_observer(sequence_spaceship_points_of_signals, data_dict, time_spaceship):
    y_coordinate = float(f'{data_dict["Distance_y"]:.2f}')
    velocity = data_dict["Velocity"]
    sequence_observer = [0]
    time_receiving_signal = 0
    print(f"Spaceship's time run {1 / time_spaceship:.2f} times slower than observer's time.")
    start_point_x_axis = sequence_spaceship_points_of_signals[0]
    print(f'Signal 1: 0 seconds  x coordinate of current signal {sequence_spaceship_points_of_signals[0]:.2f}')
    sequence_spaceship_points_of_signals = sequence_spaceship_points_of_signals[1:]
    for i in range(len(sequence_spaceship_points_of_signals)):
        x_coordinate = sequence_spaceship_points_of_signals[i]
        curr_dist_travel_along_x_axis = abs(start_point_x_axis - x_coordinate)
        time_receiving_signal = 1 / time_spaceship * (i + 1) + sq(y_coordinate ** 2 + x_coordinate ** 2) \
                                - abs(sequence_spaceship_points_of_signals[i])
        print(sq(y_coordinate ** 2 + x_coordinate ** 2))
        sequence_observer.append(time_receiving_signal)
        diff = sequence_observer[i + 1] - sequence_observer[i]
        print(f'Signal {i + 2}: {time_receiving_signal:.2f} seconds  '
              f' x coordinate of current signal {sequence_spaceship_points_of_signals[i]}  Time interval between current'
              f' and previous signal: {diff:.12f}')


def coordinates_spaceship_signals_points(data_dict, time_spaceship):
    x_coordinate = float(f'{data_dict["Distance_x"]:.2f}')
    velocity = float(data_dict["Velocity"])
    sequence_spaceship_points_of_signals = [-x_coordinate]
    position_change_spaceship_by_observer_time = 1 / time_spaceship * velocity
    for i in range(data_dict["Count_signals"]):
        new_point = position_change_spaceship_by_observer_time + sequence_spaceship_points_of_signals[-1]
        sequence_spaceship_points_of_signals.append(float(f'{new_point:.2f}'))
    calculate_times_for_observer(sequence_spaceship_points_of_signals, data_dict, time_spaceship)


def gamma_factor_time(data_dict):
    time_spaceship = sq(1 - (data_dict["Velocity"]) ** 2)
    coordinates_spaceship_signals_points(data_dict, time_spaceship)


def program_inputs():
    def spaceship_speed():
        while True:
            spaceship_velocity = float(
                input(
                    "Enter velocity of spaceship as percentage of speed of light ")) / 100  # percentage speed of light
            if 0 < spaceship_velocity < 1:
                break
            else:
                print("Invalid value")
        return spaceship_velocity

    def distance_x():
        while True:
            distance_x_axis = float(input("Enter positive value for distance in light seconds along x axis:"))
            if distance_x_axis > 0:
                break
            else:
                print("Invalid value")
        return distance_x_axis

    def distance_y():
        while True:
            distance_y_axis = float(input("Enter positive value for distance in light seconds along y axis:"))
            if distance_y_axis > 0:
                break
            else:
                print("Invalid value")
        return distance_y_axis

    count_signals = abs(int(input("Enter for how many signals to calculate (integer):")))
    data_dict = {"Velocity": spaceship_speed(), "Distance_x": distance_x(), "Distance_y": distance_y(),
                 "Count_signals": count_signals}
    gamma_factor_time(data_dict)


program_inputs()
