import random, json


def simpleExpressionGenerator():
    str_ = ""
    for i in range(10):
        str_ += str(random.randint(1,25))
        str_ += random.choice(["+","-","*","/"])
    str_ += str(random.randint(1,25))

    return str_.replace("*", "∙"), [round(eval(str_))], None

def quadraticEquationGenerator():
    """Генератор полных квадратных уравнений"""
    a = random.choice(list(range(-20, 0)) + list(range(1, 21)))
    b = random.choice(list(range(-20, 0)) + list(range(1, 21)))
    c = random.choice(list(range(-20, 0)) + list(range(1, 21)))

    D = b ** 2 - 4 * a * c
    a_str = ''
    b_str = f'{"-" if b < 0 else "+"}'
    c_str = f'{"-" if c < 0 else "+"}'
    if a == 1:
        a_str = ''
        a = ''
    if a == -1:
        a_str = '-'
        a = ''
    if b == 1:
        b_str = '+'
        b = ''
    if b == -1:
        b_str = '-'
        b = ''
    b = abs(b) if b != '' else b
    str_ = f'{a_str}{a}x²{b_str}{b}x{c_str}{abs(c)}'

    if D > 0:
        import math
        if b == '' and b_str == '+':
            b = 1
        if a_str == '-' and a == '':
            a = -1
        if b_str == '-' and b == '':
            b = -1
        if a_str == '' and a == '':
            a = 1

        x1 = (-b + math.sqrt(D)) / (2 * a)
        x2 = (-b - math.sqrt(D)) / (2 * a)

        # Округление по математическим правилам
        x1 = int(x1 + (0.5 if x1 > 0 else -0.5))
        x2 = int(x2 + (0.5 if x2 > 0 else -0.5))

        if x2 == x1:
            return quadraticEquationGenerator()
        else:
            return str_, [min(x1, x2), max(x1, x2)], None
    elif D == 0:
        x = -b / (2 * a)

        x = round(x)

        return str_, [x], None
    else:
        # Не может быть D < 0(В ОГЭ такого не бывает)
        return quadraticEquationGenerator()


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

    return curPattern.replace("*", "∙"), [ans], None

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

def GeometricalExpressions():
    tasks_ = json.load(open("geometricalExpressions.json", "r"))

    task = random.choice(tasks_["list"])
    answers = task["answers"]
    text = task["text"]

    return text, answers, None
