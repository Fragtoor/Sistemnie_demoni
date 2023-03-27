import random

import rooms
from alice_sdk import *

YesAnswers = ["да", "конечно", "ага", "согласен", "приступим", "начнем", "продолжим", "ок"]
NoAnswers = ["нет", "откажусь", "неа"]

#тут заданы варианты комнат, их описания и функции соответствующие им.
rooms_variants = {
    "Решение простых выражений": ["Тебе потребуется решить простое выражение и сказать ответ в целых числах (округляя дробный результат). Выражение: ",rooms.simpleExpressionGenerator],
    "Решение квадратных уравнений": ["Здесь тебе нужно найти корни квадратного уравнения и сказать ответ в целых числах, ответы разделяются точкой с запятой. Если ответа нет скажи 'ответа нет'. Уравнение: ", rooms.quadraticEquationGenerator]
}


def handler(event, context):
    req = AliceRequest(event)

    resp = AliceResponse(req)

    if req.is_new_session:
        answers = ['Привет! Я помогу тебе потренировать свои навыки в математике. Приступим?']
        resp.set_text(answers[0])
        resp.set_session_state({"stage": 1})
        return resp.dictionary

    if req.session_state["stage"] == 1:
        if (x in req.command.lower() for x in YesAnswers):
            resp.set_text(
                "Ты оказываешься один в закрытой школе. Чтобы выбраться тебе нужно пройти по комнатам и выполнить несколько заданий. В пойдешь вправо или влево?")
            resp.set_session_state({"stage": 2, "leftRight": True, "think": False, "score": 0})
            return resp.dictionary
        elif (x in req.command.lower() for x in NoAnswers):
            resp.set_text("Ну ладно")
            resp.end()
            return resp.dictionary
        else:
            resp.set_text("Ну так приcтупим?")
            resp.set_session_state({"stage": 1})
            return resp.dictionary

    if req.session_state["stage"] >= 12:
        if req.session_state["score"] >= 5:
            resp.set_text(
                f"Поздравляю, ты наконец выбрался из закрытой школы. Твой результат: {req.session_state['score']} из 10 правильно решёных заданий")
            resp.end()
        else:
            resp.set_text(
                f"К сожалению ты остаешься в школе. Ты будешь решать задания до тех пор пока не решишь верно.")
            resp.set_session_state({"stage": 1, "leftRight": False, "think": False, "score": 0})
        return resp.dictionary

    if req.session_state["stage"] > 1:
        if (req.session_state["leftRight"]):
            try:
                if req.command.lower() in ("вправо", "влево"):
                    name = random.choice(list(rooms_variants.keys()))
                    values = rooms_variants[name]
                    description = values[0]
                    fun = values[1]
                    exp, result = fun()

                    resp.set_text(f"Прекрасно, ты оказался в комнате под названием '{name}'. {description}{exp}")
                    resp.set_session_state(
                        {"stage": req.session_state["stage"], "leftRight": False, "think": True, "waitedResult": result,
                         "score": req.session_state["score"]})
                else:
                    resp.set_session_state(req.session_state)
                    resp.set_text(f"Пожалуйста ответь вправо или влево")

            except Exception as e:
                resp.set_text(f"Произошла ошибка: {e}")
                resp.end()
                return resp.dictionary

        if (req.session_state["think"]):

            try:
                if (req.original_utterance.lower() != "ответа нет"):
                    res = list(map(int,req.original_utterance.replace(" ", "").split(";")))
                else:
                    res = []
            except:
                resp.set_session_state(req.session_state)
                resp.set_text(f"Пожалуйста ответь в целых числах. Если ответов несколько они разделяются знаком ;. Если ответа нет скажи 'ответа нет'")
                return resp.dictionary
            if (req.session_state["waitedResult"].sort() == res.sort()):
                resp.set_text(f"Молодец, ответь влево или вправо пойдешь дальше.")
                resp.set_session_state({"stage": req.session_state["stage"] + 1, "leftRight": True, "think": False,
                                        "score": req.session_state["score"] + 1})
            else:
                resp.set_text(
                    f"Правильным ответом было {';'.join(req.session_state['waitedResult'])}. Скажи вправо или влево пойдешь дальше.")
                resp.set_session_state({"stage": req.session_state["stage"] + 1, "leftRight": True, "think": False,
                                        "score": req.session_state["score"]})

    return resp.dictionary
