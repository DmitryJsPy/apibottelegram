import requests
import wikipedia
from telebot import TeleBot, types

def random_duck():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

def random_fox():
    url = 'https://randomfox.ca/floof/'
    res = requests.get(url)
    data = res.json()
    return data['image']

def random_dog():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']

TOKEN = "7234516211:AAEPcHB0PCJW53--9jNxAb9jOkysPKl1fmk"
bot = TeleBot(TOKEN)
wikipedia.set_lang("ru")

# Главное меню с животными и Wiki
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_duck = types.KeyboardButton('Утка')
    btn_dog = types.KeyboardButton('Собака')
    btn_fox = types.KeyboardButton('Лиса')
    btn_wiki = types.KeyboardButton('Wiki')
    markup.add(btn_duck, btn_dog, btn_fox, btn_wiki)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

# Кнопки управления Wiki (появляется после команды Wiki)
def wiki_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_stop = types.KeyboardButton('Стоп')
    markup.add(btn_stop)
    bot.send_message(message.chat.id, "Введите запрос для Википедии или нажмите 'Стоп'", reply_markup=markup)

# Возвращение к главному меню
@bot.message_handler(func=lambda message: message.text == 'Стоп')
def stop_wiki(message):
    main_menu(message)

# Обработка callback'ов для кнопок Wikipedia
@bot.callback_query_handler(func=lambda call: call.data)
def answer(call):
    page = wikipedia.page(call.data)
    bot.send_message(call.message.chat.id, text=page.title)
    bot.send_message(call.message.chat.id, text=page.summary)
    bot.send_message(call.message.chat.id, text=page.url)

# Нажатие на кнопку Wiki
@bot.message_handler(func=lambda message: message.text == 'Wiki')
def wiki(message):
    bot.send_message(message.chat.id, "Напишите запрос для поиска в Википедии.")
    wiki_menu(message)
    bot.register_next_step_handler(message, handle_wiki_query)

# Обработка текстовых запросов после нажатия на Wiki
def handle_wiki_query(message):
    if message.text.lower() == 'стоп':
        stop_wiki(message)
        return
    
    text = message.text
    results = wikipedia.search(text)
    
    if not results:
        bot.send_message(message.chat.id, "Ничего не найдено.")
        wiki_menu(message)  # Позволяет ввести новый запрос
        bot.register_next_step_handler(message, handle_wiki_query)
        return
    
    markup = types.InlineKeyboardMarkup()
    for res in results:
        markup.add(types.InlineKeyboardButton(res, callback_data=res))
    
    bot.send_message(message.chat.id, text='Смотри что я нашел!', reply_markup=markup)
    wiki_menu(message)  # Позволяет ввести новый запрос
    bot.register_next_step_handler(message, handle_wiki_query)

# Команды для животных
@bot.message_handler(func=lambda message: message.text == 'Утка')
def duck(message):
    url = random_duck()
    bot.send_message(message.chat.id, url)

@bot.message_handler(func=lambda message: message.text == 'Собака')
def dog(message):
    url = random_dog()
    bot.send_message(message.chat.id, url)

@bot.message_handler(func=lambda message: message.text == 'Лиса')
def fox(message):
    url = random_fox()
    bot.send_message(message.chat.id, url)

# Стартовое меню при запуске бота
@bot.message_handler(commands=['start'])
def start(message):
    main_menu(message)

if __name__ == '__main__':
    bot.polling(non_stop=True)
