import json
import time

import telebot
from telebot import types
from telebot import util
import requests
from googletrans import Translator
from pyowm import OWM
from pyowm.utils.config import get_default_config

import config as cfg

bot_text = {
    'enter_city': 'Кроме <i>г.Киева, Одессы, Львов и тд</i>, Вы можете ввести абсолютно любой город.\nВведите название города: ',
    'greeting': '\nЯ - <b>Kroft-Bot</b> 🤖\nС помощью меня ты можешь узнать:\n☀️ Погоду\n💰 Курсы валют\n📜 Перевод слов и текста\n💡 интересные факты о числах\n\n⚙ Отправь команду <b> /help </b>, чтоб зайти в дополнительное меню команд.'
}

bot = telebot.TeleBot(cfg.date['BOT_TOKEN'])
response = requests.get(cfg.date['PRIVAT_24_API_KEY']).json()


# main menu
@bot.message_handler(commands=['start'])
def start(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🌤️ Погода')
    btn2 = types.KeyboardButton('💰 Курс валют')
    btn3 = types.KeyboardButton('🟢 Далее')
    kb.add(btn1, btn2, btn3)
    user_name = str(message.from_user.first_name)
    bot.send_message(message.chat.id, f'Привет <b>{user_name}!</b>\n' + bot_text['greeting'], parse_mode='html')
    time.sleep(1)
    pic_1 = open(r'pic_1.jpg', 'rb')
    bot.send_photo(message.chat.id,pic_1, '<i>Если вдруг пропадут кнопки меню, нажми на эту</i> <b>кнопку</b>', parse_mode='html', reply_markup=kb)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\nNew user\nuser_name -->  @{str(message.from_user.username)}\nuser_id -->  {str(message.from_user.id)}\nuser_first_name -->  {str(message.from_user.first_name)}\nuser_last_name -->  {str(message.from_user.last_name)}\n\n' + f'{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)

@bot.message_handler(commands=['help'])
def start(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🌤️ Погода')
    btn2 = types.KeyboardButton('💰 Курс валют')
    btn3 = types.KeyboardButton('🟢 Далее')
    kb.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id, '<b>/help</b> - команда настроек ⚙\n<b>/start</b> - команда запуска бота 🕹️\n/readlog - команда чтения архива 👁️', parse_mode='html')
    time.sleep(1)
    pic_1 = open(r'pic_1.jpg', 'rb')
    bot.send_photo(message.chat.id,pic_1, '<i>Если вдруг пропадут кнопки меню, нажми на эту</i> <b>кнопку</b>', parse_mode='html', reply_markup=kb)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)

@bot.message_handler(commands=['readlog'])
def start(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🌤️ Погода')
    btn2 = types.KeyboardButton('💰 Курс валют')
    btn3 = types.KeyboardButton('🟢 Далее')
    kb.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id, 'Тут ты можешь прочесть <b>всю историю</b> использования <b>бота</b> 👁️', parse_mode='html', reply_markup=kb)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
        for msg in util.split_string(txt, 1000):
            bot.send_message(message.chat.id, msg)
        





# OWM
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == '🌤️ Погода')
def bot_message_owm_1(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton('Одесса')
    btn2 = types.KeyboardButton('Киев')
    btn3 = types.KeyboardButton('Львов')
    btn4 = types.KeyboardButton('Москва')
    btn5 = types.KeyboardButton('Санкт-Петербург')
    btn6 = types.KeyboardButton('Минск')
    btn7 = types.KeyboardButton('Нью-Йорк')
    btn8 = types.KeyboardButton('Берлин')
    btn9 = types.KeyboardButton('Рим')
    main = types.KeyboardButton('⤵️В главное меню')
    kb.add(btn1, btn2, btn3,btn4, btn5, btn6,btn7, btn8, btn9)
    kb.add(main)
    sent = bot.reply_to(message, bot_text['enter_city'], parse_mode='html', reply_markup=kb)
    bot.register_next_step_handler(sent, owm)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)

# OWM
def owm(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('☂️  Погода в другом городе')
        main = types.KeyboardButton('⤵️В главное меню')
        kb.add(btn1)
        kb.add(main)
        message_to_save = message.text
        config_dict = get_default_config()  # ru
        config_dict['language'] = 'ru'  # ru
        owm = OWM(cfg.date['OWM_API_KEY'])
        place = message.text
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(place)
        w = observation.weather
        t = w.temperature('celsius')
        t1 = t['temp']
        t2 = t['feels_like']
        t3 = t['temp_max']
        t4 = t['temp_min']
        # Ветер
        wind = w.wind()['speed']
        # Влажность
        humidity = w.humidity
        # Облачность
        cloudy = w.clouds
        # Статус
        st = w.status
        # Детали
        dt = w.detailed_status
        # Время(данные о погоде)
        tm = w.reference_time('iso')
        # Давление
        pr = w.pressure['press']
        # Видиммость
        vd = w.visibility_distance
        weather_forecast = f'Ваш запрос по городу <b>{place}</b>:\n\n<b>1.</b> <i>Температра</i>: {int(t1)}°C \
        \n<b>2.</b> <i>Ощущается как</i>: {int(t2)}°C\n<b>3.</b> <i>Максимальная</i>: {int(t3)}°C \
        \n<b>4.</b> <i>Минимальная</i>: {int(t4)}°C\n<b>5.</b> <i>Скорость ветра</i>: {int(wind)} м/с\n<b>6.</b> <i>Влажность</i>: {humidity} % \
        \n<b>7.</b> <i>Облачность</i>: {cloudy} %\n<b>8.</b> <i>Статус</i>: {st}\n<b>9.</b> <i>Детальный статус</i>: {dt} \
        \n<b>10.</b> <i>Справочное время</i>: {tm}\n<b>11.</b> <i>Давление</i>: {pr} мм.рт.ст\n<b>12.</b> <i>Видимость</i>: {vd} м.'
        bot.send_message(message.chat.id, weather_forecast, parse_mode='html', reply_markup=kb)

        with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + ' ' + str(weather_forecast))
        time.sleep(0.7)

    except:
        bot.send_message(message.chat.id, '<b>Такой город не найден!</b>', parse_mode='html', reply_markup=kb)

        with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + ' - не найден.')
        time.sleep(0.7)

# OWM
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == '☂️  Погода в другом городе')
def bot_message_owm_2(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton('Одесса')
    btn2 = types.KeyboardButton('Киев')
    btn3 = types.KeyboardButton('Львов')
    btn4 = types.KeyboardButton('Москва')
    btn5 = types.KeyboardButton('Санкт-Петербург')
    btn6 = types.KeyboardButton('Минск')
    btn7 = types.KeyboardButton('Нью-Йорк')
    btn8 = types.KeyboardButton('Берлин')
    btn9 = types.KeyboardButton('Рим')
    main = types.KeyboardButton('⤵️В главное меню')
    kb.add(btn1, btn2, btn3,btn4, btn5, btn6,btn7, btn8, btn9)
    kb.add(main)
    sent = bot.reply_to(message, bot_text['enter_city'], parse_mode='html', reply_markup=kb)
    bot.register_next_step_handler(sent, owm)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)




# currency
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == '💰 Курс валют')
def bot_message_cur_1(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('EUR')
    btn2 = types.KeyboardButton('USD')
    main = types.KeyboardButton('⤵️В главное меню')
    kb.add(btn1, btn2)
    kb.add(main)
    msg = bot.send_message(message.chat.id, 'Узнать наличный курс <b>ПриватБанка</b>\n(в отделениях): ', parse_mode='html', reply_markup=kb)
    bot.register_next_step_handler(msg, currency)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)

# currency
def currency(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('💶 Посмотреть другую валюту')
        main = types.KeyboardButton('⤵️В главное меню')
        kb.add(btn1)
        kb.add(main)

        for coin in response:
            if (message.text == coin['ccy']):
                print_coin_text = print_coin(coin['buy'], coin['sale'])
                bot.send_message(message.chat.id, print_coin_text, parse_mode='html', reply_markup=kb)

                with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
                    f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + f' {print_coin_text}')
                time.sleep(0.7)

    except Exception:
        bot.reply_to(message, 'ooops!')

# currency
def print_coin(buy, sale):
    """Вывод курса пользователю."""
    return '<b>💵 Курс покупки:</b>' + str(buy) + '\n<b>💵 Курс продажи:</b>' + str(sale)

# currency
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == '💶 Посмотреть другую валюту')
def bot_message_cur_2(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('EUR')
    btn2 = types.KeyboardButton('USD')
    main = types.KeyboardButton('⤵️В главное меню')
    kb.add(btn1, btn2)
    kb.add(main)
    msg = bot.send_message(message.chat.id, 'Узнать наличный курс <b>ПриватБанка</b>\n(в отделениях): ', parse_mode='html', reply_markup=kb)
    bot.register_next_step_handler(msg, currency)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)




# menu p.2
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == '🟢 Далее')
def bot_message_p_2(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🗣️ Переводчик')
    btn2 = types.KeyboardButton('💡 Факты о числах')
    main = types.KeyboardButton('⤵️В главное меню')
    kb.add(btn1, btn2)
    kb.add(main)
    bot.send_message(message.chat.id, '🟢 Далее', parse_mode='html', reply_markup=kb)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)




# translator
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == '🗣️ Переводчик')
def bot_message_trans_1(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🇷🇺 (ru-en) 🇺🇸')
    btn2 = types.KeyboardButton('🇺🇸 (en-ru) 🇷🇺')
    btn3 = types.KeyboardButton('🇷🇺 (ru-uk) 🇺🇦')
    btn4 = types.KeyboardButton('🇺🇦 (uk-ru) 🇷🇺')
    main = types.KeyboardButton('⤵️В главное меню')
    kb.add(btn1, btn2, btn3, btn4)
    kb.add(main)
    bot.send_message(message.chat.id, 'Выберите с какого языка хотите сделать перевод и на какой язык: ', parse_mode='html', reply_markup=kb)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)

# translator ru-en
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == '🇷🇺 (ru-en) 🇺🇸')
def bot_message_ru_en(message):
    kb = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, 'Введите <b>слово</b>, либо <b>словосочетание</b>, на который хотите получить <b>перевод:</b> ', parse_mode='html', reply_markup=kb)
    bot.register_next_step_handler(msg, ru_en)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)

def ru_en(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🔃 Повторный перевод')
        main = types.KeyboardButton('⤵️В главное меню')
        kb.add(btn1)
        kb.add(main)
        message_to_save = message.text
        translator = Translator()
        translation = translator.translate(text=message.text, src='ru', dest='en')
        bot.send_message(message.chat.id, '<b>Ваш перевод:</b>\n💎 ' + translation.text + ' 💎', parse_mode='html', reply_markup=kb)

        with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + ' -->' + str(translation.text))
        time.sleep(0.7)

    except:
        bot.send_message(message.chat.id, '<b>Такое слово не найдено!</b>', parse_mode='html', reply_markup=kb)

        with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + ' - не найден.')
        time.sleep(0.7)

# translator en_ru
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == '🇺🇸 (en-ru) 🇷🇺')
def bot_message_en_ru(message):
    kb = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, 'Введите <b>слово</b>, либо <b>словосочетание</b>, на который хотите получить <b>перевод:</b> ', parse_mode='html', reply_markup=kb)
    bot.register_next_step_handler(msg, en_ru)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)

def en_ru(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🔃 Повторный перевод')
        main = types.KeyboardButton('⤵️В главное меню')
        kb.add(btn1)
        kb.add(main)
        message_to_save = message.text
        translator = Translator()
        translation = translator.translate(text=message.text, src='en', dest='ru')
        bot.send_message(message.chat.id, '<b>Ваш перевод:</b>\n💎 ' + translation.text + ' 💎', parse_mode='html', reply_markup=kb)

        with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + ' -->' + str(translation.text))
        time.sleep(0.7)

    except:
        bot.send_message(message.chat.id, '<b>Такое слово не найдено!</b>', parse_mode='html', reply_markup=kb)

        with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + ' - не найден.')
        time.sleep(0.7)

# translator ru_uk
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == '🇷🇺 (ru-uk) 🇺🇦')
def bot_message_en_ru(message):
    kb = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, 'Введите <b>слово</b>, либо <b>словосочетание</b>, на который хотите получить <b>перевод:</b> ', parse_mode='html', reply_markup=kb)
    bot.register_next_step_handler(msg, ru_uk)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)

def ru_uk(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🔃 Повторный перевод')
        main = types.KeyboardButton('⤵️В главное меню')
        kb.add(btn1)
        kb.add(main)
        message_to_save = message.text
        translator = Translator()
        translation = translator.translate(text=message.text, src='ru', dest='uk')
        bot.send_message(message.chat.id, '<b>Ваш перевод:</b>\n💎 ' + translation.text + ' 💎', parse_mode='html', reply_markup=kb)

        with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + ' -->' + str(translation.text))
        time.sleep(0.7)

    except:
        bot.send_message(message.chat.id, '<b>Такое слово не найдено!</b>', parse_mode='html', reply_markup=kb)

        with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + ' - не найден.')
        time.sleep(0.7)

# translator uk_ru
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == '🇺🇦 (uk-ru) 🇷🇺')
def bot_message_en_ru(message):
    kb = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, 'Введите <b>слово</b>, либо <b>словосочетание</b>, на который хотите получить <b>перевод:</b> ', parse_mode='html', reply_markup=kb)
    bot.register_next_step_handler(msg, uk_ru)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)

def uk_ru(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🔃 Повторный перевод')
        main = types.KeyboardButton('⤵️В главное меню')
        kb.add(btn1)
        kb.add(main)
        message_to_save = message.text
        translator = Translator()
        translation = translator.translate(text=message.text, src='uk', dest='ru')
        bot.send_message(message.chat.id, '<b>Ваш перевод:</b>\n💎 ' + translation.text + ' 💎', parse_mode='html', reply_markup=kb)

        with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + ' -->' + str(translation.text))
        time.sleep(0.7)

    except:
        bot.send_message(message.chat.id, '<b>Такое слово не найдено!</b>', parse_mode='html', reply_markup=kb)

        with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + ' - не найден.')
        time.sleep(0.7)

# translator repeat
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == '🔃 Повторный перевод')
def bot_message_repeat(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🇷🇺 (ru-en) 🇺🇸')
    btn2 = types.KeyboardButton('🇺🇸 (en-ru) 🇷🇺')
    btn3 = types.KeyboardButton('🇷🇺 (ru-uk) 🇺🇦')
    btn4 = types.KeyboardButton('🇺🇦 (uk-ru) 🇷🇺')
    main = types.KeyboardButton('⤵️В главное меню')
    kb.add(btn1, btn2, btn3, btn4)
    kb.add(main)
    bot.send_message(message.chat.id, '<b>Рад, что был полезен тебе!</b>\n<i>Какой на этот раз сделать перевод ?</i>', parse_mode='html', reply_markup=kb)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)




# numbers
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == '💡 Факты о числах')
def bot_message_num(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Мелочи')
    btn2 = types.KeyboardButton('Год')
    btn3 = types.KeyboardButton('Дата')
    btn4 = types.KeyboardButton('Математика')
    btn5 = types.KeyboardButton('🟣 Факт о числе (0 - 100)')
    main = types.KeyboardButton('⤵️В главное меню')
    kb.add(btn1, btn2, btn3, btn4, btn5)
    kb.add(main)
    bot.send_message(message.chat.id, 'Выберите <b>группу фактов :</b>', parse_mode='html', reply_markup=kb)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)

# numbers
def text_translator_numbers(text='Text', src='en', dest='ru'):
    try:
        translator = Translator()
        translation = translator.translate(text=text, src=src, dest=dest)
        return translation.text

    except Exception as ex:
        return ex

# numbers
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == 'Мелочи')
def bot_message_num_0(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('🧠 Больше интересных фактов о числах')
    main = types.KeyboardButton('⤵️В главное меню')
    kb.add(btn1)
    kb.add(main)
    number_answer = requests.get(f'http://numbersapi.com/random/trivia?json')
    bot_text_answer_eng = json.loads(number_answer.text)['text']
    bot_text_answer_ru = text_translator_numbers(text=bot_text_answer_eng, src='en', dest='ru')
    bot.send_message(message.chat.id, '<b>Answer on english language:</b>\n' + f'<i>{bot_text_answer_eng}</i>' + '\n\n<b>Ответ на русском языке:</b>\n' + f'<i>{bot_text_answer_ru}</i>',parse_mode='html', reply_markup=kb)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + ' ' + str(bot_text_answer_eng) + ' ' + str(bot_text_answer_ru))
    time.sleep(0.7)

# numbers
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == 'Год')
def bot_message_num_1(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('🧠 Больше интересных фактов о числах')
    main = types.KeyboardButton('⤵️В главное меню')
    kb.add(btn1)
    kb.add(main)
    number_answer = requests.get(f'http://numbersapi.com/random/year?json')
    bot_text_answer_eng = json.loads(number_answer.text)['text']
    bot_text_answer_ru = text_translator_numbers(text=bot_text_answer_eng, src='en', dest='ru')
    bot.send_message(message.chat.id, '<b>Answer on english language:</b>\n' + f'<i>{bot_text_answer_eng}</i>' + '\n\n<b>Ответ на русском языке:</b>\n' + f'<i>{bot_text_answer_ru}</i>',parse_mode='html', reply_markup=kb)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + ' ' + str(bot_text_answer_eng) + ' ' + str(bot_text_answer_ru))
    time.sleep(0.7)

# numbers
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == 'Дата')
def bot_message_num_2(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('🧠 Больше интересных фактов о числах')
    main = types.KeyboardButton('⤵️В главное меню')
    kb.add(btn1)
    kb.add(main)
    number_answer = requests.get(f'http://numbersapi.com/random/date?json')
    bot_text_answer_eng = json.loads(number_answer.text)['text']
    bot_text_answer_ru = text_translator_numbers(text=bot_text_answer_eng, src='en', dest='ru')
    bot.send_message(message.chat.id, '<b>Answer on english language:</b>\n' + f'<i>{bot_text_answer_eng}</i>' + '\n\n<b>Ответ на русском языке:</b>\n' + f'<i>{bot_text_answer_ru}</i>',parse_mode='html', reply_markup=kb)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + ' ' + str(bot_text_answer_eng) + ' ' + str(bot_text_answer_ru))
    time.sleep(0.7)

# numbers
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == 'Математика')
def bot_message_num_3(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('🧠 Больше интересных фактов о числах')
    main = types.KeyboardButton('⤵️В главное меню')
    kb.add(btn1)
    kb.add(main)
    number_answer = requests.get(f'http://numbersapi.com/random/math?json')
    bot_text_answer_eng = json.loads(number_answer.text)['text']
    bot_text_answer_ru = text_translator_numbers(text=bot_text_answer_eng, src='en', dest='ru')
    bot.send_message(message.chat.id, '<b>Answer on english language:</b>\n' + f'<i>{bot_text_answer_eng}</i>' + '\n\n<b>Ответ на русском языке:</b>\n' + f'<i>{bot_text_answer_ru}</i>',parse_mode='html', reply_markup=kb)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + ' ' + str(bot_text_answer_eng) + ' ' + str(bot_text_answer_ru))
    time.sleep(0.7)

# numbers
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == '🟣 Факт о числе (0 - 100)')
def bot_message_num_4(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    main = types.KeyboardButton('⤵️В главное меню')
    kb.add(main)
    msg = bot.send_message(message.chat.id, 'Введите <b>любое число</b>, чтоб узнать интересный факт о нем.', parse_mode='html', reply_markup=kb)
    bot.register_next_step_handler(msg, any_number)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)

# numbers
def any_number(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('🧠 Больше интересных фактов о числах')
        main = types.KeyboardButton('⤵️В главное меню')
        kb.add(btn1)
        kb.add(main)
        number_answer = requests.get(f'http://numbersapi.com/{message.text}?json')
        bot_text_answer_eng = json.loads(number_answer.text)['text']
        bot_text_answer_ru = text_translator_numbers(text=bot_text_answer_eng, src='en', dest='ru')
        bot.send_message(message.chat.id,'<b>Answer on english language:</b>\n' + f'<i>{bot_text_answer_eng}</i>' + '\n\n<b>Ответ на русском языке:</b>\n' + f'<i>{bot_text_answer_ru}</i>', parse_mode='html', reply_markup=kb)

        with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + ' ' + str(bot_text_answer_eng) + ' ' + str(bot_text_answer_ru))
        time.sleep(0.7)

    except:
        bot.send_message(message.chat.id, '<b>Такого числа нет в базе чисел с интересными фактами!</b>', parse_mode='html', reply_markup=kb)

        with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text) + '- такого числа нет в базе чисел с интересными фактами!')
        time.sleep(0.7)

# numbers
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == '🧠 Больше интересных фактов о числах')
def bot_message_num_repeat(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Мелочи')
    btn2 = types.KeyboardButton('Год')
    btn3 = types.KeyboardButton('Дата')
    btn4 = types.KeyboardButton('Математика')
    btn5 = types.KeyboardButton('🟣 Факт о числе (0 - 100)')
    main = types.KeyboardButton('⤵️В главное меню')
    kb.add(btn1, btn2, btn3, btn4, btn5)
    kb.add(main)
    bot.send_message(message.chat.id, '<b>Рад, что был полезен тебе!</b>\n<i>Какую на этот раз группу вы хотите узнать ?</i>', parse_mode='html', reply_markup=kb)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)




# back to main menu
@bot.message_handler(chat_types= ['private'], func=lambda x: x.text == '⤵️В главное меню')
def bot_message_back_menu(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('🌤️ Погода')
    btn2 = types.KeyboardButton('💰 Курс валют')
    btn3 = types.KeyboardButton('🟢 Далее')
    kb.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, '⤵️Гавное меню', parse_mode='html', reply_markup=kb)

    with open(f'multibot_users_data_txt/multibot_user_and_id____{str(message.from_user.username)}____{str(message.from_user.id)}.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{time.strftime("%d-%m-%Y %H:%M:%S ", time.localtime())}@{str(message.from_user.username)}({str(message.from_user.id)}) |   ' + str(message.text))
    time.sleep(0.7)



if __name__ == '__main__':
    print('Bot has been started')
    bot.polling(none_stop=True)
