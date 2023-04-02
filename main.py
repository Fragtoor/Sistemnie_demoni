import random
import re

import rooms
from alice_sdk import *
DEBUGINFO = " "

schoolPhotoId = "1652229/bad8c0c5414c0417c80d"

YesAnswers = ["да", "конечно", "ага", "согласен", "приступим", "начнем", "продолжим", "ок"]
NoAnswers = ["нет", "откажусь", "неа"]
EndAnswers = ["Хватит", "выход", "закончить"]

GoodPhrases = ['Молодчина!💯 Продолжай в том же духе.', 'Ты настоящий Мегамозг🤓', 'Молодец!🎉 Так держать!', 'Ты щёлкаешь задачки, как орешки. Не останавливайся!']
BadPhrases = ['К сожалению, это неправильный ответ.', 'Ты ответил неправильно. Будь внимательней!', 'Твой ответ неверный. Сконцентрируйся на решении задачи.', 'Эх. Ты ответил неправильно. Не расстраивайся и сосредоточься.']

EndPhrases = ["Приятно было поработать. До встречи", "Удачи в изучении математики. Пока."]

HelpPhrases = ["Сейчас тебе надо решить задачу. Постарайся максимально вдуматься в её условие. У тебя всё получиться!😀", "Перед тобой есть задача. Вспомни всё, что ты проходил на уроках математики, соберись и реши её.", "Задача, которую тебе надо решить, под силам всем. Самое главное - это сосредоточиться, вдуматься и, собрав все свои знания, решить её. У тебя всё получиться💪"]
WhatYouCan = ["В мою основную функцию входит подготовка 9-ти классников к ОГЭ по математике на лучшие оценки💯", "Мне под силу придумывать разные задания, которые будут на ОГЭ по математике🧠. Благодаря мне 9-ти классники смогут подготовиться к экзамену на желаемую отметку💥", "Я умею давать разные задачки по математике, чтобы 9-ти классники сумели подготовиться к ОГЭ по математике на наивысшие баллы💯"]

#тут заданы варианты комнат, их описания и функции соответствующие им.
rooms_variants = {
    "Решение простых выражений": ["Тебе потребуется решить простое выражение и сказать ответ в целых числах (округляя дробный результат). Выражение: ",rooms.simpleExpressionGenerator],
    "Решение квадратных уравнений": ["Здесь тебе нужно найти корни квадратного уравнения и сказать ответ в целых числах, ответы разделяются точкой с запятой. Если ответа нет скажи 'ответа нет'. Уравнение: ", rooms.quadraticEquationGenerator],
    "Решение системы уравнений": ["Найди сумму X+Y и назови её в целых числах", rooms.EquationSystem],
    "Вероятности": ["Ответ дайте в процентах: ", rooms.Chances],
    "Прогрессии": ["", rooms.Progressions],
    "Графики": ["", rooms.Graphs]
}


def handler(event, context):
    global DEBUGINFO
    req = AliceRequest(event)

    resp = AliceResponse(req)

    if req.is_new_session:
        answers = ['Привет! Я помогу тебе потренировать свои навыки в математике. Если желаешь закончить тренировку, скажи "закончить". Приступим?']
        resp.set_text(answers[0])
        resp.set_session_state({"stage": 1})
        resp.set_buttons([{"title": "Поехали!", "hide": True}, {"title": "Выход", "hide": True}, {"title": "Что ты умеешь?", "hide": True}])

        return resp.dictionary

    if any(y in req.command.lower() for y in EndAnswers):
        resp.set_text(random.choice(EndPhrases))
        resp.end()
        return resp.dictionary

    if req.session_state["stage"] == 1:

        if (req.command.lower() == "что ты умеешь"):
            resp.set_text(random.choice(WhatYouCan))
            resp.set_session_state({"stage": 1})
            resp.set_buttons([{"title": "Поехали!", "hide": True}, {"title": "Выход", "hide": True},
                              {"title": "Помощь", "hide": True}, {"title": "Что ты умеешь?", "hide": True}])
            return resp.dictionary

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
                if re.search("лев|прав",req.command.lower()):
                    name = random.choice(list(rooms_variants.keys()))
                    values = rooms_variants[name]
                    description = values[0]
                    fun = values[1]
                    exp, result, image = fun()

                    if image is None:
                        resp.set_text(f"Прекрасно, ты оказался в комнате под названием '{name}'. {description}{exp}")
                    else:
                        resp.set_text(f"Прекрасно, ты оказался в комнате под названием '{name}'. {description}")
                        resp.bigcard(image,f"Прекрасно, ты оказался в комнате под названием '{name}'.", f"{description}{exp}" )

                    resp.set_session_state(
                        {"stage": req.session_state["stage"], "leftRight": False, "think": True, "waitedResult": result,
                         "score": req.session_state["score"]})
                    resp.set_buttons([{"title": "Ответа нет", "hide": True}, {"title": "Помощь", "hide": True}, {"title": "Выход", "hide": True}])
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
            if (req.command.lower() == "помощь"):
                resp.set_text(random.choice(HelpPhrases))
                resp.set_session_state(req.session_state)
                resp.set_buttons([{"title": "Ответа нет", "hide": True}, {"title": "Помощь", "hide": True},
                                  {"title": "Выход", "hide": True}])
                return resp.dictionary

            try:
                if (req.original_utterance.lower() != "ответа нет"):
                    exp = r"^([+-]?\d+)[\s;и,]*([+-]?\d+)?[\s;,.%мсг]*$"
                    #res = list(map(int,req.original_utterance.replace(" ", "").split("и")))
                    searched = list(re.search(exp,req.original_utterance).groups())
                    if None in searched:
                        searched.remove(None)
                    DEBUGINFO = searched
                    res = list(map(int, searched))
                else:
                    res = []
            except Exception as e:
                resp.set_session_state(req.session_state)
                resp.set_text(f"Пожалуйста ответь в целых числах. Если ответов несколько называй их через И. Если ответа нет, скажи 'ответа нет'.")
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
                    text = ' и '.join(map(str,waited))
                resp.set_text(random.choice(BadPhrases) + f" Ответ: {text}")
                resp.set_session_state({"stage": req.session_state["stage"] + 1, "leftRight": True, "think": False,
                                        "score": req.session_state["score"]})
                resp.set_buttons([{"title": "Влево", "hide": True}, {"title": "Выход", "hide": True},
                                  {"title": "Вправо", "hide": True}])

    return resp.dictionary
