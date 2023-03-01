from settings import *
from parser_1 import *
import pytz,requests,json,time,random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

tz = pytz.timezone('Asia/Yekaterinburg')
page = 1
predmeti = ['Теория вероятностей', 'Математика', 'Сопровождение ИС', 'ОС и среды ', 'Информационные технологии', 'ОБЖ']

#ГЛАВНОЕ МЕНЮ
#argument1.chat.id
#argument2.from_user
def menu(bot, argument1, argument2):
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = KeyboardButton("📋Расписание📋")
    item2 = KeyboardButton("👥Преподаватели👥")
    item3 = KeyboardButton("👬Студенты группы👬")
    item4 = KeyboardButton("📖ДЗ📖")
    item5 = KeyboardButton("📒О боте📒")
    cursor.execute('''SELECT user_id FROM admin WHERE user_id = ?''', (argument1.chat.id, ))
    admin = 510441193
    if argument1.chat.id != admin:
        markup.add(item1, item2, item5)
        bot.send_message(argument1.chat.id, 'Вот что я могу сделать: '.format(argument2.from_user),  parse_mode='html', reply_markup=markup)
    else:
        item6 = KeyboardButton("Admin panel")
        markup.add(item1, item2, item3, item4, item5, item6)
        bot.send_message(argument1.chat.id, 'Вот что я могу сделать: '.format(argument2.from_user),  parse_mode='html', reply_markup=markup)
        
#ГРУППЫ
def group(bot, message):
    markup = InlineKeyboardMarkup(row_width=3)
    item1 = InlineKeyboardButton(text = "2ИС6", callback_data = '2is6')
    item2 = InlineKeyboardButton(text = "2ИС3", callback_data = "2is3")
    item3 = InlineKeyboardButton(text = "2Р5", callback_data = "2r5")
    item7 = InlineKeyboardButton(text = "Excel", callback_data = "excel")
    item5 = InlineKeyboardButton(text = "Сайт с расписанием", url = 'https://a.nttek.ru/')
    item4 = InlineKeyboardButton(text = "🔔Расписание звонков", callback_data = 'bells')
    item6 = InlineKeyboardButton(text = "Преподаватель", callback_data = 'teacher')
    back = InlineKeyboardButton(text = "Другая группа", callback_data = 'another_group')
    markup.add(item1, item2, item3, item7,back, item6)
    markup.add(item4, item5)
    bot.send_message(message.chat.id, 'Выбери расписание какой группы ты хочешь узнать: ',  parse_mode='html', reply_markup=markup)

def send_message_users(bot, message):
    markup = InlineKeyboardMarkup(row_width=2)
    item1 = InlineKeyboardButton(text = "Отправить", callback_data = 'sm')
    back = InlineKeyboardButton(text = "Назад", callback_data = 'another_group')
    markup.add(item1, back)
    bot.send_message(message.chat.id, 'Что ты хочешь?',  parse_mode='html', reply_markup=markup)


#АДМИН ПАНЕЛЬ
def adminpanel(bot, argument1, argument2):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = KeyboardButton('Пользователи')
    item2 = KeyboardButton('Права доступа')
    item3 = KeyboardButton('Отправить сообщение')
    back = KeyboardButton('🔙Назад')
    markup.add(item1, item2, item3, back)
    bot.send_message(argument1.chat.id, 'Выбери что-то из предложенного: ', parse_mode = 'html', reply_markup = markup)


#ВЫВОД РАСПИСАНИЯ
def parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, group, who):
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 2
    site = requests.get(f'https://erp.nttek.ru/api/schedule/legacy').text
    sitedate = json.loads(site)
    sitedate.sort(key=lambda x: time.mktime(time.strptime(x,"%d.%m.%Y")))

    if (len(sitedate)) <= 5:
        a = 0
    else:
        a = ((len(sitedate)) - 5)

    if group == 'group':
        for i in range(a, len(sitedate)):
            keyboard.add (InlineKeyboardButton(f'{sitedate[i]} {who}', callback_data = f'{sitedate[i], who}'))
        item1 = (InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
        item3 = (InlineKeyboardButton('Преподаватели', callback_data = 'teacher'))
        item2 = (InlineKeyboardButton('Меню', callback_data = 'close'))
        keyboard.add(item1, item3, item2)
        bot.send_message(callback.message.chat.id, 'Выберите день на который хотите узнать расписание', parse_mode='html', reply_markup = keyboard)

    elif group == 'teacher':
        for i in range(a, len(sitedate)):
            keyboard.add (InlineKeyboardButton(f'{sitedate[i]} {who}', callback_data = f'препод{sitedate[i], who}'))
        item1 = (InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
        item3 = (InlineKeyboardButton('Преподаватели', callback_data = 'teacher'))
        item2 = (InlineKeyboardButton('Меню', callback_data = 'close'))
        keyboard.add(item1, item3, item2)
        bot.send_message(callback.message.chat.id, 'Выберите день на который хотите узнать расписание', parse_mode='html', reply_markup = keyboard)

    elif group == 'excel':
        for i in range(a, len(sitedate)):
            keyboard.add (InlineKeyboardButton(f'{sitedate[i]} {who}', callback_data = f'excel {sitedate[i]}'))
        item1 = (InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
        item3 = (InlineKeyboardButton('Преподаватели', callback_data = 'teacher'))
        item2 = (InlineKeyboardButton('Меню', callback_data = 'close'))
        keyboard.add(item1, item3, item2)
        bot.send_message(callback.message.chat.id, 'Выберите день на который хотите узнать расписание', parse_mode='html', reply_markup = keyboard)
        

#ПРЕПОДЫ
def prepod(bot, message):
    f = open('data/Prepod.txt', 'r', encoding='UTF-8')
    thinks  = f.read()
    f.close()
    bot.send_message(message.chat.id, thinks, parse_mode='html')

#ЗВОНКИ
def zvonok(bot, callback):
    photo = open('data/photo.jpg', 'rb')
    markup_inline = InlineKeyboardMarkup()
    url1 = InlineKeyboardButton (text = '📅Полное расписание📅', url=f'https://a.nttek.ru')
    markup_inline.add(url1)
    bot.send_photo(callback.message.chat.id, photo, reply_markup=markup_inline)

#СТУДЕНТЫ
def groupstudents(bot, message):
    f = open('data/Student.txt', 'r', encoding='UTF-8')
    facts = f.read()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = KeyboardButton("🔁Рандомно выбрать студента🔁")
    back = KeyboardButton("🔙Назад")
    markup.add(item1, back)
    bot.send_message(message.chat.id, facts, parse_mode='html', reply_markup=markup)
    f.close()

#РАНДОМ
def myrandom(bot, message):
    file = open('data/Student.txt', 'r', encoding='UTF-8')
    lines = []
    for line in file:
        lines.append(line)
    random_line = random.choice(lines)
    file.close()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, random_line, parse_mode='html', reply_markup=markup)

#О БОТЕ
def aboutbot(bot, message):
    f = open('data/About bot.txt', 'r', encoding='UTF-8')
    facts = f.read()
    markup_inline = InlineKeyboardMarkup()
    url1 = InlineKeyboardButton (text = 'Вк', url='https://vk.com/mem445')
    url2 = InlineKeyboardButton (text = 'Телеграмм', url= 'https://t.me/Kinoki445')
    url3 = InlineKeyboardButton (text = 'Вк куратора группы', url= 'https://vk.com/id31107453')
    markup_inline.add(url1,url2, url3)
    bot.send_message(message.chat.id, facts, parse_mode='html', reply_markup=markup_inline)
    f.close()

#При появление ошибок
def error(bot):
    bot.send_message(chat_id = 510441193, text = f'В боте появилась ошибка!')  

#Панель ДЗ
def homework(bot, message, InlineKeyboardMarkup, InlineKeyboardButton):
    try:
        cursor.execute('''SELECT user_id FROM homeworker WHERE user_id = ?''', (message.chat.id, ))
        homeworker = cursor.fetchone()
        if homeworker is None:
            markup = InlineKeyboardMarkup()
            para = InlineKeyboardButton(text = 'Выбрать предмет ', callback_data='dz')
            markup.add(para, row_width = 3)
            bot.send_message(message.chat.id, text = 'Выбери что-то из предложенного: ', parse_mode='html', reply_markup=markup)
        else:
            markup = InlineKeyboardMarkup()
            para = InlineKeyboardButton(text = 'Выбрать предмет ', callback_data='dz')
            hw = InlineKeyboardButton(text = 'Добавить ДЗ', callback_data= 'addhw')
            markup.add(para,hw, row_width = 3)
            bot.send_message(message.chat.id, text = 'Выбери что-то из предложенного: ', parse_mode='html', reply_markup=markup)
    except:
        markup = InlineKeyboardMarkup()
        para = InlineKeyboardButton(text = 'Выбрать предмет ', callback_data='dz')
        markup.add(para, row_width = 3)
        bot.send_message(message.chat.id, text = 'Выбери что-то из предложенного: ', parse_mode='html', reply_markup=markup)


#Получить информацию из базы данных о пользователе
def defuser(bot, message, InlineKeyboardMarkup, InlineKeyboardButton):
    cursor.execute('''SELECT user_id FROM admin WHERE user_id = ?''', (message.chat.id, ))
    admin = 510441193
    if message.chat.id != admin:
        bot.send_message(message.chat.id, f'У тебя нету доступа к такой команде', parse_mode='html')
        menu(bot, message, message)
    else:
        cursor.execute('''SELECT * FROM users''')
        global user
        user = cursor.fetchall()
        global page
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        max = page * 5
        min = max - 5
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
            close = InlineKeyboardButton(text = 'Закрыть', callback_data='close')
            markup.add (close, amount_plus, row_width = 2)
            bot.send_message (message.chat.id, text = f'**Список {page}**', parse_mode='markdown', reply_markup = markup)

        elif a < 5:
            amount_minus = InlineKeyboardButton(text = '<-- Назад', callback_data = '-1')
            close = InlineKeyboardButton(text = 'Закрыть', callback_data='close')
            markup.add(amount_minus, close, row_width = 2)
            bot.send_message (message.chat.id, text = f'**Список {page}**', parse_mode='markdown', reply_markup = markup)

        else:
            amount_minus = InlineKeyboardButton(text = '<-- Назад', callback_data = '-1')
            amount_plus = InlineKeyboardButton(text = 'Вперёд -->', callback_data = '+1')
            close = InlineKeyboardButton(text = 'Закрыть', callback_data='close')
            markup.add (amount_minus, close, amount_plus, row_width = 3)
            bot.send_message (message.chat.id, text = f'**Список {page}**', parse_mode='markdown', reply_markup = markup)

#Получить информацию из базы данных о пользователе для callback
def defuser2(bot, callback, InlineKeyboardMarkup, InlineKeyboardButton):
    cursor.execute('''SELECT * FROM users''')
    global user
    user = cursor.fetchall()
    global page
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    max = page * 5
    min = max - 5
    a = 0
    if page == 0:
            page = page + 1

    for i in user[min:max:]:
        string = str(i[3])
        if string != 'None':
            markup.add (InlineKeyboardButton(text = f'{i[0]} | {string}', callback_data = string))
            a = a + 1
        else:
            string = str(i[2])
            markup.add (InlineKeyboardButton(text = f'{i[0]} | {string}', callback_data = string))
            a = a + 1
    if page == 1:
        amount_plus = InlineKeyboardButton(text = 'Вперёд -->', callback_data = '+1')
        close = InlineKeyboardButton(text = 'Закрыть', callback_data='close')
        markup.add (close, amount_plus, row_width = 2)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'**Список {page}**', parse_mode='markdown', reply_markup = markup)

    elif a < 5:
        amount_minus = InlineKeyboardButton(text = '<-- Назад', callback_data = '-1')
        close = InlineKeyboardButton(text = 'Закрыть', callback_data='close')
        markup.add(amount_minus, close, row_width = 2)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'**Список {page}**', parse_mode='markdown', reply_markup = markup)

    else:
        amount_minus = InlineKeyboardButton(text = '<-- Назад', callback_data = '-1')
        amount_plus = InlineKeyboardButton(text = 'Вперёд -->', callback_data = '+1')
        close = InlineKeyboardButton(text = 'Закрыть', callback_data='close')
        markup.add (amount_minus, close, amount_plus, row_width = 3)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'**Список {page}**', parse_mode='markdown', reply_markup = markup)

#Панель прав
def root(bot, argument1, argument2):
    markup = InlineKeyboardMarkup(row_width=4)
    item1 = InlineKeyboardButton(text = 'BAN', callback_data = 'banbase')
    item2 = InlineKeyboardButton(text = 'ДЗ', callback_data = 'dzbase')
    item3 = InlineKeyboardButton(text = 'admin', callback_data = 'adminbase')
    item4 = InlineKeyboardButton(text=' logs', callback_data='logs')
    back = InlineKeyboardButton(text = '🔙Назад', callback_data='close')
    markup.add(item1, item2, item3,item4, back)
    bot.send_message(argument1.chat.id, text = 'Выбери что-то из предложенного:  ', parse_mode='html', reply_markup=markup)

# callback
def mycallback(bot, callback):
    TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
    #ПОЛУЧЕНИЕ ДНЕЙ НА КОТОРЫЕ ЕСТЬ РАСПИСАНИЕ
    site = requests.get(f'https://erp.nttek.ru/api/schedule/legacy').text
    sitedate = json.loads(site)

    # a = int((sitedate[0])[0:2:])
    # print (a)
    # f = open("info.txt", "w+")
    # b = f.readline()
    # n = int(b)
    # print(n)
    # if a == n:
    #     print('Равно')
        
    sitedate.sort(key=lambda x: time.mktime(time.strptime(x,"%d.%m.%Y")))
    if (len(sitedate)) <= 5:
        a = 0
    else:
        a = ((len(sitedate)) - 5)

    #ВЫВОД ОПРЕДЕЛЁННОЙ ГРУППЫ (ДНЕЙ)
    if callback.data == '2is6':
        parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, 'group', '2ИС6')
    elif callback.data == '2r5':
        parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, 'group', '2Р5')
    elif callback.data == '2is3':
        parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, 'group', '2ИС3')
    
    elif callback.data == 'another_group':
        bot.reply_to(callback.message, 'Введи название группы, пример "2ИС6" Без - и пробелов: ')
        def another_group(message):
            try:
                parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, 'group', message.text.upper())
            except Exception as e:
                bot.send_message(chat_id = 510441193, text = f'Пользователь {message.from_user.username} {message.from_user.first_name} ввёл неверно группу {message.text}')
                bot.send_message(callback.message.chat.id, f'Такой группы не существует', parse_mode='html')
        bot.register_next_step_handler(callback.message, another_group)

    elif callback.data == 'teacher':
        bot.reply_to(callback.message, 'Введи фамилию преподавателя, пример "Зятикова ТЮ" Без - и  через пробел: ')
        def another_teacher(message):
            try:
                parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, 'teacher', message.text)
            except Exception as e:
                bot.send_message(chat_id = 510441193, text = f'Пользователь {message.from_user.username} {message.from_user.first_name} ввёл неверно группу {message.text}')
                bot.send_message(callback.message.chat.id, f'Такой группы не существует', parse_mode='html')
        bot.register_next_step_handler(callback.message, another_teacher)
        
    elif callback.data =='excel':
        parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, 'excel', 'excel')

    for i in range(a, len(sitedate)):
        if callback.data[0:6:] != 'препод':
            if callback.data[0:10:] == f'{sitedate[i]}':
                getpari(callback.data[0:10:], 'group', callback.data[11::], InlineKeyboardMarkup, InlineKeyboardButton, bot, callback)
                TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
                DATE = (datetime.datetime.now(tz)).strftime('%d.%m')
                print(f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил {callback.data[11::]}! В', TIME)
                with open("data/logs.txt", "a+") as f:
                    f.write(f'\n{TIME} {DATE}| Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил {callback.data[11::]}!')

            elif callback.data[2:12:] == f'{sitedate[i]}':
                TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
                DATE = (datetime.datetime.now(tz)).strftime('%d.%m')
                print(f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил {callback.data[16:-2:]}! В', TIME)
                with open("data/logs.txt", "a+") as f:
                    f.write(f'\n{TIME} {DATE}| Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил {callback.data[16:-2:]}!')
                getpari(callback.data[2:12:], 'group', callback.data[16:-2:], InlineKeyboardMarkup, InlineKeyboardButton, bot, callback)

            elif callback.data[0:18:] == f"excel {sitedate[i]}":
                getpari(callback.data[6:18:], 'excel', sitedate[i], InlineKeyboardMarkup, InlineKeyboardButton, bot, callback)
                TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
                DATE = (datetime.datetime.now(tz)).strftime('%d.%m')
                print(f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил excel {sitedate[i]}! В', TIME)
                with open("data/logs.txt", "a+") as f:
                        f.write(f'\n{TIME} {DATE}| Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил excel {sitedate[i]}!')
        
        elif callback.data[0:18:] == f"препод('{sitedate[i]}":
            getpari(callback.data[8:18:], 'teacher', callback.data[22:-2:], InlineKeyboardMarkup, InlineKeyboardButton, bot, callback)
            TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
            DATE = (datetime.datetime.now(tz)).strftime('%d.%m')
            print(f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил {callback.data[22:-2:]}! В', TIME)
            with open("data/logs.txt", "a+") as f:
                    f.write(f'\n{TIME} {DATE}| Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил {callback.data[22:-2:]}!')
        
    #Работа с DateBase BAN
    if callback.data == 'banbase':
        markup = InlineKeyboardMarkup()
        add_user = InlineKeyboardButton(text = 'Adduser', callback_data= 'add_user_ban')
        close = InlineKeyboardButton(text = '🔙Выйти', callback_data= 'root')
        delete_user = InlineKeyboardButton(text = 'Deleteuser', callback_data= 'del_user_ban')
        cursor.execute('''SELECT user_id FROM ban ''')
        ban = cursor.fetchall()
        for i in range(0, len(ban)):
            markup.add(InlineKeyboardButton(str(ban[i][0]), callback_data = f'{ban[i]}'))
        markup.add(add_user, close, delete_user, row_width = 3)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Все пользователи Базы: ', parse_mode='markdown', reply_markup = markup)

    #ДОБАВИТЬ ПОЛЬЗОВАТЕЛЯ В DateBase ban
    elif callback.data == 'add_user_ban':
        bot.reply_to(callback.message, 'Введи ID пользователя: ')
        def add_user_ban(message):
            try:
                id_user = int(message.text)
                today = datetime.date.today().strftime('%d.%m.%Y')
                cursor.execute('INSERT INTO ban (user_id, user_name, join_date) VALUES (?, ?, ?)', (id_user, callback.message.chat.username, today))
                database.commit()
                bot.send_message(callback.message.chat.id, f'Я добавил в базу данных ban: {message.text}', parse_mode='html')
                root(bot, callback.message, callback.message)
            except:
                bot.send_message(callback.message.chat.id, f'У тебя не получилось: {message.text}', parse_mode='html')
                root(bot, callback.message, callback.message)
        bot.register_next_step_handler(callback.message, add_user_ban)

    elif callback.data == 'logs':
        markup_inline = InlineKeyboardMarkup()
        url1 = InlineKeyboardButton (text = 'Логи', callback_data='logs_choice')
        url2 = InlineKeyboardButton (text = 'Файл', callback_data='log_file')
        markup_inline.add(url1,url2)
        bot.send_message(callback.message.chat.id, 'Что хочешь?', parse_mode='html', reply_markup=markup_inline)

    elif callback.data == 'logs_choice':
        bot.reply_to(callback.message, f'Введи количество строк')
        def logs_choice(message):
            f1 = open("data/logs.txt", "r")
            a = f1.readlines()[-(int(message.text)):]
            bot.send_message(callback.message.chat.id, f'{a}', parse_mode='Markdown')
            f1.close()
        bot.register_next_step_handler(callback.message, logs_choice)

    elif callback.data == 'log_file':
        f = open("data/logs.txt","rb")
        bot.send_document(callback.message.chat.id,f)
        f.close()

    elif callback.data == 'sm':
        cursor.execute('''SELECT user_id FROM admin WHERE user_id = ?''', (callback.message.chat.id, ))
        admin = cursor.fetchone()
        if admin is None:
            bot.send_message(callback.message.chat.id, text = 'У тебя нету прав', parse_mode='html')
            menu(bot, callback.message, callback.message)
        else:
                    bot.reply_to(callback.message, 'Что ты хочешь написать?')
                    def send(message, count = 0):
                        cursor.execute('''SELECT * FROM users''')
                        lol = cursor.fetchall()
                        count = 0
                        while count != len(lol):
                                for row in lol:
                                    try:
                                        bot.send_message(row[1], text = f'{message.text}', parse_mode='html')
                                        count += 1
                                    except:
                                        count += 1
                        menu(bot, message, message)
                    bot.register_next_step_handler(callback.message, send)

    #УДАЛИТЬ ПОЛЬЗОВАТЕЛЯ ИЗ DateBase ban
    elif callback.data == 'del_user_ban':
        bot.reply_to(callback.message, 'Введи ID пользователя: ')
        def del_user_ban(message):
            try:
                id_user = int(message.text)
                cursor.execute('DELETE from ban WHERE user_id = (?)', (id_user,))
                database.commit()
                bot.send_message(callback.message.chat.id, f'Я удалил из базы данных ban: {message.text}', parse_mode='html')
                root(bot, callback.message, callback.message)
            except:
                bot.send_message(callback.message.chat.id, f'У тебя не получилось: {message.text}', parse_mode='html')
                root(bot, callback.message, callback.message)
        bot.register_next_step_handler(callback.message, del_user_ban)


    #Работа с DateBase ДЗ
    elif callback.data == 'dzbase':
        markup = InlineKeyboardMarkup()
        add_user = InlineKeyboardButton(text = 'Adduser', callback_data= 'add_user_dz')
        close = InlineKeyboardButton(text = '🔙Выйти', callback_data= 'root')
        delete_user = InlineKeyboardButton(text = 'Deleteuser', callback_data= 'del_user_dz')
        cursor.execute('''SELECT user_id FROM homeworker ''')
        dz = cursor.fetchall()
        for i in range(0, len(dz)):
            markup.add(InlineKeyboardButton(str(dz[i][0]), callback_data = f'{dz[i]}'))
        markup.add(add_user, close, delete_user, row_width = 3)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Все пользователи Базы: ', parse_mode='markdown', reply_markup = markup)

    #ДОБАВИТЬ ПОЛЬЗОВАТЕЛЯ В DateBase дз
    elif callback.data == 'add_user_dz':
        bot.reply_to(callback.message, 'Введи ID пользователя: ')
        def add_user_dz(message):
            try:
                id_user = int(message.text)
                today = datetime.date.today().strftime('%d.%m.%Y')
                cursor.execute('INSERT INTO homeworker (user_id, user_name, join_date) VALUES (?, ?, ?)', (id_user, callback.message.chat.username, today))
                database.commit()
                bot.send_message(callback.message.chat.id, f'Я добавил в базу данных dz: {message.text}', parse_mode='html')
                root(bot, callback.message, callback.message)
            except:
                bot.send_message(callback.message.chat.id, f'У тебя не получилось: {message.text}', parse_mode='html')
                root(bot, callback.message, callback.message)
        bot.register_next_step_handler(callback.message, add_user_dz)

    #УДАЛИТЬ ПОЛЬЗОВАТЕЛЯ ИЗ DateBase ДЗ
    elif callback.data == 'del_user_dz':
        bot.reply_to(callback.message, 'Введи ID пользователя: ')
        def del_user_dz(message):
            try:
                id_user = int(message.text)
                cursor.execute('DELETE from homeworker WHERE user_id = (?)', (id_user,))
                database.commit()
                bot.send_message(callback.message.chat.id, f'Я удалил из базы данных homeworker: {message.text}', parse_mode='html')
                root(bot, callback.message, callback.message)
            except:
                bot.send_message(callback.message.chat.id, f'У тебя не получилось: {message.text}', parse_mode='html')
                root(bot, callback.message, callback.message)
        bot.register_next_step_handler(callback.message, del_user_dz)

    #Работа с DateBase admin
    elif callback.data == 'adminbase':
        markup = InlineKeyboardMarkup()
        add_user = InlineKeyboardButton(text = 'Adduser', callback_data= 'add_user_admin')
        close = InlineKeyboardButton(text = '🔙Выйти', callback_data= 'root')
        delete_user = InlineKeyboardButton(text = 'Deleteuser', callback_data= 'del_user_admin')
        cursor.execute('''SELECT user_id FROM admin ''')
        admin = cursor.fetchall()
        for i in range(0, len(admin)):
            markup.add(InlineKeyboardButton(str(admin[i][0]), callback_data = f'{admin[i]}'))
        markup.add(add_user, close, delete_user, row_width = 3)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Все пользователи Базы: ', parse_mode='markdown', reply_markup = markup)

    #ДОБАВИТЬ ПОЛЬЗОВАТЕЛЯ В DateBase admin
    elif callback.data == 'add_user_admin':
        bot.reply_to(callback.message, 'Введи ID пользователя: ')
        def add_user_admin(message):
            try:
                id_user = int(message.text)
                today = datetime.date.today().strftime('%d.%m.%Y')
                cursor.execute('INSERT INTO admin (user_id, user_name, join_date) VALUES (?, ?, ?)', (id_user, callback.message.chat.username, today))
                database.commit()
                bot.send_message(callback.message.chat.id, f'Я добавил в базу данных admin: {message.text}', parse_mode='html')
                root(bot, callback.message, callback.message)
            except:
                bot.send_message(callback.message.chat.id, f'У тебя не получилось: {message.text}', parse_mode='html')
                root(bot, callback.message, callback.message)
        bot.register_next_step_handler(callback.message, add_user_admin)
    #УДАЛИТЬ ПОЛЬЗОВАТЕЛЯ ИЗ DateBase admin
    elif callback.data == 'del_user_admin':
        bot.reply_to(callback.message, 'Введи ID пользователя: ')
        def del_user_admin(message):
            try:
                id_user = int(message.text)
                cursor.execute('DELETE from admin WHERE user_id = (?)', (id_user,))
                database.commit()
                bot.send_message(callback.message.chat.id, f'Я удалил из базы данных admin: {message.text}', parse_mode='html')
                root(bot, callback.message, callback.message)
            except:
                bot.send_message(callback.message.chat.id, f'У тебя не получилось: {message.text}', parse_mode='html')
                root(bot, callback.message, callback.message)
        bot.register_next_step_handler(callback.message, del_user_admin)

    #ВЫБОР ДЗ
    elif callback.data == 'dz':
        markup = InlineKeyboardMarkup()
        close = InlineKeyboardButton(text = '🔙Выйти', callback_data= 'close')
        for i in range(0, len(predmeti)):
            markup.add(InlineKeyboardButton(predmeti[i], callback_data = f'{predmeti[i]}DZ'))
        markup.add(close)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Выбери предмет: ', parse_mode='markdown', reply_markup = markup)

    #ДОБАВИТЬ ДЗ
    elif callback.data == 'addhw':
        markup = InlineKeyboardMarkup()
        close = InlineKeyboardButton(text = '🔙Выйти', callback_data= 'close')
        for i in range(0, len(predmeti)):
            markup.add(InlineKeyboardButton(predmeti[i], callback_data = f'{predmeti[i]}HW'))
        markup.add(close)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Выбери предмет: ', parse_mode='markdown', reply_markup = markup)

    #ВЫВОД СПИСКА ПРАВ 
    elif callback.data == 'root':
        root(bot, callback.message, callback.message)

    elif callback.data == 'bells':
        zvonok(bot, callback)

    elif callback.data == 'close':
        menu(bot, callback.message, callback)

    elif callback.data == '+1':
        global page 
        page += 1
        defuser2(bot, callback, InlineKeyboardMarkup, InlineKeyboardButton)

    elif callback.data == '-1': 
        page -= 1
        defuser2(bot, callback, InlineKeyboardMarkup, InlineKeyboardButton)

    for i in range(0, len(predmeti)):
        if callback.data == (f"{predmeti[i]}HW"):
            para = predmeti[i]
            bot.reply_to(callback.message, f'Напиши ДЗ которое задали по {para}', parse_mode='markdown') 
        
            def writehomework(message):
                text = message.text
                f = open(f'data/homework/{para}.txt', 'w+', encoding='UTF-8')
                date = datetime.datetime.now(tz).strftime('%d.%m.%Y')
                f.write(f'Задание заданное {date} числа:\n\n{text}\n\n')
                f.close
                bot.reply_to(message, f'Задание которое я добавил в Базу Данных:\n\n{message.text}\n', parse_mode='markdown')
                homework(bot, message, InlineKeyboardMarkup, InlineKeyboardButton)
                bot.send_message(chat_id = 510441193, text = f'Добавил новое ДЗ! В {para} {message.from_user.username}, {message.from_user.first_name}', parse_mode='Markdown')
                TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
                DATE = (datetime.datetime.now(tz)).strftime('%d.%m')
                print(f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} изменил ДЗ! В {para}', TIME)
                with open("data/logs.txt", "a+") as f:
                    f.write(f'\n{TIME} {DATE}| Пользователь {callback.message.chat.username} {callback.message.chat.first_name} изменил ДЗ!')
            bot.register_next_step_handler(callback.message, writehomework)

        if callback.data == (f'{predmeti[i]}DZ'):
            para = predmeti[i]
            try:
                f = open(f'data/homework/{para}.txt', 'r+', encoding='UTF-8')
                text = f.read()
                bot.send_message(callback.message.chat.id, text, parse_mode='markdown')
                f.close
            except:
                bot.send_message(callback.message.chat.id, f'Дз по {para} пока что нету!', parse_mode='markdown')
            
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
            f'Regist: {str(i[4])}\n'
            ))

        elif callback.data == str(i[2]):
            bot.send_message(callback.message.chat.id, text = 
            (
            f'Номер: {str(i[0])}\n'
            f'Имя: {str(i[2])}\n'
            f'id: {str(i[1])}\n'
            f'Nickname: {str(i[3])}\n'
            f'Regist: {str(i[4])}\n'
            ))
