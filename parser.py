import requests, json, time
import datetime as dt


def getpari(date, group, group_name, InlineKeyboardMarkup, InlineKeyboardButton, bot, callback):
    if group != 'teacher':
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
                for i in data['schedule']:
                    lesson = i['lesson']
                    name = i['name']
                    room = i['rooms']
                    teacher = i['teachers']
                    text = (text + '\n' + (f'**Номер пары:** {lesson}\n**Пара:** {name} {room}\n**Препод:** {teacher}\n'))
            
                keyboard = InlineKeyboardMarkup()
                keyboard.row_width = 2
                for i in range(a, len(sitedate)):
                    keyboard.add (InlineKeyboardButton(f'{sitedate[i]} {group_name}',callback_data = f'{sitedate[i]} {group_name}'))
                keyboard.add(InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
                bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Расписание на {date}:\n __{text}__ \nВыберите день на который хотите узнать расписание', parse_mode='Markdown', reply_markup = keyboard)
            except:
                keyboard = InlineKeyboardMarkup()
                keyboard.row_width = 2
                for i in range(a, len(sitedate)):
                    keyboard.add (InlineKeyboardButton(f'{sitedate[i]} {group_name}',callback_data = f'{sitedate[i]} {group_name}'))
                keyboard.add(InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
                bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Расписания НЕТУ!\nВыберите день на который хотите узнать расписание', parse_mode='Markdown', reply_markup = keyboard)
        except:
            keyboard = InlineKeyboardMarkup()
            keyboard.row_width = 2
            keyboard.add(InlineKeyboardButton('Другие группы', callback_data = 'another_group'))
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Такой группы нету выбери другую', parse_mode='Markdown', reply_markup = keyboard)
    else:
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
                Corpus = i['number']
                Group = i['name']
                Para = i['rooms']
                Room = i['teachers']
                text = (text + '\n' + (str(f'Корпус: {Corpus}\nГруппа: {Group}\nПара{Para}\nКабинет: {Room}\n')))
        
            keyboard = InlineKeyboardMarkup()
            keyboard.row_width = 2
            for i in range(a, len(sitedate)):
                keyboard.add (InlineKeyboardButton(f'{sitedate[i]} {group_name}',callback_data = f'{sitedate[i]} {group_name}'))
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Расписание:\n {text} \nВыберите день на который хотите узнать расписание', reply_markup = keyboard)
        except:
            keyboard = InlineKeyboardMarkup()
            keyboard.row_width = 2
            for i in range(a, len(sitedate)):
                keyboard.add (InlineKeyboardButton(f'{sitedate[i]} {group_name}',callback_data = f'{sitedate[i]} {group_name}'))
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text = f'Расписания НЕТУ!\nВыберите день на который хотите узнать расписание', reply_markup = keyboard)