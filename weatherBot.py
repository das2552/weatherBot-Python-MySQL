import telebot
import math
import pymysql
from pyowm.owm import OWM
from pyowm.utils import timestamps
from config import host, user, password, db_name


bot = telebot.TeleBot("YOUR TOKEN BOT", parse_mode=None)
owm = OWM('YOUR TOKEN OWM')
current_city_for_search = 'Yaroslavl'   # можно поменять город / choose ur city
mgr = owm.weather_manager()

#Получаем погоду сейчас
def weather_at_now(city):
    weather = mgr.weather_at_place(city).weather
    temp = weather.temperature('celsius')["temp"]
    status = weather.status
    detailedStatus = weather.detailed_status
    return temp, status, detailedStatus

#Получаем погоду через 3 часа
def weather_at_three_h(city):
    three_h_forecaster = mgr.forecast_at_place(city, '3h')
    next_three_hours = timestamps.next_three_hours()
    weather_at_three = three_h_forecaster.get_weather_at(next_three_hours)
    weather_at_three_status = weather_at_three.status
    weather_at_three_detailed_status = weather_at_three.detailed_status
    temp_at_three = weather_at_three.temperature('celsius')["temp"]
    return temp_at_three, weather_at_three_status, weather_at_three_detailed_status, 

#Генерируем ответ
def generate_answer(weather_at_now, weather_at_three_h):
    answer = "Доброе утро\n\n"

    if (weather_at_now[1] == "Rain"):
        if (weather_at_now[2] == "light rain"):
            answer += "Сейчас возможен легкий дождь! "
        else:
            answer += "Сейчас на улице дождь, бери зонт! "
    elif (weather_at_now[1] == "Clouds"):
        answer += "Сейчас на улице облачно "
    else:
        answer += "Сейчас на улице солнечно "

    answer += str(math.ceil(weather_at_now[0])) + "°"

    if (weather_at_three_h[1] == "Rain"):
        if (weather_at_three_h[2] == "light rain"):
            answer += "\n\nЧерез 3 часа возможен легкий дождь! "
        else:
            answer += "\n\nЧерез 3 часа будет дождь, бери зонт! "
    elif (weather_at_three_h[1] == "Clouds"):
        answer += "\n\nЧерез 3 часа будет облачно "
    else:
        answer += "\n\nЧерез 3 часа будет солнечно "

    answer += str(math.ceil(weather_at_three_h[0])) + "°"
    return answer

# send messages 
def send_messages():
    try:
        connection = pymysql.connect(
        host = host,
        port = 3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                # select chatID

                with connection.cursor() as cursor:
                    select_query = "SELECT chatID FROM Users"
                    cursor.execute(select_query)
                    data = cursor.fetchall()
                    for row in data:
                        bot.send_message(row['chatID'], generate_answer(weather_at_now(current_city_for_search), weather_at_three_h(current_city_for_search)))
        finally:
            connection.close()
    except Exception as ex:
        print("...")
        print(ex)

if __name__ == "__main__":
    send_messages()
