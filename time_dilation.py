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

    return {"Velocity": spaceship_speed(), "Distance_x": distance_x(), "Distance_y": distance_y()}


def gamma_factor_time(program_inputs):
    time_spaceship = sq(1- (program_inputs["Velocity"])**2)

    return time_spaceship

print(gamma_factor_time(program_inputs()))
