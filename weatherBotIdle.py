import telebot
from telebot import types
import pymysql
from config import host, user, password, db_name

bot = telebot.TeleBot("YOUR TOKEN BOT", parse_mode=None)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Хочу получать уведомления', callback_data="save_me"))
    markup.add(telebot.types.InlineKeyboardButton(text='Задать вопрос', callback_data="question"))
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот для рассылки погоды Ярославля".format(message.from_user), reply_markup=markup)
    name = message.from_user.first_name
@bot.callback_query_handler(func=lambda call: True)
def save_me(call):
    if call.data == 'save_me':
        chatID = str(call.message.chat.id)
        try:
            connection = pymysql.connect(
            host = host,
            port = 3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
            )
            print("sucefull connect to DB")

            try:
                with connection.cursor() as cursor:
                    # insert data

                    with connection.cursor() as cursor:
                        insert_query = "INSERT INTO Users (name, chatID) VALUES ('" + name + "', '" + chatID + "');"
                        cursor.execute(insert_query)

                        connection.commit()
                        bot.send_message(call.message.chat.id, "Я тебя запомнил, в 7:30 буду присылать сообщения!")
            finally:
                connection.close()
        except Exception as ex:
            print("...")
            print(ex)
            bot.send_message(call.message.chat.id, "Произошла ошибка, возможно вы уже подключены на рассылку!")

    elif call.data == 'question':
        bot.send_message(call.message.chat.id, "Все вопросы к моему папочке: https://t.me/das322")

@bot.message_handler(content_types=['text'])
def error(message):
    bot.send_message(message.chat.id, "Я тебя не понял, для того чтобы начать использовать меня напиши /start")

bot.polling( none_stop= True)