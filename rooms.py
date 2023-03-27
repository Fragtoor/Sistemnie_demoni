import random


def simpleExpressionGenerator():
    str = ""
    for i in range(10):
        str += random.randint(0,25)
        str += random.choice(["+","-","*","/"])
    str += random.randint(0,25)

    return str, round(eval(str))