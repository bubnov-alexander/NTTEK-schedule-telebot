import telebot, datetime, pytz, time as tm
from telebot import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from settings import *
from buttons import *

tz = pytz.timezone('Asia/Yekaterinburg')
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
    bot.send_message(message.from_user.id, 'Привет, чтобы пользоваться функциями бота тебе достаточно написать "Меню" c большой буквы, если что-то не получается пиши мне | @Kinoki445', parse_mode='html')
    TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
    print(f'Пользователь {message.from_user.username} {message.from_user.first_name} написал {message.text} в ', TIME)
    with open("data/logs.txt", "a+") as f:
        f.write(f'\n{TIME} | Пользователь {message.from_user.username} {message.from_user.first_name} написал {message.text}')

@bot.message_handler(commands=['students'])
def students(message):
    groupstudents(bot, message)
    TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
    print(f'Пользователь {message.from_user.username} {message.from_user.first_name} запросил студентов в', TIME)
    with open("data/logs.txt", "a+") as f:
        f.write(f'\n{TIME} | Пользователь {message.from_user.username} {message.from_user.first_name} запросил студентов')

#Действия callback
@bot.callback_query_handler(func=lambda callback: callback.data)
def callback(callback):
    mycallback(bot, callback)

#Действия когда пришёл текст
@bot.message_handler(content_types=["text"])
def bot_message(message):
    TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
    cursor.execute(f'SELECT id FROM users WHERE user_id = {message.chat.id} ')
    data = cursor.fetchone()
    message_to_bot = message.text.lower()

#Проверка на список забаненых пользователей, а так же есть ли они в БД
    cursor.execute(f'SELECT user_id FROM ban WHERE user_id = {message.chat.id} ')
    ban = 5322880119
    if message.chat.id != 5322880119:
        if data is None:
            bot.send_message(message.from_user.id, 'Привет, тебя нету в базе данных, не мог бы ты написать /start ?', parse_mode='html')
        else:
            if message.content_type.lower() == 'text':

                #Преподы
                if message_to_bot == '👥преподаватели👥' or message_to_bot == 'преподы':
                    prepod(bot, message)
                    TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
                    print(f'Пользователь {message.from_user.username} {message.from_user.first_name} узнал преподов! В', TIME)
                    with open("data/logs.txt", "a+") as f:
                        f.write(f'\n{TIME} | Пользователь {message.from_user.username} {message.from_user.first_name} узнал преподов!')
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

                elif message_to_bot == 'отправить сообщение':
                    send_message_users(bot, message)

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
                elif message_to_bot == '📋пары📋' or message_to_bot == 'пары' or message_to_bot == '📋расписание📋' or message_to_bot == 'расписание':
                    try:
                        group(bot, message)
                    except:
                        markup = InlineKeyboardMarkup()
                        url1 = InlineKeyboardButton (text = 'Сайт с расписанием: ', url= 'https://a.nttek.ru/')
                        markup.add(url1)
                        bot.send_message(message.chat.id, 'К сожелению сайт с парами сейчас недоступен, но ты можешь воспольззоваться другими функциями бота. \nДля этого напиши "меню"', parse_mode='html',reply_markup=markup)

                # elif message_to_bot == '📖дз📖' or message_to_bot == 'дз':
                #     homework(bot, message, InlineKeyboardMarkup, InlineKeyboardButton)
                #     print(f'Пользователь {message.from_user.username} {message.from_user.first_name} запросил ДЗ! В', (datetime.datetime.now(tz).strftime('%H:%M:%S')))

                #Студенты группы 
                # elif message_to_bot == '👬студенты группы👬' or message_to_bot == 'студенты группы':
                #     groupstudents(bot, message)
                #     print(f'Пользователь {message.from_user.username} {message.from_user.first_name} запросил студентов в', (datetime.datetime.now(tz).strftime('%H:%M:%S')))
                
                #Рандом пользователя
                elif message_to_bot == '🔁рандомно выбрать студента🔁':
                    myrandom(bot, message)
                    TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
                    print(f'Пользователь {message.from_user.username} {message.from_user.first_name} запросил рандом! В', TIME)
                    with open("data/logs.txt", "a+") as f:
                        f.write(f'\n{TIME} | Пользователь {message.from_user.username} {message.from_user.first_name} узнал преподов!')

                #Информация о боте 
                elif message_to_bot == '📒о боте📒' or message_to_bot == 'о боте':
                    aboutbot(bot, message)
                    TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
                    print(f'Пользователь {message.from_user.username} {message.from_user.first_name} узнал о боте в', TIME)
                    with open("data/logs.txt", "a+") as f:
                        f.write(f'\n{TIME} | Пользователь {message.from_user.username} {message.from_user.first_name} узнал о боте')
                
                #Эхо-сообщение
                else:
                    bot.send_message(message.chat.id, f'Вы написали: {message.text}\nЕсли хотите узанть что может бот напишите "меню"', parse_mode='html')
                    TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
                    print(f'Пользователь {message.from_user.username} {message.from_user.first_name} написал {message.text} в', TIME)
                    with open("data/logs.txt", "a+") as f:
                        f.write(f'\n{TIME} | Пользователь {message.from_user.username} {message.from_user.first_name} написал {message.text}')

    #Действия если user в бане
    else:
        bot.send_message(message.chat.id, 'Ты в БАНЕ чучело!!! \n Пиши @Kinoki445', parse_mode='html')   
        TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
        print(f'Забаненый пользователь {message.from_user.username} {message.from_user.first_name} написал {message.text} в', TIME)
        with open("data/logs.txt", "a+") as f:
            f.write(f'\n{TIME} | Забаненый пользователь {message.from_user.username} {message.from_user.first_name} написал {message.text}')

if __name__ == '__main__':
    TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
    print ('Бот запущен:', TIME)
    with open("data/logs.txt", "a+") as f:
            f.write(f'\n{TIME} | Бот запущен')
    while True:
        try:
            bot.infinity_polling(none_stop=True, timeout=123)
        except Exception as e:
            TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
            print(e)
            with open("data/logs.txt", "a+") as f:
                f.write(f'\n{TIME} | e')
            error(bot)
            tm.sleep(15)

# bot.polling(none_stop=True)
