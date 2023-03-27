import random


def simpleExpressionGenerator():
    str_ = ""
    for i in range(10):
        str_ += str(random.randint(1,25))
        str_ += random.choice(["+","-","*","/"])
    str_ += str(random.randint(1,25))

    return str_, [round(eval(str_))]

def quadraticEquationGenerator():
    a = random.randint(1, 50);
    b = random.randint(1, 50);
    c = random.randint(1, 50);
    D = b**2 - 4*a*c
    str_ = f"{a}x^2 + {b}x + {c} = 0"

    if D > 0:
        import math

        x1 = (-b + math.sqrt(D)) / (2 * a)
        x2 = (-b - math.sqrt(D)) / (2 * a)

        x1,x2 = map(round, [x1,x2])

        return str_, [x1,x2]
    elif D == 0:
        x = -b / (2 * a)

        x = round(x)

        return str_, [x]
    else:
        return str_, []

def EquationSystem():
    return " Пока не реализовано, чтобы пропустить напишите 'ответа нет'", []

def Unequation():
    return " Пока не реализовано, чтобы пропустить напишите 'ответа нет'", []