import random

import rooms
from alice_sdk import *


permitted_classes = [8,9,10,11]
subject_dictionary = {
    0: "Математика",
    1: "Русский язык",
    2: "Информатика",
    3: "Физика"
}

YesAnswers = ["да", "конечно", "ага","согласен","приступим","начнем","продолжим","ок"]
NoAnswers = ["нет", "откажусь", "неа"]

rooms_variants = {"Решение простых выражений": ["Тебе потребуется решить простое выражение и сказать ответ в целых числах (округляя дробный результат). Выражение: ", rooms.simpleExpressionGenerator]}



def handler(event, context):
    req = AliceRequest(event)

    resp = AliceResponse(req)

    if req.is_new_session:
        answers = ['Привет! Я помогу тебе подготовиться к ОГЭ по математике. Приступим?']
        resp.set_text(answers[0])
        resp.set_session_state({"stage": 1})
        return resp.dictionary

    if req.session_state["stage"] == 1:
        if (x in req.command.lower() for x in YesAnswers):
            resp.set_text("Ты оказываешься один в закрытой школе. Чтобы выбраться тебе нужно пройти по комнатам и выполнить несколько заданий. В пойдешь вправо или влево?")
            resp.set_session_state({"stage": 2, "leftRight": True, "think": False})
            return resp.dictionary
        elif (x in req.command.lower() for x in NoAnswers):
            resp.set_text("Ну ладно")
            resp.end()
            return resp.dictionary
        else:
            resp.set_text("Ну так приcтупим?")
            resp.set_session_state({"stage": 1})
            return resp.dictionary

    if req.session_state["stage"] > 1:
        if (req.session_state["leftRight"]):
            if req.command.lower() in ("вправо","влево"):

                name = random.choice(rooms_variants.keys())
                values = rooms_variants[name]
                description = values[0]
                fun = values[1]
                exp, result = fun()


                resp.set_text(f"Прекрасно, ты оказался в комнате под названием '{name}'. {description}{exp}")
                resp.set_session_state({"stage": req.session_state["stage"], "leftRight": False, "think": True, "waitedResult": result})

        if (req.session_state["think"]):

            try:
                res = int(req.command)
            except:
                resp.set_text(f"Пожалуйста ответь одним целым числом.")
                return resp.dictionary
            if (req.session_state["waitedResult"] == res):
                resp.set_text(f"Молодец, ответь влево или вправо пойдешь дальше.")
                resp.set_session_state({"stage": req.session_state["stage"] + 1, "leftRight": True, "think": False})
            else:
                resp.set_text(f"Правильным ответом было {req.session_state['waitedResult']}. Скажи вправо или влево пойдешь дальше.")
                resp.set_session_state({"stage": req.session_state["stage"] + 1, "leftRight": True, "think": False})



    return resp.dictionary




