import openai, datetime, pytz, time as tm
from Key import TOKEN_OPENAI

tz = pytz.timezone('Asia/Yekaterinburg')

# Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = (TOKEN_OPENAI)


def send_openai(prompt, bot, argument1):
    TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
    DATE = (datetime.datetime.now(tz)).strftime('%d.%m')
    with open("data/logs.txt", "a+") as f:
        f.write(f'\n{TIME} {DATE}| Пользователь {argument1.from_user.username} {argument1.from_user.first_name} запросил у OpenAI: {prompt}')
    print(f'{TIME} {DATE}| Пользователь {argument1.from_user.username} {argument1.from_user.first_name} запросил у OpenAI: {prompt}')
    bot.send_message(argument1.chat.id, text = "Подожди, обрабатываю запрос!")
    # задаем модель и промпт
    model_engine = "text-davinci-003"

    # задаем макс кол-во слов
    max_tokens = 128

    # генерируем ответ
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # выводим ответ
    bot.send_message(argument1.chat.id, text = f'{completion.choices[0].text}')