import telebot, datetime, pytz, time as tm
from telebot import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from settings import *
from buttons import *

tz = pytz.timezone('Asia/Yekaterinburg')
time = (datetime.datetime.now(tz))

bot = telebot.TeleBot(TOKEN)

#Действия после start
@bot.message_handler(commands=['start'])
def start_message(message):
    cursor.execute('''SELECT user_id FROM admin WHERE user_id = ?''', (message.chat.id, ))
    admin = 510441193
    if message.chat.id != admin:
        bot.send_message(message.from_user.id, f'Добро пожаловать, {message.from_user.first_name}', parse_mode='html')
        db_table_val(message, bot)
        menu(bot, message, message)
    else:
        bot.send_message(message.from_user.id, f'Добро пожаловать, Admin {message.from_user.first_name}', parse_mode='html')
        db_table_val(message, bot)
        menu(bot, message, message)

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.from_user.id, 'Привет, чтобы пользоваться функциями бота тебе достаточно написать "Меню" c большой буквы', parse_mode='html')
    print(f'Пользователь {message.from_user.username} {message.from_user.first_name} написал {message.text} в ', (datetime.datetime.now(tz).strftime('%H:%M:%S')))

#Действия callback
@bot.callback_query_handler(func=lambda callback: callback.data)
def callback(callback):
    mycallback(bot, callback)

#Действия когда пришёл текст
@bot.message_handler(content_types=["text"])
def bot_message(message):
    cursor.execute(f'SELECT id FROM users WHERE user_id = {message.chat.id} ')
    data = cursor.fetchone()
    message_to_bot = message.text.lower()

#Проверка на список забаненых пользователей, а так же есть ли они в БД
    cursor.execute(f'SELECT user_id FROM ban WHERE user_id = {message.chat.id} ')
    ban = cursor.fetchall()
    if message.chat.id not in ban:
        if data is None:
            bot.send_message(message.from_user.id, 'Привет, тебя нету в базе данных, не мог бы ты написать /start ?', parse_mode='html')
            print(f'Пользователь {message.from_user.username} {message.from_user.first_name} зарегестрировался! в', (datetime.datetime.now(tz).strftime('%H:%M:%S')))

        else:
            if message.content_type.lower() == 'text':

                #Преподы
                if message_to_bot == '👥преподы👥' or message_to_bot == 'преподы':
                    prepod(bot, message)
                    print(f'Пользователь {message.from_user.username} {message.from_user.first_name} узнал преподов! В', (datetime.datetime.now(tz).strftime('%H:%M:%S')))

                #Меню
                elif message_to_bot == '🔙назад' or message_to_bot == 'назад':
                    menu(bot, message, message)

                elif message_to_bot == 'меню' or message_to_bot == 'menu':
                    menu(bot, message, message)
                
                #Пользователи из БД
                elif message_to_bot == 'user' or message_to_bot == 'пользователи':
                    defuser(bot, message, InlineKeyboardMarkup, InlineKeyboardButton)

                elif message_to_bot == 'права доступа' or message_to_bot == 'root':
                    root(bot, message, message)

                elif message_to_bot == 'admin panel':
                    adminpanel(bot, message, message)

                #Все группы у которых можно узнать расписание
                elif message_to_bot == 'группы':
                    try:
                        group(bot, message)
                    except:
                        markup = InlineKeyboardMarkup()
                        url1 = InlineKeyboardButton (text = 'Сайт с расписанием: ', url= 'https://a.nttek.ru/')
                        markup.add(url1)
                        bot.send_message(message.chat.id, 'К сожелению сайт с парами сейчас недоступен, но ты можешь воспольззоваться другими функциями бота. \nДля этого напиши "меню"', parse_mode='html',reply_markup=markup)

                #Все группы у которых можно узнать расписание
                elif message_to_bot == '📋пары📋' or message_to_bot == 'пары':
                    try:
                        group(bot, message)
                    except:
                        markup = InlineKeyboardMarkup()
                        url1 = InlineKeyboardButton (text = 'Сайт с расписанием: ', url= 'https://a.nttek.ru/')
                        markup.add(url1)
                        bot.send_message(message.chat.id, 'К сожелению сайт с парами сейчас недоступен, но ты можешь воспольззоваться другими функциями бота. \nДля этого напиши "меню"', parse_mode='html',reply_markup=markup)

                elif message_to_bot == '📖дз📖' or message_to_bot == 'дз':
                    homework(bot, message, InlineKeyboardMarkup, InlineKeyboardButton)
                    print(f'Пользователь {message.from_user.username} {message.from_user.first_name} запросил ДЗ! В', (datetime.datetime.now(tz).strftime('%H:%M:%S')))

                #Студенты группы 
                elif message_to_bot == '👬студенты группы👬' or message_to_bot == 'студенты группы':
                    groupstudents(bot, message)
                    print(f'Пользователь {message.from_user.username} {message.from_user.first_name} запросил студентов в', (datetime.datetime.now(tz).strftime('%H:%M:%S')))
                
                #Рандом пользователя
                elif message_to_bot == '🔁рандомно выбрать студента🔁':
                    myrandom(bot, message)
                    print(f'Пользователь {message.from_user.username} {message.from_user.first_name} запросил рандом! В', (datetime.datetime.now(tz).strftime('%H:%M:%S')))

                #Информация о боте 
                elif message_to_bot == '📒о боте📒' or message_to_bot == 'о боте':
                    aboutbot(bot, message)
                    print(f'Пользователь {message.from_user.username} {message.from_user.first_name} узнал о боте в', (datetime.datetime.now(tz).strftime('%H:%M:%S')))
                
                #Эхо-сообщение
                else:
                    bot.send_message(message.chat.id, f'Вы написали: {message.text}\nЕсли хотите узанть что может бот напишите "меню"', parse_mode='html')
                    print(f'Пользователь {message.from_user.username} {message.from_user.first_name} написал {message.text} в', (datetime.datetime.now(tz).strftime('%H:%M:%S')))

    #Действия если user в бане
    else:
        bot.send_message(message.chat.id, 'Ты в БАНЕ чучело!!! \n Пиши @Kinoki445', parse_mode='html')   
        print(f'Забаненый пользователь {message.from_user.username} {message.from_user.first_name} написал {message.text} в', (datetime.datetime.now(tz).strftime('%H:%M:%S')))

print ('Бот запущен:',time.strftime('%d/%m/%Y %H:%M'))

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        error(bot, e)
        tm.sleep(15)


# bot.polling(none_stop=True)