from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from parser2 import *


def openfile(file, bot, callback, who):
    f = open(f'data/{file}', 'r', encoding='UTF-8')
    facts = f.read()
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 2
    for i in range(0, len(pari1)):
        keyboard.add (InlineKeyboardButton(f'{pari1[i]} {who}',callback_data = f'{pari1[i]} {who}'))
    bot.send_message(callback.message.chat.id, f'{facts}Выберите день на который хотите узнать расписание', reply_markup = keyboard)
    f.close