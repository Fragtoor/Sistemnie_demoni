import random, json


def simpleExpressionGenerator():
    str_ = ""
    for i in range(10):
        str_ += str(random.randint(1,25))
        str_ += random.choice(["+","-","*","/"])
    str_ += str(random.randint(1,25))

    return str_, [round(eval(str_))], None

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

        return str_, [x1,x2], None
    elif D == 0:
        x = -b / (2 * a)

        x = round(x)

        return str_, [x], None
    else:
        return str_, [], None

def EquationSystem():
    rooms_ = json.load(open("EquationSystems.json", "r"))

    room = random.choice(rooms_["list"])
    answers = room["answers"]
    image = room["image"]


    return "", answers, image


def SimpleEquation():
    while True:
        try:
            def solve_linear(equation, var='x'):
                expression = equation.replace("=", "-(") + ")"
                grouped = eval(expression.replace(var, '1j'))
                return int(-grouped.real / grouped.imag)
            patterns = [
                "a -(b) * x = c",
                "x * ( a -(b) ) = c",
                "a / b + x / c = 0"
                "a + b + x + c = 0",
                "( a -(b) ) * ( x + c ) = 0",
            ]

            curPattern = random.choice(patterns)
            a = random.randint(-25,25)
            curPattern = curPattern.replace('a', str(a))
            b = random.randint(-25, 25)
            curPattern = curPattern.replace('b', str(b))
            c = random.randint(-25, 25)
            curPattern = curPattern.replace('c', str(c))




            ans = solve_linear(curPattern)
        except:
            continue
        break

    return curPattern, [ans], None

def Graphs():
    rooms_ = json.load(open("Graphs.json", "r"))

    room = random.choice(rooms_["list"])
    answer = [room["answer"]]
    image = room["image"]
    title = room["text"]


    return title, answer, image

def Chances():
    tasks_ = json.load(open("chances.json", "r"))

    task = random.choice(tasks_["list"])
    answers = [task["answer"]]
    text = task["text"]

    return text, answers, None

def Progressions():
    tasks_ = json.load(open("Progressions.json", "r"))

    task = random.choice(tasks_["list"])
    answers = [task["answer"]]
    text = task["text"]

    return text, answers, None