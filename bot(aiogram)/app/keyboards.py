from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import json
import time
import datetime as dt
import os

# ============== Main keyboard ==============

main = InlineKeyboardMarkup(row_width=3)
main.add(InlineKeyboardButton(text = "📋Расписание📋", callback_data = "📋Расписание📋"),
        InlineKeyboardButton(text = "👥Преподаватели👥", callback_data = "👥Преподаватели👥"),
        InlineKeyboardButton(text = "🛠Настройки🛠", callback_data = "🛠Настройки🛠",),
        InlineKeyboardButton(text = "📒О боте📒", callback_data = "📒О боте📒"))

# ============== Main_admin keyboard ==============

main_admin = InlineKeyboardMarkup(row_width=3)
main_admin.add(InlineKeyboardButton(text = "📋Расписание📋", callback_data = "📋Расписание📋"),
        InlineKeyboardButton(text = "👥Преподаватели👥", callback_data = "👥Преподаватели👥"),
        InlineKeyboardButton(text = "🛠Настройки🛠", callback_data = "🛠Настройки🛠",),
        InlineKeyboardButton(text = "OpenAi", callback_data = "openai"),
        InlineKeyboardButton(text = "📒О боте📒", callback_data = "📒О боте📒"),
        InlineKeyboardButton(text = "Admin panel", callback_data = "Admin panel"))

# ============== Schedule keyboard ==============

schedule = InlineKeyboardMarkup()
schedule.add(InlineKeyboardButton(text = "Моя группа", callback_data = 'f_group'),
        InlineKeyboardButton(text = "Excel", callback_data = "excel"),
        InlineKeyboardButton(text = "Сайт с расписанием", url = 'https://a.nttek.ru/'),
        InlineKeyboardButton(text = "🔔Звонки", callback_data = 'bells'),
        InlineKeyboardButton(text = "Преподаватель", callback_data = 'teacher'),
        InlineKeyboardButton(text = "Другая группа", callback_data = 'another_group'),
        InlineKeyboardButton(text = '🔙Назад', callback_data = 'close'))

# ============== Settings keyboard ==============

settings = InlineKeyboardMarkup(1)
settings.add(InlineKeyboardButton (text = '🔔Сообщения от @Kinoki445', callback_data = 'notifications'),
        InlineKeyboardButton (text = '🔔Уведомление о новом расписании', callback_data = 'schedule_notif'),
        InlineKeyboardButton (text = '👯Добавить мою группу', callback_data = 'add_f_group'),
        InlineKeyboardButton (text = '🔙Назад', callback_data = 'close'))

# ============== About keyboard ==============

about_bot = InlineKeyboardMarkup()
about_bot.add(InlineKeyboardButton (text = '🙍🏻‍♂️Портфолио', url='https://kinoki.vercel.app/'),
        InlineKeyboardButton (text = '💌Отзыв', callback_data= 'review'),
        InlineKeyboardButton (text = '💸Поддержка автора', url='https://www.donationalerts.com/r/kinoki445', callback_data = 'print'),
        InlineKeyboardButton(text = '🔙Назад', callback_data = 'close'))

# ============== Admin keyboard ==============

admin_panel = InlineKeyboardMarkup()
admin_panel.add(InlineKeyboardButton(text = 'Пользователи', callback_data = 'users'),
            InlineKeyboardButton(text = 'Логи', callback_data = 'logs'),
            InlineKeyboardButton(text = 'Отправить сообщение', callback_data = 'send_message'),
            InlineKeyboardButton(text = 'Отправить about', callback_data = 'send_all_about'),
            InlineKeyboardButton(text = '🔙Назад', callback_data = 'close'))

# ============== Bell photo ==============

bell = InlineKeyboardMarkup()
bell.add(InlineKeyboardButton(text = '📅Полное расписание📅', url=f'https://a.nttek.ru'),
            InlineKeyboardButton(text = '🔙Назад', callback_data = '📋Расписание📋'))

# ============== Notifications Y/N ==============

notifications = InlineKeyboardMarkup()
notifications.add(InlineKeyboardButton (text = '🔔Вкл сообщения', callback_data = 'n_YES'),
                InlineKeyboardButton (text = '🔕Выкл сообщения', callback_data = 'n_NO'),
                InlineKeyboardButton (text = '🔙Назад', callback_data = '🛠Настройки🛠'))

# ============== Schedule_notif Y/N ==============

schedule_notif = InlineKeyboardMarkup()
schedule_notif.add(InlineKeyboardButton (text = '🔔Вкл уведомления', callback_data = 'n_not_YES'),
            InlineKeyboardButton (text = '🔕Выкл уведомления', callback_data = 'n_not_NO'),
            InlineKeyboardButton (text = '🔙Назад', callback_data = '🛠Настройки🛠'))

# ============== Close button ==============

close = InlineKeyboardMarkup()
close.add(InlineKeyboardButton(text = '🔙Назад', callback_data = 'close'))

close2 = InlineKeyboardMarkup()
close2.add(InlineKeyboardButton(text = '🔙Назад', callback_data = 'close_callback'))

# ============== Raspisanie button ==============

async def parimiy(bot, callback, group, who):
    a = 0
    keyboard = InlineKeyboardMarkup(row_width = 3)
    site = requests.get(f'https://erp.nttek.ru/api/schedule/legacy').text
    sitedate = json.loads(site)
    sitedate.sort(key=lambda x: time.mktime(time.strptime(x,"%d.%m.%Y")))

    if (len(sitedate)) <= 5:
        count = 0
    else:
        count = ((len(sitedate)) - 5)

    for i in range(count, len(sitedate)):
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

        if group == 'group':
            keyboard.add (InlineKeyboardButton(f'{sitedate[i]} ({date2})', callback_data = ('расп,' + sitedate[i]+ ','+ who)))
        elif group == 'excel':
            keyboard.add (InlineKeyboardButton(f'{sitedate[i]} ({date2})', callback_data = ('расе,' + sitedate[i])))
        elif group == 'teacher':
            keyboard.add (InlineKeyboardButton(f'{sitedate[i]} ({date2})', callback_data = ('раст,' + sitedate[i]+ ','+ who)))

    keyboard.add(InlineKeyboardButton('Другие группы', callback_data = 'another_group'),
                InlineKeyboardButton('Преподаватели', callback_data = 'teacher'),
                InlineKeyboardButton('Твоя группа', callback_data = 'f_group'))
    keyboard.add(InlineKeyboardButton('🔙Назад', callback_data = '📋Расписание📋'))

    try:
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text = f'Выберите день на который хотите узнать расписание {who}', reply_markup = keyboard)
    except:
        await bot.delete_message(callback.chat.id, callback.message_id)
        await bot.send_message(callback.chat.id, text = f'Выберите день на который хотите узнать расписание {who}', reply_markup = keyboard)
        