from math import sqrt as sq


def calculate_times_for_observer(sequence_spaceship_points_of_signals, data_dict, time_spaceship):
    y_coordinate = float(f'{data_dict["Distance_y"]:.2f}')
    sequence_observer = [0]
    time_receiving_signal = 0
    sequence_spaceship_points_of_signals = sequence_spaceship_points_of_signals[1:]
    print(f'{1 / time_spaceship:.2f}')
    print(f'Signal 1: 0 seconds')
    for i in range(len(sequence_spaceship_points_of_signals)):
        x_coordinate = sequence_spaceship_points_of_signals[i]
        time_receiving_signal += 1 / time_spaceship + sq(y_coordinate ** 2 + x_coordinate ** 2)
        sequence_observer.append(time_receiving_signal)
        diff = sequence_observer[i + 1] - sequence_observer[i]
        print(f'Signal {i + 2}: {time_receiving_signal:.2f} seconds  '
              f'Time interval between current and previous signal: {diff:.2f}')


def coordinates_spaceship_signals_points(data_dict, time_spaceship):
    x_coordinate = float(f'{data_dict["Distance_x"]:.2f}')
    velocity = float(data_dict["Velocity"])
    sequence_spaceship_points_of_signals = [-x_coordinate]
    distance_per_time_spaceship = velocity / time_spaceship
    for i in range(data_dict["Count_signals"]):
        new_point = distance_per_time_spaceship + sequence_spaceship_points_of_signals[-1]
        sequence_spaceship_points_of_signals.append(float(f'{new_point:.2f}'))
    calculate_times_for_observer(sequence_spaceship_points_of_signals, data_dict, time_spaceship)


def gamma_factor_time(data_dict):
    time_spaceship = sq(1 - (data_dict["Velocity"]) ** 2)
    coordinates_spaceship_signals_points(data_dict, time_spaceship)


def program_inputs():
    def spaceship_speed():
        spaceship_velocity = float(
            input("Enter velocity of spaceship as percentage of speed of light "))  # percentage speed of light
        if 0 > spaceship_velocity or spaceship_velocity >= 1:
            print('Invalid velocity')
            spaceship_speed()
        else:
            return spaceship_velocity

    def distance_x():
        distance_x_axis = float(input("Enter positive value for distance in light seconds among x axis:"))
        if distance_x_axis <= 0:
            print("Invalid value")
            distance_x()
        else:
            return distance_x_axis

    def distance_y():
        distance_y_axis = float(input("Enter positive value for distance in light seconds among y axis:"))
        if distance_y_axis <= 0:
            print("Invalid value")
            distance_y()
        else:
            return distance_y_axis

    count_signals = abs(int(input("Enter for how many signals to calculate (integer):")))
    data_dict = {"Velocity": spaceship_speed(), "Distance_x": distance_x(), "Distance_y": distance_y(),
                 "Count_signals": count_signals}
    gamma_factor_time(data_dict)


program_inputs()
