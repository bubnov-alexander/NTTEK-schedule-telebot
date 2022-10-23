import sqlite3, datetime

TOKEN = ('5641742733:AAFjF171LR2NxdLKtu-6zSGrnx63U-W137U')
PAYMENTS_TOKEN = ('3975332bf0807fb44f7fa347c2414a16')
PHONE = '+79030785665'

# 5656787289:AAE8wT3rHr92ic0FkqGCIAcHDbYQtwZ5G5s
# 5641742733:AAFjF171LR2NxdLKtu-6zSGrnx63U-W137U


database = sqlite3.connect('db/database.db', check_same_thread=False)
cursor = database.cursor()
print("Подключен к SQLite3")

cursor.execute ("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    user_id INTEGER UNIQUE NOT NULL,
    user_name TEXT NOT NULL,
    username STRING,
    join_date DATETIME NOT NULL
    )""")
database.commit()

cursor.execute ("""CREATE TABLE IF NOT EXISTS admin(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    user_id INTEGER UNIQUE NOT NULL,
    user_name TEXT NOT NULL,
    username STRING,
    join_date DATETIME NOT NULL
    )""")
database.commit()

cursor.execute ("""CREATE TABLE IF NOT EXISTS tworfive(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    user_id INTEGER UNIQUE NOT NULL,
    user_name TEXT NOT NULL,
    username STRING,
    join_date DATETIME NOT NULL
    )""")
database.commit()

cursor.execute ("""CREATE TABLE IF NOT EXISTS homeworker(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    user_id INTEGER UNIQUE NOT NULL,
    user_name TEXT NOT NULL,
    username STRING,
    join_date DATETIME NOT NULL
    )""")
database.commit()

cursor.execute ("""CREATE TABLE IF NOT EXISTS ban(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    user_id INTEGER UNIQUE NOT NULL,
    user_name TEXT NOT NULL,
    username STRING,
    join_date DATETIME NOT NULL
    )""")
database.commit()


def db_table_val(message, bot):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    username = message.from_user.username
    people_id = message.chat.id
    today = datetime.date.today()
    joindate = today.strftime('%d.%m.%Y')
    cursor.execute(f'SELECT id FROM users WHERE user_id = {people_id} ')
    data = cursor.fetchone()
    if data is None:
        cursor.execute('INSERT INTO users (user_id, user_name, username, join_date) VALUES (?, ?, ?, ?)', (us_id, us_name, username, joindate))
        database.commit()
        bot.send_message(message.chat.id, 'Я тебя зарегистрировл!', parse_mode='html')
        bot.send_message(chat_id = 510441193, text = f'Зарегестрировался новый пользователь! {username}, {us_name}', parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, 'Ты уже зарегестрирован и можешь пользоваться функциями бота!', parse_mode='html')
