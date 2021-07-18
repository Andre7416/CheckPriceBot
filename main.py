import json
import asyncio
import copy
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import Database
from csparser import Parse
import buttons


API_TOKEN = 'put_your_token_here'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database()


class Form(StatesGroup):
    url = State()
    delete_url = State()


def startup(file='your_data_file'):
    with open(file, 'r') as f:
        dt = json.load(f)
    return dt


async def save_data(dt, file='your_data_file'):
    while True:
        await asyncio.sleep(14400)
        data_check = copy.deepcopy(dt)
        with open(file, 'w') as f:
            json.dump(data_check, f)


data = startup()


async def check_prices(time=3600):
    while True:
        await asyncio.sleep(time)
        for user_id in db.get_subs():
            user_id = user_id[1]
            data_check = copy.deepcopy(data)
            for link, price in data_check.get(user_id, {}).items():
                await asyncio.sleep(2)
                parse = Parse(link)
                new_price = parse.get_price()
                word = 'увеличилась' if new_price > price else 'уменьшилась'
                delta = abs(price - new_price)
                if price != new_price and new_price != 1e12:
                    data[user_id][link] = new_price
                    await bot.send_message(user_id, f'Цена на товар "{parse.get_info()}" {word} на {delta} '
                                                    f'и составляет {new_price}\n{link}')
                await asyncio.sleep(1)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет!', reply_markup=buttons.main_menu)


@dp.message_handler(commands=['help'])
async def info(message: types.Message):
    await message.answer('''
С помощью этого бота ты сможешь следить за ценой интересующих тебя вещей!
👉Используй "/subscribe", чтобы подписаться на рассылку.
👉Добавлять товары можно с помощью команды "/add".
👉Для просмотра списка всех своих товаров можно использовать "/list".
👉Команды "/clear" и "/remove" помогут убирать ненужные товары.
👉Напиши "/unsubscribe", если больше не хочешь получать сообщения.''')


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.is_in_database(message.from_user.id):
        db.add_sub(message.from_user.id)
        await message.answer('Подписка оформлена')
    else:
        db.update_sub(message.from_user.id, True)
        await message.answer('Подписка возобновлена')


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.is_in_database(message.from_user.id):
        db.add_sub(message.from_user.id, status=False)
        await message.answer('Возможно, сначала стоит подписаться')
    else:
        db.update_sub(message.from_user.id, False)
        await message.answer('Подписка отменена')


@dp.message_handler(commands=['add'])
async def add(message: types.Message):
    await Form.url.set()
    await message.answer('Жду ссылку на интересующий товар с сайта https://www.farfetch.com/ru или '
                         'https://www.yoox.com/ru',
                         disable_web_page_preview=True)


@dp.message_handler(state=Form.url)
async def set_new_url(message: types.Message, state: FSMContext):
    user = str(message.from_user.id)
    url = message.text
    data[user] = data.get(user, dict())
    await asyncio.sleep(2)
    data[user][url] = Parse(url).get_price()
    await state.finish()
    await message.answer(f'Товар успешно добавлен, его текущая цена {data[user][url]}')


@dp.message_handler(commands=['clear'])
async def clear(message: types.Message):
    user_id = str(message.from_user.id)
    data.pop(user_id, 1)
    await message.answer('Готово. Очистка завершена!')


@dp.message_handler(commands=['remove'])
async def delete_one(message: types.Message):
    await Form.delete_url.set()
    await message.answer('Жду ссылку на товар, который нужно убрать')


@dp.message_handler(state=Form.delete_url)
async def delete_url(message: types.Message, state: FSMContext):
    user = str(message.from_user.id)
    url = message.text
    data.get(user, {}).pop(url, 1)
    await state.finish()
    await message.answer('Товар успешно убран')


@dp.message_handler(commands=['list'])
async def print_list(message: types.Message):
    user_id = str(message.from_user.id)
    data_check = copy.deepcopy(data)
    urls = data_check.get(user_id, {}).keys()
    output = ''
    for url in urls:
        parse = Parse(url)
        output += f'{parse.get_info()}\n{url}\n\n'
        await asyncio.sleep(2)
    output = output[:-2] if len(output) > 0 else 'Список пуст'
    await message.answer(output, disable_web_page_preview=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(check_prices())
    loop.create_task(save_data(data))
    executor.start_polling(dp, skip_updates=True, loop=loop, on_startup=print('Я родился!'))
