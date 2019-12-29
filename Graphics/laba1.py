"""
ГРАФИЧИСКИЕ ПРИМИТИВЫ(Равнобедренный треугольник Серпинского)
M1(модель базового типа): a, b = 312.5
                          c = 400
                          n = 3
                          h = 240
                          S = 37 500    # 0.5 * a * h = S

M2(орнамент): a(n) / 2, b(n) / 2
              c(n) / 2
              n = 3
              h(n) / 2
              S(n) / 4
              total triangles num 121
M3(муар)

"""
from time import sleep
from turtle import Screen, Turtle

TOTAL = 0


def drawTriangle(coords, color, turtle_obj):
    global TOTAL
    TOTAL += 1
    turtle_obj.fillcolor(color)

    turtle_obj.up()
    turtle_obj.goto(*coords[0])
    turtle_obj.down()

    turtle_obj.begin_fill()
    for i in coords[::-1]:
        turtle_obj.goto(*i)
    turtle_obj.end_fill()


def getMid(a, b, denom=2):
    return (a[0] + b[0]) / denom, (a[1] + b[1]) / denom


def sierpinski(coords, deg, turtle_obj):
    color_map = ['blue', 'red', 'green', 'white', 'yellow', 'violet', 'orange']
    drawTriangle(coords, color_map[deg], turtle_obj)
    if deg:
        sierpinski([coords[0], getMid(coords[0], coords[1]), getMid(coords[0], coords[2])], deg - 1, turtle_obj)
        sierpinski([coords[1], getMid(coords[0], coords[1]), getMid(coords[1], coords[2])], deg - 1, turtle_obj)
        sierpinski([coords[2], getMid(coords[0], coords[2]), getMid(coords[1], coords[2])], deg - 1, turtle_obj)


def shadow(coords, deg, turtle_obj):
    turtle_obj.fillcolor('black')

    turtle_obj.up()
    turtle_obj.goto(*coords[0])
    turtle_obj.down()

    for i in coords[::-1]:
        turtle_obj.width(deg * 0.2)
        turtle_obj.goto(*i)

    if deg:
        turtle_obj.width(deg * 0.3)
        shadow([[coords[0][0] + round(deg * 1.3), coords[0][1] + round(deg * 0.9)],
                [coords[1][0], coords[1][1] - round(deg * 0.6)],
                [coords[2][0] - round(deg * 1.3), coords[2][1] + round(deg * 0.9)]],
               deg - 1, turtle_obj
               )


def main():
    screen = Screen()
    mainTurtle = Turtle()
    mainTurtle.shape('turtle')
    coords = [[-200, -120], [0, 120], [200, -120]]
    deg = int(input('Enter degree: '))
    sierpinski(coords, deg, mainTurtle)
    print(TOTAL)
    if not input('Just enter to continue shadowing triangle: '):
        shadow(coords, 15, mainTurtle)
    screen.exitonclick()


if __name__ == '__main__':
    main()