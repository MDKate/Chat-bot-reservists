import telebot
import telegram
from telebot import types
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import pandas as pd
import numpy as np
import emoji
import telebot
from time import sleep
from multiprocessing.context import Process
from datetime import timedelta
import schedule
from pathlib import Path
from telegram import ParseMode
import datetime
from datetime import datetime

from emoji import emojize


# Подключаемся к боту
bot = telebot.TeleBot('5958215181:AAFSaPDPJr9JFxtT3UWkO_WWFxTQMEQ2DE8')




# --------------------------------------------Отправка видео по дате------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# Создаем обработчик, который отправляет видео в заданное время
def job():
    # Подгружаем базу
    base = pd.read_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
    del (base['Unnamed: 0'])
    # Работа по отправке видео. Если текущая дата совпадает с датой из таблицы, то
    if datetime.today().strftime('%Y-%m-%d %H:%M') == base['Дата'][0]:
        # Перебираем всех НЕ преподавателей и отправляем им видео
        for i in range(1, len(base)):
            if base['Участники курса'][i] != 'Преподаватель':
                bot.send_message(int(base['ID'][i]), f'Посмотрите видео и пройдите тест. \n {base["Видео"][0]}', parse_mode=ParseMode.HTML)
    # Работа по отправке теста. Определяем время отправки теста, с учетом длительности видео
    mint = datetime.strptime(str(base['Дата'][0]), '%Y-%m-%d %H:%M')+ timedelta(minutes=int(base['Продолжительность (мин)'][0]))
    # Если текущие дата, время совпадает с расчетной отправкой теста, то
    if datetime.today().strftime('%Y-%m-%d %H:%M') == mint.strftime('%Y-%m-%d %H:%M'):
        # Перебираем всех НЕ преподавателей и высылаем кнопку на прохождение теста
        for i in range(1, len(base)):
            if base['Участники курса'][i] != 'Преподаватель':
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='Пройти тест', callback_data='testr'))
                bot.send_message(int(base['ID'][i]), text=f"Для начала тестирования нажмите на кнопку: ", reply_markup=markup)
    base=""

# Контроллер, который выполняет работу каждую минуту
schedule.every(1).minutes.do(job)

# Выделение потока под контроллер
class ScheduleMessage():
    def try_send_schedule():
        while True:
            schedule.run_pending()
            sleep(1)
    def start_process():
        p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
        p1.start()

# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------



# Обработка действий при старте бота
@bot.message_handler(commands=['start'])
def start_message(message):
    # Считываем таблицу
    base = pd.read_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
    del (base['Unnamed: 0'])
    # Если пользователь уже регистрировался, то
    if message.chat.id in base['ID'].unique():
        bot.send_message(message.chat.id,
                         "Вы уже зарегистрированы! Для перерегистрации нажмите /reregistration")
    # Если пользователь регистрируется первый раз, то
    else:
        bot.send_message(message.chat.id, emoji.emojize(
            "Добрый день!:hand_with_fingers_splayed: Давайте начнем учиться! Для этого вы должны зарегистрироваться."))
        bot.send_message(message.chat.id,
                         emoji.emojize("Введите ваши фамилию, имя и отчество: :magnifying_glass_tilted_left:"))
    base = ""

# Обработка входящего текста
@bot.message_handler(func=lambda message: ['test'])
def next_message(message):
    # Считываем таблицу
    base = pd.read_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
    del (base['Unnamed: 0'])
    # Если пользователь зарегистрировался и внес иформацию о своей группе, то
    if message.chat.id in base['ID'].unique() and len(str(list(base[base['ID'] == message.chat.id]['Группа'])))-4 > 3:
        bot.send_message(message.chat.id, emoji.emojize(
                "Увы! :weary_face: Извините! Я еще плохо умею общаться 	:woman_facepalming:"))
    # Если пользователь еще не зарегистрирован, то
    else:
        sleep(1)
        # Проверяем, зарегистрировал ли человек имя и, если да, то определяем, где его строчка в таблице
        base = pd.read_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
        del (base['Unnamed: 0'])
        for i in range(0, len(base)):
            if len(str(base['ID'][i])) > 3:
                if str(message.chat.id) == str(int(base['ID'][i])):
                    idM = i
                    # Если пользователь ввел имя и группу, то
                    if len(str(base['Группа'][idM])) == 3 and len(str(base['Участники курса'][idM])) > 3:
                        # Дозаписываем данные и сохраняем таблицу
                        group = message.text
                        base['Группа'][idM] = group
                        # base.loc[:, ('Группа',idM) ] = group

                        base.to_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
                        bot.send_message(message.chat.id, 'Отлично! Давайте приступим к работе!')
                        bot.send_message(message.chat.id,
                                         'Для начала, необходимо ознакомиться с некоторыми правилами. \n У вас есть несколько учебных блоков, '
                                         'к каждому из которых есть обязательное задание. Блок состоит из обучающего видео, проверочного теста и домашнего задания. \n '
                                         'Выполняйте все задания в срок! \n Иногда вам будут приходить напоминания, что пора приступить к работе и сообщения от преподавателя. Если вы захотите '
                                         'перезагрузить домашнюю работу - воспользуйтесть тегом /jobreload. Если вы захотите оставить рефлексию - воспользуйтесь тегом /reflection. \n'
                                         'Желаю успешной учебы!')
                # else: idM=0
            else: idM=0
        # Если пользователь ввел имя, но не ввел группу, то
        if idM==0:
            # Дозаписываем данные и сохраняем таблицу
            name = message.text
            base = base.append({"Участники курса": name, "ID": message.chat.id}, ignore_index=True)
            # base = appendDictToDF(base, {"Участники курса": name, "ID": message.chat.id})
            base.to_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
            # Создаем кнопки
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Преподаватель', callback_data='but1'))
            markup.add(telebot.types.InlineKeyboardButton(text='Ученик', callback_data='but2'))
            bot.send_message(message.chat.id, text=f"Выберите вашу роль: ", reply_markup=markup)

    base = ""

# Обработка кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global question
    req = call.data.split('_')
    # Считываем таблицу
    base = pd.read_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
    del (base['Unnamed: 0'])
    # Если выбранная группа - ученик, то
    if req[0] == 'but2':
        bot.send_message(call.message.chat.id, 'Введите вашу группу:')
    # Если нажата кнопка прохождения теста
    elif req[0] == 'testr':
        # Ищем человека в базе и, в его строку, вносим пометку о просмотре видео
        for i in range(1, len(base)):
            if call.message.chat.id == base['ID'][i]:
                base['Отметка о просмотре'][i] = 'Пройдено'
                base.to_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
                iDM=i
        # Если человек пытается повторно пройти тест, то
        if base['Итого баллов?'][iDM] >= 0:
            bot.send_message(call.message.chat.id,
                             text='Внимание! Без разрешения преподавателя проходить тест повторно запрещено!')
        # Если человек первый раз проходит тест, то  выводим первый вопорос
        else:
            question = base['Тест 1'][0]
            buttons = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(text='1', callback_data='t1v1')
            button2 = telebot.types.InlineKeyboardButton(text='2', callback_data='t1v2')
            buttons.row(button1, button2)
            button3 = telebot.types.InlineKeyboardButton(text='3', callback_data='t1v3')
            button4 = telebot.types.InlineKeyboardButton(text='4', callback_data='t1v4')
            buttons.row(button3, button4)
            bot.send_message(call.message.chat.id, text=str(question), reply_markup=buttons)
    # Если это ответ на первый вопрос, то
    elif 't1' in req[0]:
        # Задаем начальное число баллов, раное нулю
        for i in range(1, len(base)):
            if call.message.chat.id == base['ID'][i]:
                iDM=i
                base['Итого баллов?'][iDM] = 0
        # Получаем ответ на вопрос
        if req[0] == 't1v1': answer = "1"
        if req[0] == 't1v2': answer = "2"
        if req[0] == 't1v3': answer = "3"
        if req[0] == 't1v4': answer = "4"
        # Если ответ верен, то присваиваем балл
        if str(base['Ответ 1'][0]) == answer: base['Итого баллов?'][iDM] += 1
        base.to_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
        # Создаем кнопки для второго вопроса
        question = base['Тест 2'][0]
        buttons = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text='1', callback_data='t2v1')
        button2 = telebot.types.InlineKeyboardButton(text='2', callback_data='t2v2')
        buttons.row(button1, button2)
        button3 = telebot.types.InlineKeyboardButton(text='3', callback_data='t2v3')
        button4 = telebot.types.InlineKeyboardButton(text='4', callback_data='t2v4')
        buttons.row(button3, button4)
        bot.send_message(call.message.chat.id, text=str(question), reply_markup=buttons)
    # Если это ответ на второй вопрос, то
    elif 't2' in req[0]:
        for i in range(1, len(base)):
            if call.message.chat.id == base['ID'][i]:
                iDM=i
        # Получаем ответ на вопрос
        if req[0]=='t2v1': answer="1"
        if req[0]=='t2v2': answer="2"
        if req[0]=='t2v3': answer="3"
        if req[0]=='t2v4': answer="4"
        # Если ответ правильный, то присваиваем балл
        if str(base['Ответ 2'][0]) == answer: base['Итого баллов?'][iDM] +=1
        base.to_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
        # Создаем третий вопрос
        question = base['Тест 3'][0]
        buttons = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text='1', callback_data='t3v1')
        button2 = telebot.types.InlineKeyboardButton(text='2', callback_data='t3v2')
        buttons.row(button1, button2)
        button3 = telebot.types.InlineKeyboardButton(text='3', callback_data='t3v3')
        button4 = telebot.types.InlineKeyboardButton(text='4', callback_data='t3v4')
        buttons.row(button3, button4)
        bot.send_message(call.message.chat.id, text=str(question), reply_markup=buttons)
    # Если это ответ на третий вопрос, то
    elif 't3' in req[0]:
        for i in range(1, len(base)):
            if call.message.chat.id == base['ID'][i]:
                iDM=i
        # Получаем ответ на вопрос
        if req[0]=='t3v1': answer="1"
        if req[0]=='t3v2': answer="2"
        if req[0]=='t3v3': answer="3"
        if req[0]=='t3v4': answer="4"
        # Если ответ правильный, то присваиваем балл
        if str(base['Ответ 3'][0]) == answer: base['Итого баллов?'][iDM] +=1
        base.to_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
        base = pd.read_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
        del (base['Unnamed: 0'])
        # Если тест пройден, то
        if int(float(base["Итого баллов?"][iDM])*100/3) > 50:
            base['Отметка о прохождении теста'][iDM] = "Пройдено"
            base.to_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
            bot.send_message(call.message.chat.id, f'Вы сдали тест на :{int(float(base["Итого баллов?"][iDM])*100/3)}%. \n Теперь вы можете приступить к выполнению домашнего задания.')
        # Если тест не пройден, то
        else:
            bot.send_message(call.message.chat.id,
                             f'Вы не прошли тест. Обратитесь к преподавателю.')


    # Если выбранная группа - преподаватель, то
    else:
        base['Группа'][base.index[-1]] = 'Преподаватель'
        base.to_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
        bot.send_message(call.message.chat.id, 'Отлично! Давайте приступим к работе!')
        bot.send_message(call.message.chat.id, 'По мере прохождения учебного блока, я буду писать вам о том, кто из учеников уже ознакомился с видео, кто и на какой балл прошел тест,'
                                               'пересылать домашнее задание учеников. В любое время вы можете написать мне, и я передам сообщение всем ученикам персонально. '
                                               'Для этого воспользуйтесь тегом /message Укажате номер группы, которой нужно отправить сообщение, и текст сообщения. \n '
                                               'Желаю плодотворной работы!')
    base = ""

















if __name__ == '__main__':
    ScheduleMessage.start_process()
    process = Process(target=next_message)
    process.start()
    process.join()
    bot.polling(none_stop=True)