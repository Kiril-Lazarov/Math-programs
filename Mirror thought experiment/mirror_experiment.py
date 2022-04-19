from math import sqrt as sq, sin, acos, dist


def pythagoras(x, y):
    return sq(x ** 2 + y ** 2)


def program_inputs():
    def spaceship_speed():
        while True:
            spaceship_velocity = float(
                input(
                    "Enter velocity of spaceship as percentage of speed of light ")) / 100
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
                 "Count_signals": count_signals, "Distance_between_mirrors": 1}
    return data_dict


def coordinates_spaceship_signals_points(inputs_dict):
    x_coordinate_a = float(f'-{inputs_dict["Distance_x"]:.2f}')
    y_coordinate_a = float(f'{inputs_dict["Distance_y"]:.2f}')
    y_coordinate_b = y_coordinate_a + inputs_dict["Distance_between_mirrors"]
    velocity = float(inputs_dict["Velocity"])
    path_length_x = velocity / sin(acos(velocity))  # The path spaceship traveled along x_axis with given speed
    sequence_spaceship_points_of_signals_a = {
        1: (x_coordinate_a, y_coordinate_a)}  # Stores x and y coordinates of photon where it reaches mirror "A"
    sequence_spaceship_points_of_signals_b = {}  # Stores x and y coordinates of photon where it reaches mirror "B"
    for i in range(inputs_dict["Count_signals"]):  # Fills the two dictionaries with data (x,y)
        x_coordinate_b = float(
            f'{sequence_spaceship_points_of_signals_a[i + 1][0] + path_length_x:.2f}')
        sequence_spaceship_points_of_signals_b[i + 1] = (x_coordinate_b, y_coordinate_b)
        x_coordinate_a = float(f'{sequence_spaceship_points_of_signals_b[i + 1][0] + path_length_x:.2f}')
        sequence_spaceship_points_of_signals_a[i + 2] = (x_coordinate_a, y_coordinate_a)
    dictionaries_list = [sequence_spaceship_points_of_signals_a, sequence_spaceship_points_of_signals_b]
    return dictionaries_list


def time_sequence_observer():
    dict_list = coordinates_spaceship_signals_points(program_inputs())
    mirror_a_points = dict_list[0]
    del mirror_a_points[len(mirror_a_points)]  # Delete the last member of mirror_a dictionary
    mirror_b_points = dict_list[1]
    time_factor = dist(mirror_a_points[1], mirror_b_points[1])
    for i in range(len(mirror_a_points)):
        signal_from_a = dist(mirror_a_points[i + 1], (0, 0)) + 2 * i * time_factor
        signal_from_b = dist(mirror_b_points[i + 1], (0, 0)) + (2 * i + 1) * time_factor

        print(f'Signal {2 * i + 1}: {float(signal_from_a):.2f}                   Mirror A point: {mirror_a_points[i+1][0]}')
        print(
            f'Signal {2 * i + 2}: {float(signal_from_b):.2f}  Difference: {abs(float(signal_from_a - signal_from_b)):.2f} '
            f'Mirror B point: {mirror_b_points[i+1][0]} ')


time_sequence_observer()
