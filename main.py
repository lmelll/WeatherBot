import telebot
from weather_parser import Weather
from telebot import types
#import logging

bot = telebot.TeleBot('1653986362:AAF9EhDJtV7Ucjq1gUrLWY0w-6h204p_NAk')
country = ""
#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

@bot.message_handler(commands=['vk'])
def open_vk(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Посетить мою страницу", url="https://vk.com/mellsenpai"))
    bot.send_message(message.chat.id, "Отлично, просто нажми на кнопку", parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['insta'])
def open_insta(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Посетить мою страницу", url="https://www.instagram.com/mell_senpai_"))
    bot.send_message(message.chat.id, "Отлично, просто нажми на кнопку", parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn = types.KeyboardButton('Погода')
    markup.add(btn)
    send_mess = f"<b>Привет {message.from_user.first_name} {message.from_user.last_name}</b>\n Что тебя интересует?"
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def mess(message):
    if not isinstance(message, str):
        get_message_bot = message.text.strip().lower()
    else:
        get_message_bot = message

    if get_message_bot == "погода":
        final_message ="Введите интересующую вас страну на английском.\n Пример: Russia"
        msg = bot.send_message(message.chat.id, final_message, parse_mode='html')
        bot.register_next_step_handler(msg, get_country)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn = types.KeyboardButton('Погода')
        markup.add(btn)
        final_message = "Ошибка, нажмите на кнопку"
        bot.send_message(message.chat.id, final_message, parse_mode='html', reply_markup=markup)

def get_country(message):
    global country
    country = message.text.strip().lower()
    if country:
        final_message = "Введите интересующий вас город на английском.\n Пример: Moscow"
        msg = bot.send_message(message.chat.id, final_message, parse_mode='html')
        bot.register_next_step_handler(msg, get_town)
    else:
        final_message = "Пустой ввод."
        msg = bot.send_message(message.chat.id, final_message, parse_mode='html')
        bot.register_next_step_handler(msg, get_country)

def get_town(message):
    town = message.text.strip().lower()
    weather = Weather(country, town)
    try:
        bot.send_message(message.chat.id, "Температура: " + weather.get_temp() +  "\n" + "Осадки: " + weather.get_desc() + "\n" + \
                     "Ощущается: " + weather.get_feels() + "\n" + "Давление: " + weather.get_pressure() + "\n" + \
                     "Ветер: " + weather.get_wind() + "\n" + "Влажность: " + weather.get_humidity())
    except:
        bot.send_message(message.chat.id, "Ошибка, возможно вы ошиблись при вводе, попробуйте ещё раз!")
        message.text = "погода"
        mess(message)


bot.polling(none_stop=True)