import random

import rooms
from alice_sdk import *

schoolPhotoId = "1652229/bad8c0c5414c0417c80d"

YesAnswers = ["да", "конечно", "ага", "согласен", "приступим", "начнем", "продолжим", "ок"]
NoAnswers = ["нет", "откажусь", "неа"]
EndAnswers = ["Хватит", "выход", "закончить"]

GoodPhrases = ['Молодчина!💯 Продолжай в том же духе.', 'Ты настоящий Мегамозг🤓', 'Молодец!🎉 Так держать!', 'Ты щёлкаешь задачки, как орешки. Не останавливайся!']
BadPhrases = ['К сожалению, это неправильный ответ.', 'Ты ответил неправильно. Будь внимательней!', 'Твой ответ неверный. Сконцентрируйся на решении задачи.', 'Эх. Ты ответил неправильно. Не расстраивайся и сосредоточься.']

EndPhrases = ["Приятно было поработать. До встречи", "Удачи в изучении математики. Пока."]

#тут заданы варианты комнат, их описания и функции соответствующие им.
rooms_variants = {
    "Решение простых выражений": ["Тебе потребуется решить простое выражение и сказать ответ в целых числах (округляя дробный результат). Выражение: ",rooms.simpleExpressionGenerator],
    "Решение квадратных уравнений": ["Здесь тебе нужно найти корни квадратного уравнения и сказать ответ в целых числах, ответы разделяются точкой с запятой. Если ответа нет скажи 'ответа нет'. Уравнение: ", rooms.quadraticEquationGenerator],
    "Поиск решение к неравенству": ["Решение какого из данных неравенств изображено на рисунке", rooms.Unequation],
    "Решение системы уравнений": ["Найдите X и Y системы уравнений", rooms.EquationSystem],
    "Решение линейных уравнений": ["Найдите корни уравнения", rooms.EquationSystem]
}


def handler(event, context):
    req = AliceRequest(event)

    resp = AliceResponse(req)

    if req.is_new_session:
        answers = ['Привет! Я помогу тебе потренировать свои навыки в математике. Если желаешь закончить тренировку, скажи "закончить". Приступим?']
        resp.set_text(answers[0])
        resp.set_session_state({"stage": 1})
        resp.set_buttons([{"title": "Поехали!", "hide": True}, {"title": "Выход", "hide": True}])

        return resp.dictionary

    if any(y in req.command.lower() for y in EndAnswers):
        resp.set_text(random.choice(EndPhrases))
        resp.end()
        return resp.dictionary

    if req.session_state["stage"] == 1:
        if (x in req.command.lower() for x in YesAnswers):
            resp.set_text(
                "Ты оказываешься один в закрытой школе. Чтобы выбраться, тебе нужно пройти по комнатам и выполнить несколько заданий. В пойдешь вправо или влево?")

            resp.bigcard(schoolPhotoId, "Ты оказываешься один в закрытой школе. ", "Чтобы выбраться, тебе нужно пройти по комнатам и выполнить несколько заданий. После каждого ответа тебе предстоит выбирать: идти либо влево, либо вправо. Пойдешь вправо или влево? \nФото взято с сайта: https://klike.net/1903-shkola-krasivye-kartinki-40-foto.html")

            resp.set_session_state({"stage": 2, "leftRight": True, "think": False, "score": 0})
            resp.set_buttons([{"title": "Влево", "hide": True}, {"title": "Выход", "hide": True},
                              {"title": "Вправо", "hide": True}])
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
            resp.set_buttons([{"title": "Продолжим", "hide": True}, {"title": "Выход", "hide": True}])
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
                    resp.set_buttons([{"title": "Ответа нет", "hide": True}, {"title": "Выход", "hide": True}])
                else:
                    resp.set_session_state(req.session_state)
                    resp.set_text(f"Пожалуйста ответь вправо или влево")
                    resp.set_buttons([{"title": "Влево", "hide": True}, {"title": "Выход", "hide": True},
                                     {"title": "Вправо", "hide": True}])

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
                resp.set_text(f"Пожалуйста ответь в целых числах. Если ответов несколько они разделяются знаком ;. Если ответа нет, скажи 'ответа нет'")
                resp.set_buttons([{"title": "Ответа нет", "hide": True}, {"title": "Выход", "hide": True}])
                return resp.dictionary
            if (sorted(req.session_state["waitedResult"]) == sorted(res)):
                resp.set_text(random.choice(GoodPhrases))
                resp.set_session_state({"stage": req.session_state["stage"] + 1, "leftRight": True, "think": False,
                                        "score": req.session_state["score"] + 1})
                resp.set_buttons([{"title": "Влево", "hide": True}, {"title": "Выход", "hide": True},
                                  {"title": "Вправо", "hide": True}])

            else:
                waited = req.session_state['waitedResult']
                if len(waited) == 0:
                    text = "Ответа нет"
                elif len(waited) == 1:
                    text = str(waited[0])
                else:
                    text = ';'.join(map(str,waited))
                resp.set_text(random.choice(BadPhrases) + f" Ответ: {text}")
                resp.set_session_state({"stage": req.session_state["stage"] + 1, "leftRight": True, "think": False,
                                        "score": req.session_state["score"]})
                resp.set_buttons([{"title": "Влево", "hide": True}, {"title": "Выход", "hide": True},
                                  {"title": "Вправо", "hide": True}])

    return resp.dictionary
