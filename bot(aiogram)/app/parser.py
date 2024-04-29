import requests
import json
import time
import datetime as dt
from app import database as db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def getpari(date, group, group_name, bot, callback, type):
    site = requests.get(f'https://erp.nttek.ru/api/schedule/legacy').text
    sitedate = json.loads(site)
    keyboard = InlineKeyboardMarkup(row_width=3)

    f = open('data/last_data.txt', 'r', encoding='UTF-8')
    schedule_number = f.read()
    f.close()

    if schedule_number.strip('"') != str(sitedate[0:1]):
        await db.send_newshuld(bot, sitedate)
    else:
        pass

    sitedate.sort(key=lambda x: time.mktime(time.strptime(x, "%d.%m.%Y")))

    if (len(sitedate)) <= 5:
        a = 0
    else:
        a = ((len(sitedate)) - 5)

    for i in range(a, len(sitedate)):
        date1 = int(dt.datetime.weekday(dt.datetime.strptime(
            sitedate[i].replace('.', '-'), '%d-%m-%Y')))
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
        keyboard.add(InlineKeyboardButton(f'{sitedate[i]} ({date2})', callback_data=(
            type + ',' + sitedate[i] + ',' + group_name)))

    date = date.replace('.', '-')
    now = dt.datetime.strptime(date, '%d-%m-%Y')
    now = now.strftime('%Y-%m-%d')

    date1 = int(dt.datetime.weekday(dt.datetime.strptime(date, '%d-%m-%Y')))
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
        try:
            r = requests.get(
                f'https://erp.nttek.ru/api/schedule/legacy/{now}/{group}/{group_name}').text
            data = json.loads(r)
            try:
                text = ''
                for i in data['schedule']:
                    lesson = i['lesson']

                    if lesson == '1' or lesson =='1-2':
                        lesson = (i['lesson'] + ' 8:30 - 9:50')
                    elif lesson == '3':
                        lesson = (i['lesson'] + ' 10:00 - 10:40')
                    elif lesson == '4':
                        lesson = (i['lesson'] + ' 10:40 - 11:20')
                    elif lesson == '5':
                        lesson = (i['lesson'] + ' 11:20 - 12:00')
                    elif lesson == '6-7':
                        lesson = (i['lesson'] + ' 12:10 - 13:30')
                    elif lesson == '8-9':
                        lesson = (i['lesson'] + ' 13:40 - 15:00')
                    elif lesson == '10-11':
                        lesson = (i['lesson'] + ' 15:15 - 16:35')
                    elif lesson == '12-13':
                        lesson = (i['lesson'] + ' 16:40 - 18:00')
                    else:
                        lesson = i['lesson']
                    name = i['name']
                    room = i['rooms']
                    teacher = i['teachers']
                    text = (
                        text + '\n' + (f'**Номер урока:** {lesson}\n**Урок:** {name} {room}\n**Препод:** {teacher}\n'))

                keyboard.add(InlineKeyboardButton('Другие группы', callback_data='another_group'),
                            InlineKeyboardButton(
                                'Преподаватели', callback_data='teacher'),
                            InlineKeyboardButton('Твоя группа', callback_data='f_group'))
                keyboard.add(InlineKeyboardButton(
                    'Меню', callback_data='📋Расписание📋'))
                try:
                    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=f'Расписание на {date} ({date2}):\n __{text}__ \nВыберите день на который хотите узнать расписание\nгруппы {group_name}', parse_mode='Markdown', reply_markup=keyboard)
                except:
                    await bot.edit_message_text(chat_id=callback.chat.id, message_id=callback.message_id, text=f'Расписание на {date} ({date2}):\n __{text}__ \nВыберите день на который хотите узнать расписание\nгруппы {group_name}', parse_mode='Markdown', reply_markup=keyboard)
                date = ('')
                date2 = ('')
                text = ('')

            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

    elif group == 'excel':
        try:
            r = requests.get(
                f'https://erp.nttek.ru/api/schedule/legacy/{now}').text
            data = json.loads(r)
            try:
                url = data['url']
                text = (f'**{url}**')

                keyboard.add(InlineKeyboardButton('Другие группы', callback_data='another_group'),
                            InlineKeyboardButton(
                                'Преподаватели', callback_data='teacher'),
                            InlineKeyboardButton('Твоя группа', callback_data='f_group'))
                keyboard.add(InlineKeyboardButton(
                    'Меню', callback_data='📋Расписание📋'))
                try:
                    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=f'Расписание на {date} ({date2}):\n __{text}__ \nВыберите день на который хотите узнать расписание\nгруппы {group_name}', parse_mode='Markdown', reply_markup=keyboard)
                except:
                    await bot.edit_message_text(chat_id=callback.chat.id, message_id=callback.message_id, text=f'Расписание на {date} ({date2}):\n __{text}__ \nВыберите день на который хотите узнать расписание\nгруппы {group_name}', parse_mode='Markdown', reply_markup=keyboard)

                date = ('')
                date2 = ('')
                text = ('')

            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

    elif group == 'teacher':
        try:
            r = requests.get(
                f'https://erp.nttek.ru/api/schedule/legacy/{now}/{group}/{group_name}').text
            data = json.loads(r)
            try:
                text = ''
                for i in data:
                    Corpus = data[i]['building']['number']
                    Group = data[i]['group']
                    Para = data[i]['name']
                    Room = data[i]['rooms']
                    text = (
                        text + '\n' + (str(f'{Corpus}\nНомер урока: {i}\nГруппа: {Group}\nУрок: {Para}\nКабинет: {Room}\n')))

                keyboard.add(InlineKeyboardButton('Другие группы', callback_data='another_group'),
                            InlineKeyboardButton(
                                'Преподаватели', callback_data='teacher'),
                            InlineKeyboardButton('Твоя группа', callback_data='f_group'))
                keyboard.add(InlineKeyboardButton(
                    'Меню', callback_data='📋Расписание📋'))
                try:
                    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=f'Расписание на {date} ({date2}):\n __{text}__ \nВыберите день на который хотите узнать расписание\nгруппы {group_name}', parse_mode='Markdown', reply_markup=keyboard)
                except:
                    await bot.edit_message_text(chat_id=callback.chat.id, message_id=callback.message_id, text=f'Расписание на {date} ({date2}):\n __{text}__ \nВыберите день на который хотите узнать расписание\nгруппы {group_name}', parse_mode='Markdown', reply_markup=keyboard)
                date = ('')
                date2 = ('')
                text = ('')

            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
