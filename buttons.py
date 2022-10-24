from settings import *
from parser import *
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
    item1 = KeyboardButton("📋Пары📋")
    item2 = KeyboardButton("👥Преподы👥")
    item3 = KeyboardButton("👬Студенты группы👬")
    item4 = KeyboardButton("📖ДЗ📖")
    item5 = KeyboardButton("📒О боте📒")
    cursor.execute('''SELECT user_id FROM admin WHERE user_id = ?''', (argument1.chat.id, ))
    admin = cursor.fetchone()
    if argument1.chat.id not in admin:
        markup.add(item1, item2, item3, item4, item5)
        bot.send_message(argument1.chat.id, 'Выбери то, вот что я могу тебе предложить: '.format(argument2.from_user),  parse_mode='html', reply_markup=markup)
    else:
        item6 = KeyboardButton("Admin panel")
        markup.add(item1, item2, item3, item4, item5, item6)
        bot.send_message(argument1.chat.id, 'Выбери то, вот что я могу тебе предложить: '.format(argument2.from_user),  parse_mode='html', reply_markup=markup)
        
#Пары
def group(bot, message):
    markup = InlineKeyboardMarkup(row_width=3)
    item1 = InlineKeyboardButton(text = "2ИС6", callback_data = '2ИС6')
    item2 = InlineKeyboardButton(text = "2ПСО12", callback_data = "2pso12")
    item3 = InlineKeyboardButton(text = "2Р5", callback_data = "2r5")
    item4 = InlineKeyboardButton(text = "Расписание куратора", callback_data = "teacher")
    item5 = InlineKeyboardButton(text = "🔔Расписание звонков", callback_data = 'bells')
    back = InlineKeyboardButton(text = "🔙Назад", callback_data = 'back')
    markup.add(item1, item2, item3, item4, back)
    bot.send_message(message.chat.id, 'Выбери расписание какой группы ты хочешь узнать: ',  parse_mode='html', reply_markup=markup)

def adminpanel(bot, argument1, argument2):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = KeyboardButton('Пользователи')
    item2 = KeyboardButton('Права доступа')
    back = KeyboardButton('🔙Назад')
    markup.add(item1, item2, back)
    bot.send_message(argument1.chat.id, 'Выбери что-то из предложенного: ', parse_mode = 'html', reply_markup = markup)

#ВЫБОР РАСПИСАНИЯ
def parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, group, who):
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 2
    site = requests.get(f'https://erp.nttek.ru/api/schedule/legacy').text
    sitedate = json.loads(site)
    sitedate.sort(key=lambda x: time.mktime(time.strptime(x,"%d.%m.%Y")))
    for i in range(0, len(sitedate)):
        keyboard.add (InlineKeyboardButton(f'{sitedate[i]} {who}', callback_data = f'{sitedate[i]} {who}'))
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

def error(bot, e):
    bot.send_message(chat_id = 510441193, text = f'В боте появилась ошибка: \n{e}', parse_mode='html')

#ДЗ
def homework(bot, message, InlineKeyboardMarkup, InlineKeyboardButton):
    try:
        cursor.execute('''SELECT user_id FROM homeworker WHERE user_id = ?''', (message.chat.id, ))
        homeworker = cursor.fetchall()[0]
        if message.chat.id not in homeworker:
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
        hw = InlineKeyboardButton(text = 'Добавить ДЗ', callback_data= 'addhw')
        markup.add(para,hw, row_width = 3)
        bot.send_message(message.chat.id, text = 'Выбери что-то из предложенного: ', parse_mode='html', reply_markup=markup)


#Получить информацию из базы данных о пользователе
def defuser(bot, message, InlineKeyboardMarkup, InlineKeyboardButton):
    cursor.execute('''SELECT user_id FROM admin WHERE user_id = ?''', (message.chat.id, ))
    admin = cursor.fetchall()[0]
    if message.chat.id not in admin:
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

def root(bot, argument1, argument2):
    markup = InlineKeyboardMarkup(row_width=4)
    item1 = InlineKeyboardButton(text = '2Р5', callback_data = '2r5base')
    item2 = InlineKeyboardButton(text = 'BAN', callback_data = 'banbase')
    item3 = InlineKeyboardButton(text = 'ДЗ', callback_data = 'dzbase')
    item4 = InlineKeyboardButton(text = 'admin', callback_data = 'adminbase')
    back = InlineKeyboardButton(text = '🔙Назад', callback_data='close')
    markup.add(item1, item2, item3, item4, back)
    bot.send_message(argument1.chat.id, text = 'Выбери что-то из предложенного:  ', parse_mode='html', reply_markup=markup)



# callback
def mycallback(bot, callback):
    site = requests.get(f'https://erp.nttek.ru/api/schedule/legacy').text
    sitedate = json.loads(site)
    sitedate.sort(key=lambda x: time.mktime(time.strptime(x,"%d.%m.%Y")))

    if callback.data == '2ИС6':
        parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, 'group', '2ИС6')
        print(f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил 2is6! В', (datetime.datetime.now(tz).strftime('%H:%M:%S')))
    for i in range(0, len(sitedate)):
        if callback.data == (f'{sitedate[i]} 2ИС6'):
            getpari(sitedate[i], 'group', "2ИС6", InlineKeyboardMarkup, InlineKeyboardButton, bot, callback)

    if callback.data == '2r5':
            parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, 'group', '2Р5')
            print(f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил 2Р5! В', (datetime.datetime.now(tz).strftime('%H:%M:%S')))
    for i in range(0, len(sitedate)):
        if callback.data == (f'{sitedate[i]} 2Р5'):
            getpari(sitedate[i], 'group', "2Р5", InlineKeyboardMarkup, InlineKeyboardButton, bot, callback)

    if callback.data == '2pso12':
            parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, 'group', '2ПСО12')
            print(f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил 2ПСО12! В', (datetime.datetime.now(tz).strftime('%H:%M:%S')))
    for i in range(0, len(sitedate)):
        if callback.data == (f'{sitedate[i]} 2ПСО12'):
            getpari(sitedate[i], 'group', "2ПСО12", InlineKeyboardMarkup, InlineKeyboardButton, bot, callback)
                

    if callback.data == 'teacher':
        pass
    #     parimiy(InlineKeyboardMarkup, InlineKeyboardButton, bot, callback, 'teacher', 'Зятикова ТЮ')
    #     print(f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} запросил Зятикова ТЮ! В', (datetime.datetime.now(tz).strftime('%H:%M:%S')))
    # for i in range(0, len(sitedate)):
    #     if callback.data == (f'{sitedate[i]} Зятикова ТЮ'):
    #         getpari(sitedate[i], 'teacher', "Зятикова ТЮ", InlineKeyboardMarkup, InlineKeyboardButton, bot, callback)
    
    elif callback.data == '2r5base':
        markup = InlineKeyboardMarkup()
        add_user = InlineKeyboardButton(text = 'Adduser', callback_data= 'adduser_tworfive')
        close = InlineKeyboardButton(text = '🔙Выйти', callback_data= 'close')
        delete_user = InlineKeyboardButton(text = 'Deleteuser', callback_data= 'deleteuser_tworfive')
        cursor.execute('''SELECT user_id FROM tworfive ''')
        tworfive = cursor.fetchall()
        for i in range(0, len(tworfive)):
            markup.add(InlineKeyboardButton(str(tworfive[i]), callback_data = f'{tworfive[i]}'))
        markup.add(add_user, close, delete_user, row_width = 3)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Выбери пользователя: ', parse_mode='markdown', reply_markup = markup)

    elif callback.data == 'adduser_tworfive':
        bot.reply_to(callback.message, 'Введи ID пользователя: ')
        def addusertwofive(message):
            tworfive.append(message.text)
            bot.send_message(callback.message.chat.id, f'Я добавил в базу данных: {message.text}', parse_mode='html')
        bot.register_next_step_handler(callback.message, addusertwofive)
        

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

    elif callback.data == 'dz':
        markup = InlineKeyboardMarkup()
        close = InlineKeyboardButton(text = '🔙Выйти', callback_data= 'close')
        for i in range(0, len(predmeti)):
            markup.add(InlineKeyboardButton(predmeti[i], callback_data = f'{predmeti[i]}DZ'))
        markup.add(close)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Выбери предмет: ', parse_mode='markdown', reply_markup = markup)

    elif callback.data == 'addhw':
        markup = InlineKeyboardMarkup()
        close = InlineKeyboardButton(text = '🔙Выйти', callback_data= 'close')
        for i in range(0, len(predmeti)):
            markup.add(InlineKeyboardButton(predmeti[i], callback_data = f'{predmeti[i]}HW'))
        markup.add(close)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Выбери предмет: ', parse_mode='markdown', reply_markup = markup)


    for i in range(0, len(predmeti)):
        if callback.data == (f"{predmeti[i]}HW"):
            para = predmeti[i]
            bot.reply_to(callback.message, f'Напиши ДЗ которое задали по {para}', parse_mode='markdown') 
        
            def writehomework(message):
                text = message.text
                f = open(f'data/homework/{para}.txt', 'a+', encoding='UTF-8')
                date = datetime.datetime.now(tz).strftime('%d.%m.%Y')
                f.write(f'Задание заданное {date} числа:\n{text}\n\n')
                f.close
                bot.reply_to(message, f'Задание которое я добавил в Базу Данных:\n\n{message.text}\n', parse_mode='markdown')
                homework(bot, message, InlineKeyboardMarkup, InlineKeyboardButton)
                bot.send_message(chat_id = 510441193, text = f'Добавил новое ДЗ! В {para} {message.from_user.username}, {message.from_user.first_name}', parse_mode='Markdown')
                print(f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} изменил ДЗ! В {para}', (datetime.datetime.now(tz).strftime('%H:%M:%S')))
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
            f'Nickname: {str(i[3])}\n'
            f'Regist: {str(i[4])}\n'
            )
            , parse_mode='markdown')