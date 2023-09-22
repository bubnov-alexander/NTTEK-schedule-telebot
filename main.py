import telebot, datetime, pytz, time as tm
from telebot import telebot
from settings import *
from buttons import *
from Key import TOKEN

tz = pytz.timezone('Asia/Yekaterinburg')
bot = telebot.TeleBot(TOKEN)

#Действия после start
@bot.message_handler(commands=['start'])
def start_message(message):
    admin = 510441193
    if message.chat.id != admin:
        bot.send_message(message.from_user.id, f'Добро пожаловать, {message.from_user.first_name}', parse_mode='html')
        db_table_val(message, bot)
        menu(bot, message)
    else:
        bot.send_message(message.from_user.id, f'Добро пожаловать, Admin {message.from_user.first_name}', parse_mode='html')
        db_table_val(message, bot)
        menu(bot, message)

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.from_user.id, 'Привет, чтобы пользоваться функциями бота тебе достаточно написать /menu, если что-то не получается пиши мне | @Kinoki445', parse_mode='html')
    TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
    DATE = (datetime.datetime.now(tz)).strftime('%d.%m')
    print(f'Пользователь {message.from_user.username} {message.from_user.first_name} написал {message.text} в ', TIME)
    with open("data/logs.txt", "a+", encoding='UTF-8') as f:
        f.write(f'\n{TIME} {DATE}| Пользователь {message.from_user.username} {message.from_user.first_name} написал {message.text}')

@bot.message_handler(commands=['clear'])
def message_menu(message):
    delete = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, f'Я удалил кнопки!', parse_mode='html', reply_markup=delete)

@bot.message_handler(commands=['menu'])
def message_menu(message):
    menu(bot, message)

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
    ban = 5322880119
    if message.chat.id != 5322880119:
        if data is None:
            bot.send_message(message.from_user.id, 'Привет, тебя нету в базе данных, не мог бы ты написать /start ?', parse_mode='html')
        else:
            if message.content_type.lower() == 'text':
                if message_to_bot == 'меню' or message_to_bot == 'menu':
                    menu(bot, message)
                    bot.delete_message(message.chat.id, message.message_id)

                else:
                    delete = telebot.types.ReplyKeyboardRemove()
                    bot.send_message(message.chat.id, f'Вы написали: {message.text}\nЕсли хотите узнать что может бот напишите /menu\nБудут вопросы пишите: @Kinoki445', parse_mode='html', reply_markup=delete)
                    TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
                    DATE = (datetime.datetime.now(tz)).strftime('%d.%m')
                    print(f'{TIME} {DATE} | Пользователь {message.from_user.username} {message.from_user.first_name} написал {message.text}')
                    bot.delete_message(message.chat.id, message.message_id)
                    try:
                        with open("data/logs.txt", "a+", encoding='UTF-8') as f:
                            f.write(f'\n{TIME} {DATE}| Пользователь {message.from_user.username} {message.from_user.first_name} написал {message.text}')
                    except:
                        pass

    #Действия если user в бане
    else:
        bot.send_message(message.chat.id, 'Ты в БАНЕ чучело!!! \n Пиши @Kinoki445', parse_mode='html')   
        TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
        DATE = (datetime.datetime.now(tz)).strftime('%d.%m')
        print(f'{TIME} {DATE} | Забаненый пользователь {message.from_user.username} {message.from_user.first_name} написал {message.text}')
        with open("data/logs.txt", "a+", encoding='UTF-8') as f:
            f.write(f'\n{TIME} {DATE} | Забаненый пользователь {message.from_user.username} {message.from_user.first_name} написал {message.text}')

if __name__ == '__main__':
    TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
    DATE = (datetime.datetime.now(tz)).strftime('%d.%m')
    print ('Бот запущен:', TIME)
    with open("data/logs.txt", "a+", encoding='UTF-8') as f:
        f.write(f'\n{TIME} {DATE}| Бот запущен')
    while True:
        try:
            bot.infinity_polling(none_stop=True, timeout=123)
        except Exception as e:
            TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
            DATE = (datetime.datetime.now(tz)).strftime('%d.%m')
            print(e)
            with open("data/logs.txt", "a+", encoding='UTF-8') as f:
                f.write(f'\n{TIME} {DATE}| {e}')
            tm.sleep(15)
            continue