from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv

from app import database as db
from app import keyboards as kb
from app import text
from app import parser
from app import openAI as ai

import os
import datetime as dt
import pytz
import time as tm

tz = pytz.timezone('Asia/Yekaterinburg')

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)

# ============== Start bot ==============


async def on_startup(_):
    await db.db_start()
    TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
    DATE = (dt.datetime.now(tz)).strftime('%d.%m')
    print('Бот запущен:', TIME)
    with open("data/logs.txt", "a+", encoding='UTF-8') as f:
        f.write(f'\n{TIME} {DATE}| Бот запущен')

# ============== Comand /start ==============


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await db.db_table_val(message, bot)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вы авторизовались как администратор!', reply_markup=kb.main_admin)
    else:
        await message.answer(f'{message.from_user.first_name}, добро пожаловать в @nttek_2is6_bot\nБота с расписанием колледжа НТТЭК!', reply_markup=kb.main)

# ============== Comand /menu ==============


@dp.message_handler(commands=['menu'])
async def cmd_start(message: types.Message):
    await db.db_table_val(message, bot)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вот что я могу сделать: ', reply_markup=kb.main_admin)
    else:
        await message.answer(f'Вот что я могу сделать: ', reply_markup=kb.main)

@dp.message_handler(commands=['add_group_id'])
async def start(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        await message.answer(f"Привет! Это личное сообщение. Если хочешь добавить свою группу в БД, пиши /add_group_id в группе которую хочешь добавить, перед этим боту нужно дать все права! Если хочешь удалить из БД: /delete_group_id\nБудут вопросы пиши: @kinoki445")

    elif message.chat.type == types.ChatType.GROUP or message.chat.type == types.ChatType.SUPERGROUP:        
        await db.db_table_group(message, bot)
        await message.answer(f"Я успешно добавил твою группу в Базу Данных")

@dp.message_handler(commands=['delete_group_id'])
async def start(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        await message.answer(f"Привет! Это личное сообщение. Если хочешь удалить свою группу в БД, пиши /delete_group_id в группе которую хочешь удалить, перед этим боту нужно дать все права! Если хочешь вернуть группу в БД: /add_group_id \nБудут вопросы пиши: @kinoki445")

    elif message.chat.type == types.ChatType.GROUP or message.chat.type == types.ChatType.SUPERGROUP:        
        await db.delete_group(message, bot)
        await message.answer(f"Я успешно удалил твою группу из Базы Данных")


# ============== Admin panel ==============


@dp.message_handler(text='admin')
async def admin_panel(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Вот что я могу сделать: ', reply_markup=kb.admin_panel)
        await bot.delete_message(message.chat.id, message.message_id)
    else:
        message_to_bot = message.text.lower()
        if message.content_type.lower() == 'text':
            if message_to_bot == 'меню' or message_to_bot == 'menu':
                await message.answer('Вот что я могу сделать: ', reply_markup=kb.main_admin)
                await bot.delete_message(message.chat.id, message.message_id)
            else:
                await bot.send_message(message.chat.id, f'Вы написали: {message.text}\nЕсли хотите узнать что может бот напишите /menu\nБудут вопросы пишите: @Kinoki445', parse_mode='html')
                TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
                DATE = (dt.datetime.now(tz)).strftime('%d.%m')
                print(
                    f'{TIME} {DATE} | Пользователь @{message.from_user.username} {message.from_user.first_name} написал {message.text}')
                await bot.delete_message(message.chat.id, message.message_id)
                try:
                    with open("data/logs.txt", "a+", encoding='UTF-8') as f:
                        f.write(
                            f'\n{TIME} {DATE}| Пользователь @{message.from_user.username} {message.from_user.first_name} написал {message.text}')
                except:
                    pass

# ============== Another text(message) ==============


@dp.message_handler()
async def answer(message: types.Message):
    message_to_bot = message.text.lower()
    if message.content_type.lower() == 'text':
        if message_to_bot == 'меню' or message_to_bot == 'menu':
            await message.answer('Вот что я могу сделать: ', reply_markup=kb.main_admin)
            await bot.delete_message(message.chat.id, message.message_id)
        else:
            await bot.send_message(message.chat.id, f'Вы написали: {message.text}\nЕсли хотите узнать что может бот напишите /menu\nБудут вопросы пишите: @Kinoki445', parse_mode='html')
            TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
            DATE = (dt.datetime.now(tz)).strftime('%d.%m')
            print(f'{TIME} {DATE} | Пользователь @{message.from_user.username} {message.from_user.first_name} написал {message.text}')
            await bot.delete_message(message.chat.id, message.message_id)
            try:
                with open("data/logs.txt", "a+", encoding='UTF-8') as f:
                    f.write(
                        f'\n{TIME} {DATE}| Пользователь @{message.from_user.username} {message.from_user.first_name} написал {message.text}')
            except:
                pass

# ============== FSM Machne ==============


class my_fsm(StatesGroup):
    all_message = State()
    send_about = State()
    review = State()
    change_fgroup = State()
    select_another_group = State()
    teacher = State()
    message_toai = State()

# ============== FSM Send message ==============


@dp.callback_query_handler(text='send_message')
async def send_message_all_users(callback: types.CallbackQuery):
    await my_fsm.all_message.set()
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Напишите что хотите отправить пользователям!', reply_markup=kb.close2)


@dp.message_handler(state=my_fsm.all_message)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data = message.text
    await db.send_all_message(data, message, bot)
    await message.answer('Сообщение успешно отправилось', reply_markup=kb.main_admin)
    await state.finish()
# ============== FSM another_group ==============


@dp.callback_query_handler(text='another_group')
async def select_another_group(callback: types.CallbackQuery):
    await my_fsm.select_another_group.set()
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text='Напиши название группы пример: 3ИС6', reply_markup=kb.close2)


@dp.message_handler(state=my_fsm.select_another_group)
async def select_another_group_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data = message.text
    await kb.parimiy(bot, message, "group", data)
    await state.finish()

# ============== FSM teacher ==============


@dp.callback_query_handler(text='teacher')
async def select_teacher(callback: types.CallbackQuery):
    await my_fsm.teacher.set()
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text='Напиши преподователя пример: Зятикова ТЮ', reply_markup=kb.close2)


@dp.message_handler(state=my_fsm.teacher)
async def select_teacher_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data = message.text
    await kb.parimiy(bot, message, "teacher", data)
    await state.finish()

# ============== FSM change_fgroup ==============


@dp.callback_query_handler(text='add_f_group')
async def change_fgroup(callback: types.CallbackQuery):
    await my_fsm.change_fgroup.set()
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text='Напиши название группы пример: 3ИС6', reply_markup=kb.close2)


@dp.message_handler(state=my_fsm.change_fgroup)
async def change_fgroup_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data = message.text
    await db.change_fgroup(data, message, bot)
    await state.finish()


# ============== FSM review ==============


@dp.callback_query_handler(text='review')
async def review(callback: types.CallbackQuery):
    await my_fsm.review.set()
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text='Напиши своё мнение о боте', reply_markup=kb.close2)


@dp.message_handler(state=my_fsm.review)
async def review_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data = message.text
    await db.review(data, message, bot)
    await state.finish()

# ============== FSM openai ==============

@dp.callback_query_handler(text='openai')
async def toai(callback: types.CallbackQuery):
    await my_fsm.message_toai.set()
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text='Напиши что хочешь спросить', reply_markup=kb.close2)


@dp.message_handler(state=my_fsm.message_toai)
async def toai_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data = message.text
    await ai.send_openai(data, bot, message)
    await state.finish()

# ============== FSM cancel ==============


@dp.callback_query_handler(state="*", text='close_callback')
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Я отменил твой запрос', reply_markup=kb.main)
    await state.finish()


# ============== callback data ==============
@dp.callback_query_handler()
async def callback_query_keyboard(callback: types.CallbackQuery):
    if callback.data == '📋Расписание📋':
        try:
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        text='Выбери расписание какой группы ты хочешь узнать: ',  parse_mode='html', reply_markup=kb.schedule)
        except:
            await callback.message.delete()
            await bot.send_message(chat_id=callback.message.chat.id, text='Вот что я могу сделать: ', reply_markup=kb.schedule)

    elif callback.data == '👥Преподаватели👥':
        TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
        DATE = (dt.datetime.now(tz)).strftime('%d.%m')
        print(f'{TIME} {DATE}| Пользователь @{callback.from_user.username} {callback.from_user.first_name} узнал преподов!')
        with open("data/logs.txt", "a+", encoding='UTF-8') as f:
            f.write(
                f'\n{TIME} {DATE}| Пользователь @{callback.from_user.username} {callback.from_user.first_name} узнал преподов!')
        await bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id, text=text.teacher, parse_mode="HTML", reply_markup=kb.close)

    elif callback.data == '🛠Настройки🛠':
        await bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id, text='Нажми на кнопку взависимости от твоего желания!', reply_markup=kb.settings)

    elif callback.data == '📒О боте📒':
        TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
        DATE = (dt.datetime.now(tz)).strftime('%d.%m')
        print(f'{TIME} {DATE}| Пользователь @{callback.from_user.username} {callback.from_user.first_name} узнал о боте!')
        with open("data/logs.txt", "a+", encoding='UTF-8') as f:
            f.write(
                f'\n{TIME} {DATE}| Пользователь @{callback.from_user.username} {callback.from_user.first_name} узнал о боте')
        await bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id, text=text.about_bot, parse_mode="HTML", reply_markup=kb.about_bot)

    elif callback.data == 'f_group':
        await db.check_group(bot, callback, kb.parimiy)

    elif callback.data == 'excel':
        await kb.parimiy(bot, callback, 'excel', '')

    elif callback.data == 'bells':
        photo = open('data/bell.jpg', 'rb')
        await callback.message.delete()
        await bot.send_photo(chat_id=callback.message.chat.id, photo=photo, reply_markup=kb.bell)

    elif callback.data == 'Admin panel':
        await bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id, text='Вот что я могу сделать: ', reply_markup=kb.admin_panel)

    elif callback.data == 'notifications':
        await bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id, text='Нажми на кнопку взависимости от твоего желания!', reply_markup=kb.notifications)

    elif callback.data == 'n_YES':
        await db.change_message('yes', bot, callback)

    elif callback.data == 'n_NO':
        await db.change_message('no', bot, callback)

    elif callback.data == 'schedule_notif':
        await bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id, text='Нажми на кнопку взависимости от твоего желания!', reply_markup=kb.schedule_notif)

    elif callback.data == 'n_not_YES':
        await db.change_schedule_notif('yes', bot, callback)

    elif callback.data == 'n_not_NO':
        await db.change_schedule_notif('no', bot, callback)

    elif callback.data == 'logs':
        f = open("data/logs.txt", "rb")
        await bot.send_document(callback.message.chat.id, f, reply_markup=kb.close)
        f.close()

    elif callback.data == 'send_all_about':
        await db.send_all_about(callback, bot)

    elif callback.data == 'close':
        if callback.from_user.id == int(os.getenv('ADMIN_ID')):
            try:
                await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Вот что я могу сделать: ', reply_markup=kb.main_admin)
            except:
                await callback.message.delete()
                await callback.message.answer(f'Вот что я могу сделать: ', reply_markup=kb.main_admin)
        else:
            await callback.message.delete()
            await callback.message.answer(f'Вот что я могу сделать: ', reply_markup=kb.main)


# ============== Select shedles ==============


# ============== Select group ==============

    elif callback.data[0:4] == 'расп':
        await parser.getpari(callback.data[5:15], 'group', callback.data[16::], bot, callback, 'расп')
        TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
        DATE = (dt.datetime.now(tz)).strftime('%d.%m')
        print(
            f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил {callback.data[16::]} {callback.data[5:15]}! В', TIME)
        try:
            with open("data/logs.txt", "a+", encoding='UTF-8') as f:
                f.write(
                    f'\n{TIME} {DATE}| Пользователь @{callback.message.chat.username} {callback.message.chat.first_name} запросил {callback.data[16::]} {callback.data[5:15]}!')
        except:
            pass

# ============== Select excel ==============

    elif callback.data[0:4] == 'расе':
        await parser.getpari(callback.data[5:15], 'excel', callback.data[16::], bot, callback, 'расе')
        TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
        DATE = (dt.datetime.now(tz)).strftime('%d.%m')
        print(
            f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил excel {callback.data[5:15]}! В', TIME)
        try:
            with open("data/logs.txt", "a+", encoding='UTF-8') as f:
                f.write(
                    f'\n{TIME} {DATE}| Пользователь @{callback.message.chat.username} {callback.message.chat.first_name} запросил excel {callback.data[5:15]}!')
        except:
            pass

# ============== Select teacher ==============

    elif callback.data[0:4] == 'раст':
        await parser.getpari(callback.data[5:15], 'teacher', callback.data[16::], bot, callback, 'раст')
        TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
        DATE = (dt.datetime.now(tz)).strftime('%d.%m')
        print(
            f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил {callback.data[16::]} {callback.data[5:15]}! В', TIME)
        try:
            with open("data/logs.txt", "a+", encoding='UTF-8') as f:
                f.write(
                    f'\n{TIME} {DATE}| Пользователь @{callback.message.chat.username} {callback.message.chat.first_name} запросил {callback.data[16::]} {callback.data[5:15]}!')
        except:
            pass

# ============== Start __main__ ==============

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
