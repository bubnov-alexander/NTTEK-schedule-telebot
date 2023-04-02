from settings import cursor, database
from parser_1 import getpari
from openAI import send_openai
import pytz,requests,json,time,random, datetime as dt
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

tz = pytz.timezone('Asia/Yekaterinburg')
page = 1
predmeti = ['Теория вероятностей', 'Математика', 'Сопровождение ИС', 'ОС и среды ', 'Информационные технологии', 'ОБЖ']

#ГЛАВНОЕ МЕНЮ
def menu(bot, callback):
    
    markup=InlineKeyboardMarkup(row_width=3)
    item1 = InlineKeyboardButton(text = "📋Расписание📋", callback_data = "📋Расписание📋")
    item2 = InlineKeyboardButton(text = "👥Преподаватели👥", callback_data = "👥Преподаватели👥")
    item3 = InlineKeyboardButton(text = "🛠Настройки🛠", callback_data = "🛠Настройки🛠")
    item5 = InlineKeyboardButton(text = "📒О боте📒", callback_data = "📒О боте📒")
    cursor.execute('''SELECT user_id FROM admin WHERE user_id = ?''', (callback.chat.id, ))
    admin = 510441193
    if callback.chat.id != admin:
        markup.add(item1, item2, item3,item5)
        try:
            bot.edit_message_text(chat_id=callback.chat.id, message_id=callback.id, text = 'Вот что я могу сделать: '.format(callback.from_user),  parse_mode='html', reply_markup=markup)
        except:
            bot.send_message(callback.chat.id, 'Вот что я могу сделать: '.format(callback.from_user),  parse_mode='html', reply_markup=markup)
    else:
        item6 = InlineKeyboardButton("Admin panel", callback_data = "Admin panel")
        markup.add(item1, item2, item3,item5, item6)
        try:
            bot.edit_message_text(chat_id=callback.chat.id, message_id=callback.id, text = 'Вот что я могу сделать: '.format(callback.from_user),  parse_mode='html', reply_markup=markup)

        except:
            bot.send_message(callback.chat.id, 'Вот что я могу сделать: '.format(callback.from_user),  parse_mode='html', reply_markup=markup)

def group(bot,callback):
    markup = InlineKeyboardMarkup(row_width=3)
    item1 = InlineKeyboardButton(text = "Моя группа", callback_data = 'f_group')
    item7 = InlineKeyboardButton(text = "Excel", callback_data = "excel")
    item5 = InlineKeyboardButton(text = "Сайт с расписанием", url = 'https://a.nttek.ru/')
    item4 = InlineKeyboardButton(text = "🔔Расписание звонков", callback_data = 'bells')
    item6 = InlineKeyboardButton(text = "Преподаватель", callback_data = 'teacher')
    item8 = InlineKeyboardButton(text = "Другая группа", callback_data = 'another_group')
    back = InlineKeyboardButton(text = '🔙Назад', callback_data = 'close')
    markup.add(item1, item7, item8, item6)
    markup.add(item4, item5)
    markup.add(back)
    try:
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = 'Выбери расписание какой группы ты хочешь узнать: ',  parse_mode='html', reply_markup=markup)
    except:
        bot.send_message(callback.message.chat.id, 'Выбери расписание какой группы ты хочешь узнать: ',  parse_mode='html', reply_markup=markup)

#ВЫВОД РАСПИСАНИЯ
def parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, group, who):
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 3
    site = requests.get(f'https://erp.nttek.ru/api/schedule/legacy').text
    sitedate = json.loads(site)
    sitedate.sort(key=lambda x: time.mktime(time.strptime(x,"%d.%m.%Y")))

    if (len(sitedate)) <= 5:
        a = 0
    else:
        a = ((len(sitedate)) - 5)

    if group == 'group':
        for i in range(a, len(sitedate)):
            date1 = int(dt.datetime.weekday(dt.datetime.strptime(sitedate[i].replace('.','-'), '%d-%m-%Y')))
            date2 = ''

            if date1 > 2:
                if date1 == 3:
                    date2 = ('Четверг')
                elif date1 == 4:
                    date2 = ('Пятница')
                elif date1 == 5:
                    date2 = ('Суббота')
            elif date1 < 2:
                if date1 == 1:
                    date2 = ('Вторник')
                elif date1 == 0:
                    date2 = ('Понедельник')
            else:
                date2 = ('Среда')

            keyboard.add (InlineKeyboardButton(f'{sitedate[i]} ({date2})', callback_data = f'{sitedate[i], who}'))
        item1 = (InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
        item3 = (InlineKeyboardButton('Преподаватели', callback_data = 'teacher'))
        item2 = (InlineKeyboardButton('Твоя группа', callback_data = 'f_group'))
        close = (InlineKeyboardButton('Меню', callback_data = 'close2'))
        keyboard.add(item1, item3, item2)
        keyboard.add(close)
        try:
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Выберите день на который хотите узнать расписание\nгруппы {who}', parse_mode='html', reply_markup = keyboard)
        except:
            bot.send_message(callback.message.chat.id, f'Выберите день на который хотите узнать расписание\nгруппы {who}', parse_mode='html', reply_markup = keyboard)

    elif group == 'teacher':
        for i in range(a, len(sitedate)):
            date1 = int(dt.datetime.weekday(dt.datetime.strptime(sitedate[i].replace('.','-'), '%d-%m-%Y')))
            date2 = ''

            if date1 > 2:
                if date1 == 3:
                    date2 = ('Четверг')
                elif date1 == 4:
                    date2 = ('Пятница')
                elif date1 == 5:
                    date2 = ('Суббота')
            elif date1 < 2:
                if date1 == 1:
                    date2 = ('Вторник')
                elif date1 == 0:
                    date2 = ('Понедельник')
            else:
                date2 = ('Среда')
            keyboard.add (InlineKeyboardButton(f'{sitedate[i]} ({date2})', callback_data = f'препод{sitedate[i], who}'))
        item1 = (InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
        item3 = (InlineKeyboardButton('Преподаватели', callback_data = 'teacher'))
        item2 = (InlineKeyboardButton('Твоя группа', callback_data = 'f_group'))
        close = (InlineKeyboardButton('Меню', callback_data = 'close2'))
        keyboard.add(item1, item3, item2)
        keyboard.add(close)
        try:
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Выберите день на который хотите узнать расписание преподавателя {who}', parse_mode='html', reply_markup = keyboard)
        except:
            bot.send_message(callback.message.chat.id, f'Выберите день на который хотите узнать расписание преподавателя {who}', parse_mode='html', reply_markup = keyboard)

    elif group == 'excel':
        for i in range(a, len(sitedate)):
            date1 = int(dt.datetime.weekday(dt.datetime.strptime(sitedate[i].replace('.','-'), '%d-%m-%Y')))
            date2 = ''

            if date1 > 2:
                if date1 == 3:
                    date2 = ('Четверг')
                elif date1 == 4:
                    date2 = ('Пятница')
                elif date1 == 5:
                    date2 = ('Суббота')
            elif date1 < 2:
                if date1 == 1:
                    date2 = ('Вторник')
                elif date1 == 0:
                    date2 = ('Понедельник')
            else:
                date2 = ('Среда')
            keyboard.add (InlineKeyboardButton(f'{sitedate[i]} ({date2})', callback_data = f'excel {sitedate[i]}'))
        item1 = (InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
        item3 = (InlineKeyboardButton('Преподаватели', callback_data = 'teacher'))
        item2 = (InlineKeyboardButton('Твоя группа', callback_data = 'f_group'))
        close = (InlineKeyboardButton('Меню', callback_data = 'close2'))
        keyboard.add(item1, item3, item2)
        keyboard.add(close)
        try:
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = 'Выберите день на который хотите узнать расписание', parse_mode='html', reply_markup = keyboard)
        except:
            bot.send_message(callback.message.chat.id, 'Выберите день на который хотите узнать расписание', parse_mode='html', reply_markup = keyboard)

#Получить информацию из базы данных о пользователе
def defuser(bot, message, InlineKeyboardMarkup, InlineKeyboardButton):
    cursor.execute('''SELECT user_id FROM admin WHERE user_id = ?''', (message.chat.id, ))
    admin = 510441193
    if message.chat.id != admin:
        bot.send_message(message.chat.id, f'У тебя нету доступа к такой команде', parse_mode='html')
        menu(bot, message)
    else:
        cursor.execute('''SELECT * FROM users''')
        global user
        user = cursor.fetchall()
        global page
        markup = InlineKeyboardMarkup()
        back = InlineKeyboardButton(text = '🔙Назад', callback_data = 'close')
        markup.row_width = 1
        max = page * 10
        min = max - 10
        a = 0
        b = 0
        if page == 0:
            page = page + 1

        for i in user[min:max:]:
            string = str(i[3])
            if string != 'None':
                markup.add (InlineKeyboardButton(text = f'{i[0]} | {string}', callback_data = string))
                a = a + 1
                b = b + a
            else:
                string = str(i[2])
                markup.add (InlineKeyboardButton(text = f'{i[0]} | {string}', callback_data = string))
                a = a + 1
                b = b + a
        if page == 1:
            amount_plus = InlineKeyboardButton(text = 'Вперёд -->', callback_data = '+1')
            maxpage = InlineKeyboardButton(text = 'Конец', callback_data='maxpage')
            markup.add (maxpage, amount_plus, row_width = 4)
            markup.add(back)
            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text = f'**Список {page}**', parse_mode='markdown', reply_markup = markup)
            except:
                bot.send_message (message.chat.id, text = f'**Список {page}**', parse_mode='markdown', reply_markup = markup)

        elif a < 10:
            amount_minus = InlineKeyboardButton(text = '<-- Назад', callback_data = '-1')
            start = InlineKeyboardButton(text = 'Начало', callback_data='minpage')
            maxpage = InlineKeyboardButton(text = 'Конец', callback_data='maxpage')
            markup.add(amount_minus, start,maxpage, row_width = 4)
            markup.add(back)
            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text = f'**Список {page}**', parse_mode='markdown', reply_markup = markup)
            except:
                bot.send_message(message.chat.id, text = f'**Список {page}**', parse_mode='markdown', reply_markup = markup)
        else:
            amount_minus = InlineKeyboardButton(text = '<-- Назад', callback_data = '-1')
            amount_plus = InlineKeyboardButton(text = 'Вперёд -->', callback_data = '+1')
            start = InlineKeyboardButton(text = 'Начало', callback_data='minpage')
            maxpage = InlineKeyboardButton(text = 'Конец', callback_data='maxpage')
            markup.add (amount_minus, start, maxpage, amount_plus, row_width = 4)
            markup.add(back)
            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text = f'**Список {page}**', parse_mode='markdown', reply_markup = markup)
            except:
                bot.send_message(message.chat.id, text = f'**Список {page}**', parse_mode='markdown', reply_markup = markup)

# callback
def mycallback(bot, callback):
    TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
    #ПОЛУЧЕНИЕ ДНЕЙ НА КОТОРЫЕ ЕСТЬ РАСПИСАНИЕ
    site = requests.get(f'https://erp.nttek.ru/api/schedule/legacy').text
    sitedate = json.loads(site)
    sitedate.sort(key=lambda x: time.mktime(time.strptime(x,"%d.%m.%Y")))
    if (len(sitedate)) <= 5:
        a = 0
    else:
        a = ((len(sitedate)) - 5)

        #ВЫВОД ОПРЕДЕЛЁННОЙ ГРУППЫ (ДНЕЙ)

    #ГРУППЫ
    if callback.data == '📋Расписание📋':
        group(bot, callback)

    elif callback.data == 'print':
        print('Ты 4мо')

# #ЗВОНКИ
    elif callback.data == 'bells':
        photo = open('data/photo.jpg', 'rb')
        markup_inline = InlineKeyboardMarkup()
        url1 = InlineKeyboardButton (text = '📅Полное расписание📅', url=f'https://a.nttek.ru')
        back = InlineKeyboardButton(text = '🔙Назад', callback_data = 'close2')
        markup_inline.add(url1, back)
        bot.send_photo(callback.message.chat.id, photo, reply_markup=markup_inline)
        

#ПРЕПОДЫ
    elif callback.data == "👥Преподаватели👥":
        f = open('data/Prepod.txt', 'r', encoding='UTF-8')
        thinks = f.read()
        f.close()
        markup_inline = InlineKeyboardMarkup()
        markup_inline.add(InlineKeyboardButton(text = '🔙Назад', callback_data = 'close'))
        TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
        DATE = (dt.datetime.now(tz)).strftime('%d.%m')
        print(f'{TIME} {DATE}| Пользователь {callback.from_user.username} {callback.from_user.first_name} узнал преподов!')
        with open("data/logs.txt", "a+", encoding="utf-8") as f:
            f.write(f'\n{TIME} {DATE}| Пользователь {callback.from_user.username} {callback.from_user.first_name} узнал преподов!')
        try:
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = thinks, parse_mode='html', reply_markup=markup_inline)
        except:
            bot.send_message(callback.message.chat.id, thinks, parse_mode='html', reply_markup=markup_inline)
            

#🛠Настройки🛠
    elif callback.data == "🛠Настройки🛠":
        markup = InlineKeyboardMarkup()
        url1 = InlineKeyboardButton (text = '🔔Вкл уведомления', callback_data = 'n_YES')
        url2 = InlineKeyboardButton (text = '🔕Выкл уведомления', callback_data = 'n_NO')
        url3 = InlineKeyboardButton (text = '👯Добавить мою группу', callback_data = 'add_f_group')
        back = InlineKeyboardButton (text = '🔙Назад', callback_data = 'close')
        markup.add(url1,url2)
        markup.add(url3)
        markup.add(back)
        try:
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = "Нажми на кнопку взависимости от твоего желания!", parse_mode='html', reply_markup=markup)
        except:
            bot.send_message(callback.message.chat.id, "Нажми на кнопку взависимости от твоего желания!", parse_mode='html', reply_markup=markup)

    #АДМИН ПАНЕЛЬ
    elif callback.data == 'Admin panel':
        markup = InlineKeyboardMarkup()
        item1 = InlineKeyboardButton(text = 'Пользователи', callback_data = 'users')
        item2 = InlineKeyboardButton(text = 'Логи', callback_data = 'logs')
        item3 = InlineKeyboardButton(text = 'Отправить сообщение', callback_data = 'send_message')
        back = InlineKeyboardButton(text = '🔙Назад', callback_data = 'close')
        markup.add(item1, item2, item3, back)
        try:
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = 'Выбери что-то из предложенного: ', parse_mode = 'html', reply_markup = markup)
        except:
            bot.send_message(callback.message.chat.id, 'Выбери что-то из предложенного: ', parse_mode = 'html', reply_markup = markup)


    elif callback.data == '🥸OpenAI🥸':
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Отмена', callback_data = 'close'))
        try:
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = 'Задай вопрос!', reply_markup=keyboard)
        except:
            bot.send_message(callback.message.chat.id, text = 'Задай вопрос!', reply_markup=keyboard)
        def openai_send(message):
            send_openai(message.text, bot, callback, InlineKeyboardMarkup, InlineKeyboardButton)
            bot.delete_message(message.chat.id, message.message_id)
        bot.register_next_step_handler(callback.message, openai_send)

#О БОТЕ
    elif callback.data == '📒О боте📒':
        f = open('data/About bot.txt', 'r', encoding='UTF-8')
        facts = f.read()
        markup_inline = InlineKeyboardMarkup()
        url1 = InlineKeyboardButton (text = '🙍🏻‍♂️Вк', url='https://vk.com/mem445')
        url2 = InlineKeyboardButton (text = '💌Отзыв', callback_data= 'review')
        url3 = InlineKeyboardButton (text = '💸Поддержка автора', url='https://www.donationalerts.com/r/kinoki445', callback_data = 'print')
        back = InlineKeyboardButton(text = '🔙Назад', callback_data = 'close')
        markup_inline.add(url1,url2)
        markup_inline.add(url3)
        markup_inline.add(back)
        TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
        DATE = (dt.datetime.now(tz)).strftime('%d.%m')
        print(f'{TIME} {DATE}| Пользователь {callback.from_user.username} {callback.from_user.first_name} узнал о боте!')
        with open("data/logs.txt", "a+", encoding="utf-8") as f:
            f.write(f'\n{TIME} {DATE}| Пользователь {callback.from_user.username} {callback.from_user.first_name} узнал о боте')

        try:
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = facts, parse_mode='html', reply_markup=markup_inline)
        except:
            bot.send_message(callback.message.chat.id, facts, parse_mode='html', reply_markup=markup_inline)
        f.close()

    elif callback.data == 'f_group':
        try:
            bot.clear_step_handler_by_chat_id(chat_id=callback.message.chat.id)
        except:
            pass
        cursor.execute(f'SELECT f_group FROM users WHERE user_id = {callback.message.chat.id}')
        data = cursor.fetchone()
        try:
            if data[0] is None:
                bot.send_message(callback.message.chat.id, 'У тебя нету твоей группы, добавь её в настройках, если нету настроек напиши menu', parse_mode='html')
            else:
                parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, 'group', f'{data[0]}')
        except Exception as e:
            print(e)
            bot.send_message(callback.message.chat.id, 'Какая-то ошибка, пиши @Kinoki445', parse_mode='html')
    
    elif callback.data == 'another_group':
        try:
            bot.clear_step_handler_by_chat_id(chat_id=callback.message.chat.id)
        except:
            pass
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Отмена', callback_data = 'close2'))
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = 'Введи название группы, пример (2ИС6) Без - и пробелов: ', reply_markup = keyboard)
        def another_group(message):
            try:
                parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, 'group', message.text.upper())
                bot.delete_message(message.chat.id, message.message_id)
            except Exception as e:
                bot.send_message(chat_id = 510441193, text = f'Пользователь {message.from_user.username} {message.from_user.first_name} ввёл неверно группу {message.text}')
                bot.send_message(callback.message.chat.id, f'Такой группы не существует', parse_mode='html')
        bot.register_next_step_handler(callback.message, another_group)

    elif callback.data == 'teacher':
        try:
            bot.clear_step_handler_by_chat_id(chat_id=callback.message.chat.id)
        except:
            pass
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Отмена', callback_data = 'close2'))
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = 'Введи фамилию преподавателя, пример (Зятикова ТЮ) Без - и  через пробел: ', reply_markup = keyboard)
        def another_teacher(message):
            try:
                parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, 'teacher', message.text)
                bot.delete_message(message.chat.id, message.message_id)
            except Exception as e:
                bot.send_message(chat_id = 510441193, text = f'Пользователь {message.from_user.username} {message.from_user.first_name} ввёл неверно группу {message.text}')
                bot.send_message(callback.message.chat.id, f'Такой группы не существует', parse_mode='html')
        bot.register_next_step_handler(callback.message, another_teacher)
        
    elif callback.data =='excel':
        parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, 'excel', 'excel')

    elif callback.data == 'close2':
        try:
            bot.clear_step_handler_by_chat_id(chat_id=callback.message.chat.id)
        except:
            pass
        group(bot, callback)

    for i in range(a, len(sitedate)):
        if callback.data[0:6:] != 'препод':
            if callback.data[0:10:] == f'{sitedate[i]}':
                getpari(callback.data[0:10:], 'group', callback.data[11::], InlineKeyboardMarkup, InlineKeyboardButton, bot, callback)
                TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
                DATE = (dt.datetime.now(tz)).strftime('%d.%m')
                print(f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил {callback.data[11::]}! В', TIME)
                try:
                    with open("data/logs.txt", "a+", encoding="utf-8") as f:
                        f.write(f'\n{TIME} {DATE}| Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил {callback.data[11::]}!')
                except:
                        pass
                
            elif callback.data[2:12:] == f'{sitedate[i]}':
                TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
                DATE = (dt.datetime.now(tz)).strftime('%d.%m')
                print(f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил {callback.data[16:-2:]}! В', TIME)
                try:
                    with open("data/logs.txt", "a+", encoding="utf-8") as f:
                        f.write(f'\n{TIME} {DATE}| Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил {callback.data[16:-2:]}!')
                except:
                    pass
                getpari(callback.data[2:12:], 'group', callback.data[16:-2:], InlineKeyboardMarkup, InlineKeyboardButton, bot, callback)

            elif callback.data[0:18:] == f"excel {sitedate[i]}":
                getpari(callback.data[6:18:], 'excel', sitedate[i], InlineKeyboardMarkup, InlineKeyboardButton, bot, callback)
                TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
                DATE = (dt.datetime.now(tz)).strftime('%d.%m')
                print(f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил excel {sitedate[i]}! В', TIME)
                try:
                    with open("data/logs.txt", "a+", encoding="utf-8") as f:
                        f.write(f'\n{TIME} {DATE}| Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил excel {sitedate[i]}!')
                except:
                        pass
        
        elif callback.data[0:18:] == f"препод('{sitedate[i]}":
            getpari(callback.data[8:18:], 'teacher', callback.data[22:-2:], InlineKeyboardMarkup, InlineKeyboardButton, bot, callback)
            TIME = (dt.datetime.now(tz)).strftime('%H:%M:%S')
            DATE = (dt.datetime.now(tz)).strftime('%d.%m')
            print(f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил {callback.data[22:-2:]}! В', TIME)
            try:
                with open("data/logs.txt", "a+", encoding="utf-8") as f:
                    f.write(f'\n{TIME} {DATE}| Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил {callback.data[22:-2:]}!')
            except:
                pass

    if callback.data == 'add_f_group':
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Отмена', callback_data = 'close'))
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = 'Введи свою группу, например: "2ИС6" без " - и т.п ', reply_markup=keyboard)
        def add_user_ban(message):
            try:
                cursor.execute(f'''UPDATE users SET f_group = '{message.text}' WHERE user_id = {callback.message.chat.id}''')
                database.commit()
                bot.send_message(callback.message.chat.id, 'Я успешно обновил твою группу!', parse_mode='html')
                menu(bot, callback.message)
            except:
                bot.send_message(callback.message.chat.id, 'Появилась какая-то ошибка, обратись к @kinoki445', parse_mode='html')
                menu(bot, callback.message)
        bot.register_next_step_handler(callback.message, add_user_ban)

    elif callback.data == 'review':
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Отмена', callback_data = 'close'))
        try:
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = 'Напиши свой отзыв: ', reply_markup=keyboard)
        except:
            bot.send_message(callback.message.chat.id, 'Напиши свой отзыв: ', reply_markup=keyboard)
        def review(message):
            try:
                cursor.execute(f'''UPDATE users SET review = '{message.text}' WHERE user_id = {callback.message.chat.id}''')
                database.commit()
                bot.send_message(callback.message.chat.id, 'Благодарю за твоё мнение о боте)', parse_mode='html')
                bot.send_message(chat_id = 510441193, text = f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} написал отзыв: \n{message.text}')
                menu(bot, callback.message)
            except:
                bot.send_message(callback.message.chat.id, 'Появилась какая-то ошибка, обратись к @kinoki445', parse_mode='html')
                menu(bot, callback.message)
        bot.register_next_step_handler(callback.message, review)

    elif callback.data == 'n_YES':
        try:
            cursor.execute(f'UPDATE users SET notice = {1} WHERE user_id = {callback.message.chat.id}')
            database.commit()
            bot.send_message(callback.message.chat.id, 'Теперь тебе будут приходить мои сообщения :)', parse_mode='html')
            menu(bot, callback.message)
        except:
            bot.send_message(callback.message.chat.id, 'Появилась какая-то ошибка, обратись к @kinoki445', parse_mode='html')
            menu(bot, callback.message)

    elif callback.data == 'n_NO':
        try:
            cursor.execute(f'UPDATE users SET notice = {0} WHERE user_id = {callback.message.chat.id}')
            database.commit()
            bot.send_message(callback.message.chat.id, 'Теперь тебе не будут приходить мои сообщения :)', parse_mode='html')
            menu(bot, callback.message)
        except:
            bot.send_message(callback.message.chat.id, 'Появилась какая-то ошибка, обратись к @kinoki445', parse_mode='html')
            menu(bot, callback.message)

    elif callback.data == 'logs':
        markup_inline = InlineKeyboardMarkup()
        url1 = InlineKeyboardButton (text = 'Логи', callback_data='logs_choice')
        url2 = InlineKeyboardButton (text = 'Файл', callback_data='log_file')
        back = InlineKeyboardButton(text = '🔙Назад', callback_data = 'close')
        markup_inline.add(url1,url2,back)
        try:
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = 'Что хочешь?', parse_mode='html', reply_markup=markup_inline)
        except:
            bot.send_message(callback.message.chat.id, 'Что хочешь?', parse_mode='html', reply_markup=markup_inline)

    elif callback.data == 'logs_choice':
        markup = InlineKeyboardMarkup()
        back = InlineKeyboardButton(text = '🔙Назад', callback_data = 'close')
        markup.add(back)
        bot.reply_to(callback.message, f'Введи количество строк', reply_markup=markup)
        def logs_choice(message):
            f1 = open("data/logs.txt", "r")
            a = f1.readlines()[-(int(message.text)):]
            text = ''
            for i in a:
                text = (text + i)
            print(text)
            bot.send_message(callback.message.chat.id, f'{text}')
            f1.close()
        bot.register_next_step_handler(callback.message, logs_choice)

    elif callback.data == 'log_file':
        markup = InlineKeyboardMarkup()
        back = InlineKeyboardButton(text = '🔙Назад', callback_data = 'close')
        markup.add(back)
        f = open("data/logs.txt","rb")
        bot.send_document(callback.message.chat.id,f,reply_markup=markup)
        f.close()

    elif callback.data == 'send_message':
        cursor.execute('''SELECT user_id FROM admin WHERE user_id = ?''', (callback.message.chat.id, ))
        admin = cursor.fetchone()
        if admin is None:
            bot.send_message(callback.message.chat.id, text = 'У тебя нету прав', parse_mode='html')
            menu(bot, callback.message)
        else:
            markup = InlineKeyboardMarkup()
            back = InlineKeyboardButton(text = '🔙Назад', callback_data = 'close')
            markup.add(back)
            bot.reply_to(callback.message, 'Что ты хочешь написать?', reply_markup = markup)
            def send(message, count = 0):
                cursor.execute(f'SELECT user_id FROM users WHERE notice = {1}')
                lol = cursor.fetchall()
                count = 0
                while count != len(lol):
                        for row in lol:
                            try:
                                bot.forward_message(row[0], message.chat.id, message.id)
                                count += 1
                            except:
                                count += 1
                menu(bot, message)
            bot.register_next_step_handler(callback.message, send)

    elif callback.data == 'users':
        defuser(bot, callback.message, InlineKeyboardMarkup, InlineKeyboardButton)

    elif callback.data == 'close':
        try:
            bot.clear_step_handler_by_chat_id(chat_id=callback.message.chat.id)
        except:
            pass
        menu(bot, callback.message)

    elif callback.data == '+1':
        global page 
        page += 1
        defuser(bot, callback.message, InlineKeyboardMarkup, InlineKeyboardButton)

    elif callback.data == '-1':
        page -= 1
        defuser(bot, callback.message, InlineKeyboardMarkup, InlineKeyboardButton)

    elif callback.data == 'maxpage':
        cursor.execute('''SELECT * FROM users''')
        user = cursor.fetchall()
        page = len(user) // 10
        defuser(bot, callback.message, InlineKeyboardMarkup, InlineKeyboardButton)
    
    elif callback.data == 'minpage':
        page = 1
        defuser(bot, callback.message, InlineKeyboardMarkup, InlineKeyboardButton)

    try:      
        cursor.execute('''SELECT * FROM users''')
        user = cursor.fetchall()
        for i in user:
            if callback.data == i[3]:
                bot.send_message(callback.message.chat.id, text = 
                (
                f'Номер: {str(i[0])}\n'
                f'Имя: {str(i[2])}\n'
                f'id: {str(i[1])}\n'
                f'Nickname: {str(i[3])}\n'
                f'Отзыв: {str(i[5])}\n'
                f'Уведомление: {str(i[4])}\n'
                f'Group: {str(i[6])}\n'
                f'Regist: {str(i[7])}\n'
                ))
                bot.answer_callback_query(callback_query_id=callback.id, show_alert=False)

            elif callback.data == str(i[2]):
                bot.send_message(callback.message.chat.id, text = 
                (
                f'Номер: {str(i[0])}\n'
                f'Имя: {str(i[2])}\n'
                f'id: {str(i[1])}\n'
                f'Nickname: {str(i[3])}\n'
                f'Отзыв: {str(i[5])}\n'
                f'Уведомление: {str(i[4])}\n'
                f'Group: {str(i[6])}\n'
                f'Regist: {str(i[7])}\n'
                ))
                bot.answer_callback_query(callback_query_id=callback.id, show_alert=False)
    except:
        bot.answer_callback_query(callback_query_id=callback.id, show_alert=False)