from math import sqrt as sq

'''
    Description:
    
    This program tests the hypothesis whether the time flow of a moving body goes faster for the observer when 
the body approaches it and goes slower when it moves away.  According to the Special theory of relativity, 
time moves slower in the moving system. This hypothesis agrees with this, but says that there must be a difference 
in how the passage of time in the moving system looks to the stationary observer. The thought experiment consists in 
the following - the observer is situated at the origin of the coordinate system (0.0) and the moving body (spacecraft) 
at a distant point with coordinates x and y (inputs). The ship is moving at some speed close to the speed of light.
Every second, measured by his own time, he emits a signal from the point at which he is at that moment. The observer 
receives the signals and measures the time intervals between them. Calculations show that the intervals are shorter 
when the ship approaches the observer and longer when it moves away from it.
'''


def pythagoras(x, y):
    return sq(x ** 2 + y ** 2)


def print_func(message):
    print(message)


def calculate_times_for_observer(sequence_spaceship_points_of_signals, data_dict, time_spaceship):
    y_coordinate = float(f'{data_dict["Distance_y"]:.2f}')
    sequence_observer = []
    path_diff = 0
    message = f"Spaceship's time run {1 / time_spaceship:.2f} times slower than observer's time."
    print_func(message)
    for i in range(len(sequence_spaceship_points_of_signals)):
        x_coordinate = sequence_spaceship_points_of_signals[i]
        # calculates the distance that new signal need to travel after receiving of the previous signal
        if i > 0:
            path_diff = abs(pythagoras(sequence_spaceship_points_of_signals[i], y_coordinate) -
                            (pythagoras(sequence_spaceship_points_of_signals[i - 1],
                                        y_coordinate) - 1 / time_spaceship))

            sequence_observer.append(float(f'{sequence_observer[i - 1] + path_diff:.2f}'))
        else:
            sequence_observer.append(float(f'{pythagoras(x_coordinate, y_coordinate):.2f}'))

        message = f'Signal {i + 1}: {sequence_observer[i]:.2f} seconds ' \
                  f' x coordinate of current signal {sequence_spaceship_points_of_signals[i]}   Time interval between current' \
                  f' and previous signal: {path_diff:.12f}'
        print_func(message)


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
