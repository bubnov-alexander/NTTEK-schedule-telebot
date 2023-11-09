import openai, datetime, pytz, time as tm, os
from app import keyboards as kb

tz = pytz.timezone('Asia/Yekaterinburg')

# Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = os.getenv('OPENAI')


async def send_openai(prompt, bot, callback):
    TIME = (datetime.datetime.now(tz)).strftime('%H:%M:%S')
    DATE = (datetime.datetime.now(tz)).strftime('%d.%m')
    with open("data/logs.txt", "a+", encoding="utf-8") as f:
        f.write(f'\n{TIME} {DATE}| Пользователь {callback.from_user.username} {callback.from_user.first_name} запросил у OpenAI: {prompt}')
    print(f'{TIME} {DATE}| Пользователь {callback.from_user.username} {callback.from_user.first_name} запросил у OpenAI: {prompt}')
    await bot.send_message(callback.chat.id,  text = "Подожди, обрабатываю запрос!")

    # генерируем ответ
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # выводим ответ
    try:
        await bot.edit_message_text(chat_id=callback.chat.id, message_id=callback.message_id, text = f'{completion.choices[0].text}',  reply_markup=kb.close)
    except:
        await bot.send_message(callback.chat.id, text = f'{completion.choices[0].text}',  reply_markup=kb.close)