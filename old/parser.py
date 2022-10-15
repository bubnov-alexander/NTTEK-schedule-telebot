import requests
from bs4 import BeautifulSoup as b
import datetime as dt, shutil


f = open('data/Par.txt', 'w+', encoding='UTF-8')
url = (f'https://a.nttek.ru/index.php')
r = requests.get(url)
soup = b(r.text, 'html.parser')
pari = soup.find(id="schedule-date").get_text()
pari = (pari[17:-21:])
pari = pari.rsplit()
pari1 = []
f.write((" ".join(pari)))
f.close()

for idx, x in enumerate(pari):
    if idx %2 == 1:
        pari1.append(x)

par = len(pari1)

def parserdef2(who, group):

    a = (0)
    number1 = (0)
    number2 = (1)
    number3 = (2)

    
        #Получаем сами расписания
    while a != par:
        if who == 'teacher':
            pari12 = pari1[number1:number2:]
            pari12 = ((" ".join(pari12)))
            dt_obj = (dt.datetime.strptime((pari12[:-2]),'%d.%m.%Y'))
            month = dt_obj.strftime('%-m')
            day = dt_obj.strftime('%-d')
            urlteacher = (f'https://a.nttek.ru/teachers.php?date={day}-{month}')
            r1 = requests.get(urlteacher)
            soup = b(r1.text, 'html.parser')
            pari = soup.find_all('li')
            clear_url = [t.text for t in pari]
            number = 0
            prepod = '\nЗятикова ТЮ\n'

            for i in range(len(clear_url)):
                if prepod == clear_url[number]:
                    break
                elif prepod != clear_url[number]:
                    number += 1
            file = open(f'data/par/{pari12}.txt', 'w', encoding='UTF-8')
            url = (f'https://a.nttek.ru/teacher.php?key={day}-{month}.{number}')
            r = requests.get(url)
            soup = b(r.text, 'html.parser')
            pari = soup.find('table')

            try:
                clear_pari = [t.text for t in pari]
                file.write (f'На {pari12}')
                file.write (" ".join(clear_pari))
            except:
                file.write ('Расписания на такую дату ещё не выложили, либо у вас выходной! Проверьте сайт с расписанием! ⬇️⬇️⬇️⬇️')
                file.close ()
            number1 += 1
            number2 += 1
            number3 += 1
            a += 1
        else:
            while a != par:
                pari12 = pari1[number1:number2:]
                pari12 = ((" ".join(pari12)))
                dt_obj = (dt.datetime.strptime((pari12[:-2]),'%d.%m.%Y'))
                month = dt_obj.strftime('%-m')
                day = dt_obj.strftime('%-d')
                file = open(f'data/par/{pari12}.txt', 'w', encoding='UTF-8')
                url = (f'https://a.nttek.ru/group.php?key={day}-{month}{group}')
                r = requests.get(url)
                soup = b(r.text, 'html.parser')
                pari = soup.find('table')
                try:
                    clear_pari = [t.text for t in pari]
                    file.write (f'На {pari12}')
                    file.write (" ".join(clear_pari))
                except:
                    file.write ('Расписания на такую дату ещё не выложили, либо у вас выходной! Проверьте сайт с расписанием! ⬇️⬇️⬇️⬇️')
                    file.close ()
                number1 += 1
                number2 += 1
                number3 += 1
                a += 1

