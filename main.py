from aiohttp import web
from aioalice import Dispatcher, get_new_configured_app, types
from aioalice.dispatcher import MemoryStorage


WEBHOOK_URL_PATH = ''  # webhook endpoint
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 8081
dp = Dispatcher(storage=MemoryStorage())

@dp.request_handler(func=lambda areq: areq.session.new)
async def handle_new_session(alice_request):
    return alice_request.response('Привет! Этот навык позволяет вычислить наминал  резистора по цветовой маркеровке. Для выхода из навыка скажите клиса хватиттр. Сколько полос на резисторе? Четыре или пять?')


async def handle_all_other_requests(alice_request):
    # Всеми силами убеждаем пользователя купить слона,
    # предлагаем варианты ответа на основе текста запроса
    requst_text = alice_request.request.original_utterance
    suggests = await get_suggests(alice_request.session.user_id)
    return alice_request.response('Все говорят "цвет или количество колец названы неверно. скажите справка для списка команд')


if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)