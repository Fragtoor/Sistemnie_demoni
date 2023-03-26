import aioalice as ae
from aioalice.dispatcher import MemoryStorage
from aioalice.utils.helper import HelperMode, Helper, Item

dp = ae.Dispatcher(storage=MemoryStorage())


permitted_classes = [8,9,10,11]
subject_dictionary = {
    0: "Математика",
    1: "Русский язык",
    2: "Информатика",
    3: "Физика"
}



class BotStates(Helper):
    mode = HelperMode.snake_case

    SELECTED_SUBJECT = Item()  # = select_game
    SELECTED_CLASS = Item()  # = guess_num
    STAGE = Item()  # 0 - Not classified; 1 - Haven't subject; 2-x - solving; x+1 - final

@dp.request_handler()
async def handle_all_requests(alice_request, state=BotStates.GUESS_NUM):
    user_id = alice_request.session.user_id
    dp.storage.set_state(user_id, 1)
    return alice_request.response('Привет! Я навык помогающий подготовиться к экзаменам. Скажи в каком ты классе.', buttons=permitted_classes)