import requests, json, time
import datetime as dt
from settings import cursor

def getpari(date, group, group_name, InlineKeyboardMarkup, InlineKeyboardButton, bot, callback):
    if group == 'group':
        try:
            site = requests.get(f'https://erp.nttek.ru/api/schedule/legacy').text
            sitedate = json.loads(site)
            f = open('data/last_data.txt', 'r', encoding='UTF-8')
            schedule_number = f.read()
            f.close()
            try:
                if schedule_number.strip('"') != str(sitedate[0:1]):
                    with open('data/last_data.txt', 'w', encoding='UTF-8') as f:
                        f.write(f'{sitedate[0:1]}')
                    cursor.execute(f'SELECT user_id FROM users WHERE schedule = {1}')
                    lol = cursor.fetchall()
                    count = 0
                    while count != len(lol):
                        for row in lol:
                            try:
                                bot.send_message(chat_id = row[0], text = f'Добавили новое расписание!\nЕсли тебе не нравится это уведомление ты всегда можешь выключить его в настройках /menu')
                                count += 1
                            except:
                                count += 1
            except:
                    pass
            
            sitedate.sort(key=lambda x: time.mktime(time.strptime(x,"%d.%m.%Y")))

            if (len(sitedate)) <= 5:
                a = 0
            else:
                a = ((len(sitedate)) - 5)

            date = date.replace('.','-')
            now = dt.datetime.strptime(date, '%d-%m-%Y')
            now = now.strftime('%Y-%m-%d')
            r = requests.get(f'https://erp.nttek.ru/api/schedule/legacy/{now}/{group}/{group_name}').text
            data = json.loads(r)
            try:
                text = ''
                for i in data['schedule']:
                    lesson = i['lesson']
                    name = i['name']
                    room = i['rooms']
                    teacher = i['teachers']
                    text = (text + '\n' + (f'**Номер урока:** {lesson}\n**Урок:** {name} {room}\n**Препод:** {teacher}\n'))
            
                keyboard = InlineKeyboardMarkup()
                keyboard.row_width = 3

                for i in range(a, len(sitedate)):
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
                    keyboard.add (InlineKeyboardButton(f'{sitedate[i]} ({date2})',callback_data = f'{sitedate[i]} {group_name}'))
                    
                item1 = (InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
                item3 = (InlineKeyboardButton('Преподаватели', callback_data = 'teacher'))
                item2 = (InlineKeyboardButton('Твоя группа', callback_data = 'f_group'))
                close = (InlineKeyboardButton('Меню', callback_data = 'close2'))
                keyboard.add(item1, item3, item2)
                keyboard.add(close)

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

                try:
                    bot.answer_callback_query(callback_query_id=callback.id, show_alert=False)
                    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Расписание на {date} ({date2}):\n __{text}__ \nВыберите день на который хотите узнать расписание\nгруппы {group_name}', parse_mode='Markdown', reply_markup = keyboard)
                    date = ('') 
                    date2 = ('')
                    text = ('')
                except:
                    pass

            except Exception as e:
                keyboard = InlineKeyboardMarkup()
                keyboard.row_width = 3

                for i in range(a, len(sitedate)):
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
                    keyboard.add (InlineKeyboardButton(f'{sitedate[i]} ({date2})',callback_data = f'{sitedate[i]} {group_name}'))
                    
                item1 = (InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
                item3 = (InlineKeyboardButton('Преподаватели', callback_data = 'teacher'))
                item2 = (InlineKeyboardButton('Твоя группа', callback_data = 'f_group'))
                close = (InlineKeyboardButton('Меню', callback_data = 'close2'))
                keyboard.add(item1, item3, item2)
                keyboard.add(close)
                try:
                    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Расписания НЕТУ! Либо попробуй нажать ещё раз\nВыберите день на который хотите узнать расписание:', parse_mode='Markdown', reply_markup = keyboard)
                except:
                    pass

        except Exception as e:
            print(e)
            keyboard = InlineKeyboardMarkup()
            keyboard.row_width = 3

            for i in range(a, len(sitedate)):
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
                keyboard.add (InlineKeyboardButton(f'{sitedate[i]} ({date2})',callback_data = f'{sitedate[i]} {group_name}'))
                
            item1 = (InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
            item3 = (InlineKeyboardButton('Преподаватели', callback_data = 'teacher'))
            item2 = (InlineKeyboardButton('Твоя группа', callback_data = 'f_group'))
            close = (InlineKeyboardButton('Меню', callback_data = 'close2'))
            keyboard.add(item1, item3, item2)
            keyboard.add(close)

            try:
                bot.answer_callback_query(callback_query_id=callback.id, show_alert=False)
                bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Такой группы нету выбери другую, либо проблемы на сайте, \nузнай у меня в чём проблема @kinoki445', parse_mode='Markdown', reply_markup = keyboard)
            except: 
                pass
    elif group == 'excel':
        try:
            site = requests.get(f'https://erp.nttek.ru/api/schedule/legacy').text
            sitedate = json.loads(site)
            sitedate.sort(key=lambda x: time.mktime(time.strptime(x,"%d.%m.%Y")))

            if (len(sitedate)) <= 5:
                a = 0
            else:
                a = ((len(sitedate)) - 5)

            date = date.replace('.','-')
            now = dt.datetime.strptime(date, '%d-%m-%Y')
            now = now.strftime('%Y-%m-%d')
            r = requests.get(f'https://erp.nttek.ru/api/schedule/legacy/{now}').text
            data = json.loads(r)
            try:
                url = data['url']
                text = (f'**{url}**')
            
                keyboard = InlineKeyboardMarkup()
                keyboard.row_width = 3

                for i in range(a, len(sitedate)):
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
                    keyboard.add (InlineKeyboardButton(f'{sitedate[i]} ({date2})',callback_data = f'excel {sitedate[i]}'))
                    
                item1 = (InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
                item3 = (InlineKeyboardButton('Преподаватели', callback_data = 'teacher'))
                item2 = (InlineKeyboardButton('Твоя группа', callback_data = 'f_group'))
                close = (InlineKeyboardButton('Меню', callback_data = 'close2'))
                keyboard.add(item1, item3, item2)
                keyboard.add(close)
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

                try:
                    bot.answer_callback_query(callback_query_id=callback.id, show_alert=False)
                    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Расписание на {date} ({date2}):\n __{text}__ \nВыберите день на который хотите узнать расписание', parse_mode='Markdown', reply_markup = keyboard)
                    date = ('') 
                    date2 = ('')
                    text = ('')
                except:
                    pass

            except Exception as e:
                keyboard = InlineKeyboardMarkup()
                keyboard.row_width = 3
                for i in range(a, len(sitedate)):
                    keyboard.add(InlineKeyboardButton(f'{sitedate[i]} {group_name}',callback_data = f'{sitedate[i]} {group_name}'))
                item1 = (InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
                item3 = (InlineKeyboardButton('Преподаватели', callback_data = 'teacher'))
                item2 = (InlineKeyboardButton('Твоя группа', callback_data = 'f_group'))
                close = (InlineKeyboardButton('Меню', callback_data = 'close2'))
                keyboard.add(item1, item3, item2)
                keyboard.add(close)

                try:
                    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Расписания НЕТУ! Либо попробуй нажать ещё раз\nВыберите день на который хотите узнать расписание:', parse_mode='Markdown', reply_markup = keyboard)
                    bot.answer_callback_query(callback_query_id=callback.id, show_alert=False)
                except:
                    pass
        except Exception as e:
            bot.send_message(chat_id = 510441193, text = f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} ввёл неверно группу')
            keyboard = InlineKeyboardMarkup()
            keyboard.row_width = 3
            item1 = (InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
            item3 = (InlineKeyboardButton('Преподаватели', callback_data = 'teacher'))
            item2 = (InlineKeyboardButton('Твоя группа', callback_data = 'f_group'))
            close = (InlineKeyboardButton('Меню', callback_data = 'close2'))
            keyboard.add(item1, item3, item2)
            keyboard.add(close)
            try:
                bot.answer_callback_query(callback_query_id=callback.id, show_alert=False)
                bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Такой группы нету выбери другую, либо узнай у меня в чём проблема @kinoki445', parse_mode='Markdown', reply_markup = keyboard)
            except:
                pass

    else:
        try:
            site = requests.get(f'https://erp.nttek.ru/api/schedule/legacy').text
            sitedate = json.loads(site)
            sitedate.sort(key=lambda x: time.mktime(time.strptime(x,"%d.%m.%Y")))

            if (len(sitedate)) <= 5:
                a = 0
            else:
                a = ((len(sitedate)) - 5)

            date = date.replace('.','-')
            now = dt.datetime.strptime(date, '%d-%m-%Y')
            now = now.strftime('%Y-%m-%d')
            r = requests.get(f'https://erp.nttek.ru/api/schedule/legacy/{now}/{group}/{group_name}').text
            data = json.loads(r)
            try:
                text = ''
                for i in data:
                    Corpus = data[i]['building']['number']
                    Group = data[i]['group']
                    Para = data[i]['name']
                    Room = data[i]['rooms']
                    text = (text + '\n' + (str(f'{Corpus}\nНомер урока: {i}\nГруппа: {Group}\nУрок: {Para}\nКабинет: {Room}\n')))
                keyboard = InlineKeyboardMarkup()
                keyboard.row_width = 3
                for i in range(a, len(sitedate)):
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
                    keyboard.add (InlineKeyboardButton(f'{sitedate[i]} ({date2})',callback_data = f'препод{sitedate[i], group_name}'))
                item1 = (InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
                item3 = (InlineKeyboardButton('Преподаватели', callback_data = 'teacher'))
                item2 = (InlineKeyboardButton('Твоя группа', callback_data = 'f_group'))
                close = (InlineKeyboardButton('Меню', callback_data = 'close2'))
                keyboard.add(item1, item3, item2)
                keyboard.add(close)
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

                try:
                    bot.answer_callback_query(callback_query_id=callback.id, show_alert=False)
                    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Расписание на {date} ({date2}):\n __{text}__ \nВыберите день на который хотите узнать расписание преподавателя {group_name}', parse_mode='Markdown', reply_markup = keyboard)
                    date = ('') 
                    date2 = ('')
                    text = ('')
                except:
                    pass

            except Exception as e:
                keyboard = InlineKeyboardMarkup()
                keyboard.row_width = 3
                for i in range(a, len(sitedate)):
                    keyboard.add(InlineKeyboardButton(f'{sitedate[i]} {group_name}',callback_data = f'препод{sitedate[i], group_name}'))
                item1 = (InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
                item3 = (InlineKeyboardButton('Преподаватели', callback_data = 'teacher'))
                item2 = (InlineKeyboardButton('Твоя группа', callback_data = 'f_group'))
                close = (InlineKeyboardButton('Меню', callback_data = 'close2'))
                keyboard.add(item1, item3, item2)
                keyboard.add(close)
                try:
                    bot.answer_callback_query(callback_query_id=callback.id, show_alert=False)
                    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Расписания НЕТУ! Либо попробуй нажать ещё раз\nВыберите день на который хотите узнать расписание:', parse_mode='Markdown', reply_markup = keyboard)
                except:
                    pass

        except Exception as e:
            bot.send_message(chat_id = 510441193, text = f'Пользователь {callback.message.chat.username} {callback.message.chat.first_name} ввёл неверно группу')
            keyboard = InlineKeyboardMarkup()
            keyboard.row_width = 3
            item1 = (InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
            item3 = (InlineKeyboardButton('Преподаватели', callback_data = 'teacher'))
            item2 = (InlineKeyboardButton('Твоя группа', callback_data = 'f_group'))
            close = (InlineKeyboardButton('Меню', callback_data = 'close2'))
            keyboard.add(item1, item3, item2)
            keyboard.add(close)
            try:
                bot.answer_callback_query(callback_query_id=callback.id, show_alert=False)
                bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Такого препода нету нету выбери другую', parse_mode='Markdown', reply_markup = keyboard)
            except:
                pass