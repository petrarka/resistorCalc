from aiohttp import web
from aioalice import Dispatcher, get_new_configured_app, types
from aioalice.dispatcher import MemoryStorage


WEBHOOK_URL_PATH = ''  # webhook endpoint
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 8081
dp = Dispatcher(storage=MemoryStorage())
COLORS = {'чёрный':0, 'коричневый':1, 'красный':2,'оранжевый':3, 'желтый':4, 'зеленый':5, 'синий':6, 'фиолетовый':7, 'серый':8, 'белый':9}
ROWW = ['второй', 'третьей', 'четвёртой', 'пятой']
class User():
    state = "select_type"
    rings = []
USERS={}

def calc(rows, t):
    return 'pass'

@dp.request_handler(func=lambda areq: areq.session.new)
async def handle_new_session(alice_request):
    user_id = alice_request.session.user_id
    USERS[user_id] = User()
    return alice_request.response('Привет! Этот навык позволяет вычислить наминал  резистора по цветовой маркеровке. Для выхода из навыка скажите алиса хватит, для помощи скажите справка. Сколько полос на резисторе? Четыре или пять?')

@dp.request_handler(func=lambda areq: USERS[areq.session.user_id].state=="select_type")
async def handle_select_state(alice_request):
    user_id = alice_request.session.user_id
    if int(alice_request.request.command) == 4:
        USERS[user_id].state = "4rows"
        return alice_request.response('выбран четырехполосной код, назовите цвет первой полосы')
    elif int(alice_request.request.command) == 5:
        USERS[user_id].state = "5rows"
        return alice_request.response('выбран пятиполосный код, назовите цвет первой полосы')
    else:
        return alice_request.response('Тип не распознан, повторите пожалуйста, на резисторе 4 или 5 полос?')

@dp.request_handler(func=lambda areq: USERS[areq.session.user_id].state=="4rows")
async def handle_4rows(alice_request):
    user_id = alice_request.session.user_id

    if  alice_request.request.command in COLORS:
        USERS[user_id].rows.append(COLORS[alice_request.request.command])
        if len(USERS[user_id].rows) == 4:
            return alice_request.response(calc(USERS[user_id].rows, 4)) 
        return alice_request.response('Назовите цвет {} полосы'.format(ROWW[len(USERS[user_id].rows)-2]))
    else:
        return alice_request.response('Цвет не распознан, повторите.')

@dp.request_handler(func=lambda areq: USERS[areq.session.user_id].state=="5rows")
async def handle_5rows(alice_request):
    user_id = alice_request.session.user_id

    if  alice_request.request.command in COLORS:
        USERS[user_id].rows.append(COLORS[alice_request.request.command])
        if len(USERS[user_id].rows) == 5:
            return alice_request.response(calc(USERS[user_id].rows, 5)) 
        return alice_request.response('Назовите цвет {} полосы'.format(ROWW[len(USERS[user_id].rows)-2]))
    else:
        return alice_request.response('Цвет не распознан, повторите.')
        

@dp.request_handler()
async def handle_all_other_requests(alice_request):
    # Всеми силами убеждаем пользователя     купить слона,
    # предлагаем варианты ответа на основе текста запроса
    print(alice_request.session.user_id)
    return alice_request.response('цвет или количество колец названы неверно. скажите справка для списка команд')


if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)