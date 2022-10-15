import telebot, datetime, pytz
from telebot import types, telebot
from parser import parserdef
from myrandom import randomman
from settings import TOKEN, db_table_val, cursor
from buttons import *

tz = pytz.timezone('Asia/Yekaterinburg')
today = datetime.date.today()
tomorrow = datetime.date.today() + datetime.timedelta(days=+1)
yesterday = datetime.date.today() + datetime.timedelta(days=-1)
today_d = today.strftime('%-d')
tomorrow_d = tomorrow.strftime('%-d')
yesterday_d = yesterday.strftime('%-d')
today_m = today.strftime('%-m')
tomorrow_m = tomorrow.strftime('%-m')
yesterday_m = yesterday.strftime('%-m')

nubmeruser = 1

#Действия после команд
def telebot_bot(TOKEN):
    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        admin = [510441193]
        if message.chat.id not in admin:
            if message.text == '/start':
                bot.send_message(message.from_user.id, 'Добро пожаловать')
                db_table_val(message, bot)
                menu(types,bot,message)
            else:
                bot.send_message(message.from_user.id, 'Добро пожаловать, Admin')
                db_table_val(message, bot)
                menu(types,bot,message)


    @bot.message_handler(content_types=["text"])
    def bot_message(message):
        cursor.execute(f'SELECT id FROM users WHERE user_id = {message.chat.id} ')
        data = cursor.fetchone()
        if data is None:
            bot.send_message(message.from_user.id, 'Привет, тебя нету в базе данных, не мог бы ты написать /start ?')
            print(f'Пользователь {message.from_user.username} зарегестрировался!')
        else:
            adm = [1612734022, 712230934, 510441193]
            admin = [510441193]

            if message.content_type == 'text':
                if message.text == '👥Преподы👥':
                    f = open('data/Prepod.txt', 'r', encoding='UTF-8')
                    thinks  = f.read()
                    f.close()
                    bot.send_message(message.chat.id, thinks)
                    print(f'Пользователь {message.from_user.username} запросил препадов')

                elif message.text == '🔙Назад':
                    menu(types,bot,message)
                
                elif message.text == 'Группы':
                    group(types, bot, message)

                elif message.text == '📋Пары📋':
                    group(types, bot, message)

                elif message.text == '2ИС6':
                    day(types, bot, message)

                elif message.text == '2Р5':
                    if message.chat.id not in adm:
                        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                        back=types.KeyboardButton("Группы")
                        markup.add(back)
                        bot.send_message(message.chat.id, 'Прости ты не из той группы!!! Хочешь смотреть расписание группы 2Р5 пиши создателю! @kinoki445',  reply_markup=markup)
                    else:
                        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1=types.KeyboardButton("Вчерашние 2Р5")
                        item2=types.KeyboardButton("На сегодня 2Р5")
                        item3=types.KeyboardButton("На завтра 2Р5")
                        item4=types.KeyboardButton("🔔Расписание звонков")
                        back=types.KeyboardButton("Группы")
                        markup.add(item1, item2, item3, item4, back)
                        bot.send_message(message.chat.id, 'Выбери на какой день ты хочешь узнать пары: ',  reply_markup=markup)

                elif message.text == 'Расписание куратора':
                    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1=types.KeyboardButton("Вчерашние Кур")
                    item2=types.KeyboardButton("На сегодня Кур")
                    item3=types.KeyboardButton("На завтра Кур")
                    item4=types.KeyboardButton("🔔Расписание звонков")
                    back=types.KeyboardButton("Группы")
                    markup.add(item1, item2, item3, item4, back)
                    bot.send_message(message.chat.id, 'Выбери на какой день ты хочешь узнать пары: ',  reply_markup=markup)

                elif message.text == '🔔Расписание звонков':
                    photo = open('data/photo.jpg', 'rb')
                    markup_inline = types.InlineKeyboardMarkup()
                    url1 = types.InlineKeyboardButton (text = '📅Полное расписание📅', url=f'https://a.nttek.ru/group.php?key={yesterday_d}-{yesterday_m}.1.3.54')
                    markup_inline.add(url1)
                    bot.send_photo(message.chat.id, photo, reply_markup=markup_inline)
                    print(f'Пользователь {message.from_user.username} запросил расписание звонков')
                
                elif message.text == 'Вчерашние 2Р5':
                    pari(yesterday_d, yesterday_m, yesterday, 'group', '.2.3.45', types, bot, message)

                elif message.text == 'Вчерашние':
                    pari(yesterday_d, yesterday_m, yesterday, 'group', '.1.3.54', types, bot, message)
                
                elif message.text == 'Вчерашние Кур':
                    pari(yesterday_d, yesterday_m, yesterday, 'teacher', '.16', types, bot, message)

                elif message.text == 'На сегодня 2Р5':
                    pari(today_d, today_m, today, 'group', '.2.3.45', types, bot, message)

                elif message.text == 'На сегодня':
                    pari(today_d, today_m, today, 'group', '.1.3.54', types, bot, message)

                elif message.text == 'На сегодня Кур':
                    pari(today_d, today_m, today, 'teacher', '.16', types, bot, message)

                elif message.text == 'На завтра 2Р5':
                    pari(tomorrow_d, tomorrow_m, tomorrow, 'group', '.2.3.45', types, bot, message)

                elif message.text == 'На завтра Кур':
                    pari(tomorrow_d, tomorrow_m, tomorrow, 'teacher', '.16', types, bot, message)
                
                elif message.text == 'На завтра':
                    pari(tomorrow_d, tomorrow_m, tomorrow, 'group', '.1.3.54', types, bot, message)

                elif message.text == '👬Студенты группы👬':
                    f = open('data/Student.txt', 'r', encoding='UTF-8')
                    facts = f.read()
                    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton("🔁Рандомно выбрать студента🔁")
                    back = types.KeyboardButton("🔙Назад")
                    markup.add(item1, back)
                    print(f'Пользователь {message.from_user.username} запросил студентов')
                    bot.send_message(message.chat.id, facts, reply_markup=markup)
                    f.close()

                elif message.text == '🔁Рандомно выбрать студента🔁':
                    randomman(message.from_user.username)
                    f1 = open('data/random.txt', 'r', encoding='UTF-8')
                    facts = f1.read()
                    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                    bot.send_message(message.chat.id, facts, reply_markup=markup)

                elif message.text == '📒О боте📒':
                    f = open('data/About bot.txt', 'r', encoding='UTF-8')
                    facts = f.read()
                    markup_inline = types.InlineKeyboardMarkup()
                    url1 = types.InlineKeyboardButton (text = 'Вк', url='https://vk.com/mem445')
                    url2 = types.InlineKeyboardButton (text = 'Телеграмм', url= 'https://t.me/Kinoki445')
                    url3 = types.InlineKeyboardButton (text = 'Вк куратора группы', url= 'https://vk.com/id31107453')
                    markup_inline.add(url1,url2, url3)
                    print(f'Пользователь {message.from_user.username} узнал о боте')
                    bot.send_message(message.chat.id, facts, reply_markup=markup_inline)
                    f.close()
                

                else:
                    bot.send_message(message.chat.id, 'Вы написали: ' + message.text)
                    print(f'Пользователь {message.from_user.username} написал {message.text}')
                    

    time = (datetime.datetime.now(tz))
    print ('Бот запущен\n', time.strftime('%d/%-m/%Y %H/%M/%S'))
    bot.polling(none_stop=True, interval=0)   


# Запускаем бота
if __name__ == '__main__':
    telebot_bot(TOKEN)
