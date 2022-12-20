import turtle as tl

from games.arkanoid.game_classes import CircleBall, SquareBall, TriangleBall

wn = tl.Screen()
wn.title('Arcanoid')
wn.bgcolor('Green')
wn.setup(width=800, height=700)
wn.tracer(0)

player = tl.Turtle()
player.speed(0)
player.shape('square')
player.color('black')
player.shapesize(stretch_len=8, stretch_wid=1)
player.penup()
player.goto(0, -300)

cb = CircleBall()
cs = SquareBall()
eb = TriangleBall()
cb.goto(-370, 0)
cs.goto(-330, 0)
eb.goto(370, 0)
ball = tl.Turtle()
ball.speed(0)
ball.shape('circle')
ball.color('black')
# ball.shapesize(stretch_len=5, stretch_wid=1)
ball.penup()
ball.goto(0, 0)
ball.dx = 0.5
ball.dy = 0.5


def player_up():
    y = player.ycor()
    y += 30
    player.sety(y)


def player_down():
    y = player.ycor()
    y -= 30
    player.sety(y)


def player_left():
    x = player.xcor()
    x -= 30
    player.setx(x)


def player_right():
    x = player.xcor()
    x += 30
    player.setx(x)


def get_ball_position():
    return ball.xcor(), ball.ycor()


def get_player_position():
    return player.xcor(), player.ycor()


# def ball_acceleration(value):
#     if ball.dx < 0:
#         value *= -1
#     else:
#         value *= 1
#     if ball.dy < 0:
#         value *= -1
#     else:
#         value *= 1
#     ball.dx += value
#     ball.dy += value
#     return ball.dx, ball.dy


# Keybord binding
wn.listen()
wn.onkeypress(player_up, 'Up')
wn.onkeypress(player_down, 'Down')
wn.onkeypress(player_left, 'Left')
wn.onkeypress(player_right, 'Right')

# Main Game Loop


while True:
    wn.update()
    # ball.dx, ball.dy = ball_acceleration(0.01)
    # print(f'DX: {ball.dx} DY: {ball.dy}')
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)
    ball_position = get_ball_position()
    player_position = get_player_position()
    if ball_position[1] > 340:
        ball.sety(340)
        ball.dy *= -1

    if ball_position[1] < -340:
        ball.sety(-340)
        ball.dy *= -1

    if ball_position[0] > 390:
        ball.setx(390)
        ball.dx *= -1

    if ball_position[0] < -390:
        ball.setx(-390)
        ball.dx *= -1

    # ball collisions with player
    # if (ball_position[1]<= player_position[1] and
    # player_position[0] - 50 <= ball_position[0]  <= player_position[0] + 50):
    if ball_position[1] < player_position[1] and (player_position[0] - 40) < ball_position[0] < (player_position[0] + 40):
        ball.dy *= -1
    if ball_position[0] <= player_position[0]:
        ball.dx *= -1

    # print(player_position[0], player_position[1])
