from parser2 import *
from myrandom import *
from openfile import *
from settings import *
import pytz
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
    if argument1 in admin:
        item6 = KeyboardButton("Admin panel")
        markup.add(item1, item2, item3, item4, item5, item6)
        bot.send_message(argument1, 'Выбери то, вот что я могу тебе предложить: '.format(argument2),  parse_mode='html', reply_markup=markup)
    else:
        markup.add(item1, item2, item3, item4, item5)
        bot.send_message(argument1, 'Выбери то, вот что я могу тебе предложить: '.format(argument2),  parse_mode='html', reply_markup=markup)


#Пары
def group(bot, message):
    markup = InlineKeyboardMarkup(row_width=3)
    item1 = InlineKeyboardButton(text = "2ИС6", callback_data = '2is6')
    item2 = InlineKeyboardButton(text = "2Р5", callback_data = "2r5")
    item3 = InlineKeyboardButton(text = "Расписание куратора", callback_data = "teacher")
    item4 = InlineKeyboardButton(text = "🔔Расписание звонков", callback_data = 'bells')
    back = InlineKeyboardButton(text = "🔙Назад", callback_data = 'back')
    markup.add(item1, item2, item3, item4, back)
    bot.send_message(message.chat.id, 'Выбери расписание какой группы ты хочешь узнать: ',  parse_mode='html', reply_markup=markup)


#ВЫБОР РАСПИСАНИЯ
def parimiy(InlineKeyboardMarkup, InlineKeyboardButton, pari1, bot, callback, group, who):
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 2
    parserdef2(who, group)
    for i in range(0, len(pari1)):
        keyboard.add (InlineKeyboardButton(pari1[i], callback_data = f'{pari1[i]} {who}'))
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
    randomman()
    f1 = open('data/random.txt', 'r', encoding='UTF-8')
    facts = f1.read()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, facts, parse_mode='html', reply_markup=markup)

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

#ДЗ
def homework(bot, message, InlineKeyboardMarkup, InlineKeyboardButton):
    if message not in homeworker:
        markup = InlineKeyboardMarkup()
        para = InlineKeyboardButton(text = 'Выбрать предмет ', callback_data='dz')
        markup.add(para, row_width = 3)
        bot.send_message(message, text = 'Выбери что-то из предложенного: ', parse_mode='html', reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup()
        para = InlineKeyboardButton(text = 'Выбрать предмет ', callback_data='dz')
        hw = InlineKeyboardButton(text = 'Добавить ДЗ', callback_data= 'addhw')
        markup.add(para,hw, row_width = 3)
        bot.send_message(message, text = 'Выбери что-то из предложенного: ', parse_mode='html', reply_markup=markup)


#Получить информацию из базы данных о пользователе
def defuser(bot, message, InlineKeyboardMarkup, InlineKeyboardButton):
    if message not in admin:
         bot.send_message(message, f'У тебя нету доступа к такой команде', parse_mode='html')
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
            bot.send_message (message, text = f'**Список {page}**', parse_mode='markdown', reply_markup = markup)

        elif a < 5:
            amount_minus = InlineKeyboardButton(text = '<-- Назад', callback_data = '-1')
            close = InlineKeyboardButton(text = 'Закрыть', callback_data='close')
            markup.add(amount_minus, close, row_width = 2)
            bot.send_message (message, text = f'**Список {page}**', parse_mode='markdown', reply_markup = markup)

        else:
            amount_minus = InlineKeyboardButton(text = '<-- Назад', callback_data = '-1')
            amount_plus = InlineKeyboardButton(text = 'Вперёд -->', callback_data = '+1')
            close = InlineKeyboardButton(text = 'Закрыть', callback_data='close')
            markup.add (amount_minus, close, amount_plus, row_width = 3)
            bot.send_message (message, text = f'**Список {page}**', parse_mode='markdown', reply_markup = markup)

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

# callback
def mycallback(bot, callback):
    if callback.data == '2is6':
        parimiy(InlineKeyboardMarkup, InlineKeyboardButton, pari1, bot, callback, '.1.3.54', '2is6')
        print(f'Пользователь {callback.from_user.username} запросил 2is6! В', (datetime.datetime.now(tz).strftime('%H:%M:%S')))
        for i in range(0, len(pari1)):
            if callback.data == f"{pari1[i]} 2is6":
                who  = '2is6'
                openfile(f'par{who}/{pari1[i]}.txt', bot, callback, who)

    elif callback.data == '2r5':
        if callback.message.chat.id not in tworfive:
            bot.send_message(callback.message.chat.id, 'Прости ты не из той группы!!! Хочешь смотреть расписание группы 2Р5 пиши создателю! @kinoki445', parse_mode='html')
            print(f'Пользователь {callback.from_user.username} запросил 2r5, но не смог получить, в', (datetime.datetime.now(tz).strftime('%H:%M:%S')))
        else:
            parimiy(InlineKeyboardMarkup, InlineKeyboardButton, pari1, bot, callback, '.2.3.45', '2r5')
            print(f'Пользователь {callback.from_user.username} запросил 2r5! В', (datetime.datetime.now(tz).strftime('%H:%M:%S')))
        for i in range(0, len(pari1)):
            if callback.data == f"{pari1[i]} 2r5":
                who  = '2r5'
                openfile(f'par{who}/{pari1[i]}.txt', bot, callback, who)

    
    elif callback.data == 'teacher':
        parimiy(InlineKeyboardMarkup, InlineKeyboardButton, pari1, bot, callback, '.16', 'teacher')
        print(f'Пользователь {callback.from_user.username} запросил teacher! В', (datetime.datetime.now(tz).strftime('%H:%M:%S')))
        for i in range(0, len(pari1)):
            if callback.data == f"{pari1[i]} teacher":
                who = 'teacher'
                openfile(f'par{who}/{pari1[i]}.txt', bot, callback, who)
    
    elif callback.data == 'bells':
        zvonok(bot, callback)

    elif callback.data == 'back':
        menu(bot, callback.message.chat.id, callback.from_user)

    elif callback.data == 'close':
        menu(bot, callback.message.chat.id, callback.from_user)

    elif callback.data == '+1':
        global page 
        page += 1
        defuser2(bot, callback, InlineKeyboardMarkup, InlineKeyboardButton)

    elif callback.data == '-1': 
        page -= 1
        defuser2(bot, callback, InlineKeyboardMarkup, InlineKeyboardButton)

    elif callback.data == 'dz':
        markup = InlineKeyboardMarkup()
        close = InlineKeyboardButton(text = 'Выйти', callback_data= 'close')
        for i in range(0, len(predmeti)):
            markup.add(InlineKeyboardButton(predmeti[i], callback_data = f'{predmeti[i]}DZ'))
        markup.add(close)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Выбери предмет: ', parse_mode='markdown', reply_markup = markup)

    elif callback.data == 'addhw':
        markup = InlineKeyboardMarkup()
        close = InlineKeyboardButton(text = 'Выйти', callback_data= 'close')
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
                f.write(f'Задание заданное {date} числа:\n{text}\n')
                f.close
                bot.reply_to(message, f'Задание которое я добавил в Базу Данных:\n{message.text}', parse_mode='markdown')
                homework(bot, message.chat.id, InlineKeyboardMarkup, InlineKeyboardButton)
                print(f'Пользователь {message.from_user.username} изменил ДЗ! В', (datetime.datetime.now(tz).strftime('%H:%M:%S')))
            bot.register_next_step_handler(callback.message, writehomework)

        if callback.data == (f'{predmeti[i]}DZ'):
            para = predmeti[i]
            try:
                f = open(f'data/homework/{para}.txt', 'r+', encoding='UTF-8')
                text = f.read()
                print(text)
                bot.send_message(callback.message.chat.id, text, parse_mode='markdown')
                f.close
            except:
                bot.send_message(callback.message.chat.id, 'Дз пока что нету!', parse_mode='markdown')
            
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
    
    