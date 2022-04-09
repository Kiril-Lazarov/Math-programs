from math import sqrt as sq


def program_inputs():
    def spaceship_speed():
        spaceship_velocity = float(input("Enter velocity of spaceship (0,1)"))  # percentage speed of light
        if 0 > spaceship_velocity or spaceship_velocity >= 1:
            print('Invalid velocity')
            spaceship_speed()
        else:
            return spaceship_velocity

    def distance_x():
        distance_x_axis = float(input("Enter positive value for distance among x axis:"))
        if distance_x_axis <= 0:
            print("Invalid value")
            distance_x()
        else:
            return distance_x_axis

    def distance_y():
        distance_y_axis = float(input("Enter positive value for distance among y axis:"))
        if distance_y_axis <= 0:
            print("Invalid value")
            distance_y()
        else:
            return distance_y_axis

    count_signals = abs(int(input("Enter for how many signals to calculate (integer):")))
    data_dict = {"Velocity": spaceship_speed(), "Distance_x": distance_x(), "Distance_y": distance_y(),
                 "Count_signals": count_signals}
    gamma_factor_time(data_dict)


def gamma_factor_time(data_dict):
    time_spaceship = sq(1 - (data_dict["Velocity"]) ** 2)

    coordinates_spaceship_signals_points(str(time_spaceship), data_dict)


def coordinates_spaceship_signals_points(data_dict, time_spaceship):
    x_coordinate = float(f'{data_dict["Distance_x"]:.2f}') * -1
    y_coordinate = float(f'{data_dict["Distance_y"]:.2f}') * -1
    sequence_spaceship_points_of_signals = [x_coordinate]
    for i in range(data_dict["Count_signals"]):
        sequence_spaceship_points_of_signals[i] += sequence_spaceship_points_of_signals[i] * float(time_spaceship)
        sequence_spaceship_points_of_signals.append(sequence_spaceship_points_of_signals[i])

    print(sequence_spaceship_points_of_signals)


program_inputs()
