import random


def simpleExpressionGenerator():
    str_ = ""
    for i in range(10):
        str_ += str(random.randint(1,25))
        str_ += random.choice(["+","-","*","/"])
    str_ += str(random.randint(1,25))

    return str_, round(eval(str_))