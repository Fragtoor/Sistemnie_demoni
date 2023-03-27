from alice_sdk import *


permitted_classes = [8,9,10,11]
subject_dictionary = {
    0: "Математика",
    1: "Русский язык",
    2: "Информатика",
    3: "Физика"
}

def handler(event, context):
    req = AliceRequest(event)

    resp = AliceResponse(req)

    if req.is_new_session:
        resp.set_text("I am a parrot and i will repeat all your messages")
    else:
        resp.set_text(req.command)

    return resp.dictionary


