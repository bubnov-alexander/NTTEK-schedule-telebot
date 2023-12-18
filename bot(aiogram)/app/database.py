import sqlite3
import datetime
import pytz
import os
from app import keyboards as kb
from app import text as tx

tz = pytz.timezone('Asia/Yekaterinburg')
TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
DATE = (datetime.datetime.now(tz)).strftime('%d.%m')

# ============== Create tables ==============

async def db_start():
    global database, cursor
    database = sqlite3.connect(
        'data/database.db', check_same_thread=False, timeout=7)
    cursor = database.cursor()
    print("Подключен к SQLite3")
    with open("data/logs.txt", "a+", encoding='UTF-8') as f:
        f.write(f'\n{TIME} {DATE}| Подключен к SQLite3')

    cursor.execute("""CREATE TABLE IF NOT EXISTS 'group'(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        group_id INTEGER UNIQUE NOT NULL,
        group_name TEXT NOT NULL,
        group_description STRING,
        join_date DATETIME NOT NULL
        )""")
    database.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        user_id INTEGER UNIQUE NOT NULL,
        user_name TEXT NOT NULL,
        username STRING,
        notice INTEGER NOT NULL DEFAULT 1,
        schedule INTEGER NOT NULL DEFAULT 1,
        review TEXT,
        f_group STRING,
        join_date DATETIME NOT NULL
        )""")
    database.commit()

# ============== Check and send new shuld ==============

async def send_newshuld(bot, sitedate):
    with open('data/last_data.txt', 'w', encoding='UTF-8') as f:
        f.write(f'{sitedate[0:1]}')
    lol = cursor.execute(
        f'SELECT user_id FROM users WHERE schedule = {1}').fetchall()
    lol += (cursor.execute(
        f'SELECT group_id FROM "group"').fetchall())
    
    count = 0
    while count != len(lol):
        for row in lol:
            try:
                await bot.send_message(chat_id=row[0], text=f'Добавили новое расписание!\nЕсли тебе не нравится это уведомление ты всегда можешь выключить его в настройках /menu')
                count += 1
            except:
                count += 1

# ============== Select Y/N my message ==============

async def change_message(type, bot, callback):
    if type == 'yes':
        try:
            cursor.execute(
                f'UPDATE users SET notice = {1} WHERE user_id = {callback.message.chat.id}')
            database.commit()
            await bot.send_message(callback.message.chat.id, 'Теперь тебе будут приходить мои сообщения :)', parse_mode='html')
        except:
            await bot.send_message(callback.message.chat.id, 'Появилась какая-то ошибка, обратись к @kinoki445', parse_mode='html')
    elif type == 'no':
        try:
            cursor.execute(
                f'UPDATE users SET notice = {0} WHERE user_id = {callback.message.chat.id}')
            database.commit()
            await bot.send_message(callback.message.chat.id, 'Теперь тебе не будут приходить мои сообщения :)', parse_mode='html')
        except:
            await bot.send_message(callback.message.chat.id, 'Появилась какая-то ошибка, обратись к @kinoki445', parse_mode='html')

# ============== Select Y/N new scheld ==============

async def change_schedule_notif(type, bot, callback):
    if type == 'yes':
        try:
            cursor.execute(
                f'UPDATE users SET schedule = {1} WHERE user_id = {callback.message.chat.id}')
            database.commit()
            await bot.send_message(callback.message.chat.id, 'Теперь тебе будут приходить уведомления о новом расписание :)', parse_mode='html')
        except:
            await bot.send_message(callback.message.chat.id, 'Появилась какая-то ошибка, обратись к @kinoki445', parse_mode='html')
    elif type == 'no':
        try:
            cursor.execute(
                f'UPDATE users SET schedule = {0} WHERE user_id = {callback.message.chat.id}')
            database.commit()
            await bot.send_message(callback.message.chat.id, 'Теперь тебе не будут приходить уведомления о новом расписание :)', parse_mode='html')
        except:
            await bot.send_message(callback.message.chat.id, 'Появилась какая-то ошибка, обратись к @kinoki445', parse_mode='html')

# ============== Check favorite group ==============

async def check_group(bot, callback, parimiy):
    cursor.execute(
        f'SELECT f_group FROM users WHERE user_id = {callback.message.from_user.id}')
    data = cursor.fetchone()
    if data == None:
        cursor.execute(
            f'SELECT f_group FROM users WHERE user_id = {callback.from_user.id}')
        data = cursor.fetchone()
    else:
        pass
    try:
        if data[0] is None:
            await bot.send_message(callback.message.chat.id, 'У тебя нету твоей группы, добавь её в настройках, /menu', parse_mode='html')
        else:
            await parimiy(bot, callback, 'group', f'{data[0]}')
    except Exception as e:
        print(e)
        await bot.send_message(callback.message.chat.id, 'Какая-то ошибка, пиши @Kinoki445', parse_mode='html')

# ============== Send all users message ==============

async def send_all_message(text, message, bot):
    cursor.execute(f'SELECT user_id FROM users')
    lol = cursor.fetchall()
    count = 0

    while count != len(lol):
        for row in lol:
            try:
                # Пересылаем сообщение из текущего чата в другой чат (замените chat_id на нужный)
                await bot.forward_message(chat_id=row[0], from_chat_id=message.chat.id, message_id=message.message_id)
                count += 1
            except:
                count += 1
                
async def send_all_about(callback, bot):
    cursor.execute(f'SELECT user_id FROM users')
    lol = cursor.fetchall()
    count = 0
    while count != len(lol):
        for row in lol:
            try:
                await bot.send_message(row[0], text=tx.about_bot, parse_mode="HTML", reply_markup=kb.about_bot)
                count += 1
            except:
                count += 1

# ============== Change favorite group ==============

async def change_fgroup(text, message, bot):
    cursor.execute(
        f'''UPDATE users SET f_group = '{text}' WHERE user_id = {message.chat.id}''')
    database.commit()
    await bot.send_message(message.chat.id, 'Я успешно обновил твою группу!', parse_mode='html', reply_markup=kb.main)

# ============== Send review ==============

async def review(text, message, bot):
    cursor.execute(
        f'''UPDATE users SET review = '{text}' WHERE user_id = {message.chat.id}''')
    database.commit()
    await bot.send_message(message.chat.id, 'Благодарю за твоё мнение о боте)', parse_mode='html', reply_markup=kb.main)
    await bot.send_message(chat_id=os.getenv('ADMIN_ID'), text=f'Пользователь @{message.chat.username} {message.chat.first_name} написал отзыв: \n{text}')

# ============== New users ==============

async def db_table_val(message, bot):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    username = message.from_user.username
    today = datetime.date.today()
    joindate = today.strftime('%d.%m.%Y')
    user = cursor.execute(
        f'SELECT * FROM users WHERE user_id = {us_id} ').fetchone()
    if user is None:
        cursor.execute('INSERT INTO users (user_id, user_name, username, join_date) VALUES (?, ?, ?, ?)',
                    (us_id, us_name, username, joindate))
        database.commit()
        await bot.send_message(chat_id=os.getenv('ADMIN_ID'), text=f'Зарегестрировался новый пользователь! @{username}, {us_name}')
        print(f'Пользователь {message.from_user.username} {message.from_user.first_name} зарегестрировался! в', (
            datetime.datetime.now(tz).strftime('%H:%M:%S')))
        with open("data/logs.txt", "a+", encoding='UTF-8') as f:
            f.write(
                f'\n{TIME} {DATE}| Пользователь {message.from_user.username} {message.from_user.first_name} зарегестрировался!')
            
async def db_table_group(message, bot):
    chat_id = message.chat.id
    chat_info = await bot.get_chat(chat_id)
    # Выводим название группы и ее описание
    group_name = chat_info.title
    group_description = chat_info.description

    today = datetime.date.today()
    joindate = today.strftime('%d.%m.%Y')
    user = cursor.execute(
        f'SELECT * FROM "group" WHERE group_id = {chat_id} ').fetchone()
    if user is None:
        cursor.execute('INSERT INTO "group" (group_id, group_name, group_description, join_date) VALUES (?, ?, ?, ?)',
                    (chat_id, group_name, group_description, joindate))
        database.commit()
        await bot.send_message(chat_id=os.getenv('ADMIN_ID'), text=f'Зарегестрировалась новая группа! @{group_name}, {group_description}')
        print(f'Пользователь {group_name} {group_description} зарегестрировался! в', (
            datetime.datetime.now(tz).strftime('%H:%M:%S')))
        with open("data/logs.txt", "a+", encoding='UTF-8') as f:
            f.write(
                f'\n{TIME} {DATE}| Пользователь {group_name} {group_description} зарегестрировался!')
        
async def delete_group(message, bot):
    # Запрос на удаление записей
    cursor.execute('DELETE FROM "group" WHERE group_id = ?', (message.chat.id,))

    # Подтверждение изменений
    database.commit()