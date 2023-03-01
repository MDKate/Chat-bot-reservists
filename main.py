import telebot
import telegram
from telebot import types
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import pandas as pd
import numpy as np
import emoji

from pathlib import Path
from telegram import ParseMode
import datetime

from emoji import emojize

# Подключаемся к боту
bot = telebot.TeleBot('5958215181:AAFSaPDPJr9JFxtT3UWkO_WWFxTQMEQ2DE8')


# page = 1
# count = 10
#
#
# Определяем отклик
# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call):
#     req = call.data.split('_')





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


# Обработка входящего текста
@bot.message_handler(func=lambda message: ['test'])
def start_message(message):
    # Считываем таблицу
    base = pd.read_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
    del (base['Unnamed: 0'])
    # Если пользователь зарегистрировался и внес иформацию о своей группе, то
    if message.chat.id in base['ID'].unique() and len(str(list(base[base['ID'] == message.chat.id]['Группа'])))-4 > 3:
        bot.send_message(message.chat.id, emoji.emojize(
                "Увы! :weary_face: Извините! Я еще плохо умею общаться 	:woman_facepalming:"))
    # Если пользователь еще не зарегистрирован, то
    else:
        # Если пользователь ввел имя и группу, то
        if len(str(base['Группа'][base.index[-1]])) == 3 and len(str(base['Участники курса'][base.index[-1]])) > 3:
            # Дозаписываем данные и сохраняем таблицу
            group = message.text
            base['Группа'][base.index[-1]] = group
            base.to_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
            bot.send_message(message.chat.id, 'Отлично! Давайте приступим к работе!' )
            bot.send_message(message.chat.id, 'Для начала, необходимо ознакомиться с некоторыми правилами. \n У вас есть несколько учебных блоков, '
                                              'к каждому из которых есть обязательное задание. Блок состоит из обучающего видео, проверочного теста и домашнего задания. \n '
                                              'Выполняйте все задания в срок! \n Иногда вам будут приходить напоминания, что пора приступить к работе и сообщения от преподавателя. Если вы захотите '
                                              'перезагрузить домашнюю работу - воспользуйтесть тегом /jobreload. Если вы захотите оставить рефлексию - воспользуйтесь тегом /reflection. \n'
                                              'Желаю успешной учебы!')
        # Если пользователь ввел имя, но не ввел группу, то
        else:
            # Дозаписываем данные и сохраняем таблицу
            name = message.text
            base = base.append({"Участники курса": name, "ID": message.chat.id}, ignore_index=True)
            base.to_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
            # Создаем кнопки
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='Преподаватель', callback_data='but1'))
            markup.add(telebot.types.InlineKeyboardButton(text='Ученик', callback_data='but2'))
            bot.send_message(message.chat.id, text=f"Выберите вашу роль: " , reply_markup=markup)


# Обработка кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    req = call.data.split('_')
    # Если выбранная группа - ученик, то
    if req[0] == 'but2':
        bot.send_message(call.message.chat.id, 'Введите вашу группу:')
    # Если выбранная группа - преподаватель, то
    else:
        # Считываем таблицу
        base = pd.read_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
        base['Группа'][base.index[-1]] = 'Преподаватель'
        del (base['Unnamed: 0'])
        base.to_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
        bot.send_message(call.message.chat.id, 'Отлично! Давайте приступим к работе!')
        bot.send_message(call.message.chat.id, 'По мере прохождения учебного блока, я буду писать вам о том, кто из учеников уже ознакомился с видео, кто и на какой балл прошел тест,'
                                               'пересылать домашнее задание учеников. В любое время вы можете написать мне, и я передам сообщение всем ученикам персонально. '
                                               'Для этого воспользуйтесь тегом /message Укажате номер группы, которой нужно отправить сообщение, и текст сообщения. \n '
                                               'Желаю плодотворной работы!')




        # @bot.message_handler(content_types=['text'])
            # def message_input_step(message):


    # @bot.message_handler(content_types=['text'])
    # def return_text(message):
    #     name = message.text
    #     bot.send_message(message.chat.id, 'Выберите вашу роль:')




# buttons = types.InlineKeyboardMarkup(row_width=2)
#     button1 = types.InlineKeyboardButton('Преподаватель', callback_data='but1')
#     button2 = types.InlineKeyboardButton('Ученик', callback_data='but2')
#     buttons.add(button1, button2)
#     bot.send_message(message.chat.id, text='Выберите вашу роль: ', reply_markup=buttons)







        # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------Начало работы----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # if req[0] == 'start':  # Если метка start
    #     ChoosingTopicsResult = ChoosingTopics(tree)  # Вызываем функцию
    #     markup = InlineKeyboardMarkup()  # Определяем кнопку
    #     for i in range(0, len(ChoosingTopicsResult), 2):  # Бежим по списку, вовзвращенному функцией
    #         markup.add(InlineKeyboardButton(text=ChoosingTopicsResult[i],
    #                                         callback_data=str(int(i / 2))))  # Создаем соответствующие кнопки
    #     bot.edit_message_text(emoji.emojize(f"Выберите раздел: :magnifying_glass_tilted_left: "), reply_markup=markup,
    #                           chat_id=call.message.chat.id,
    #                           message_id=call.message.message_id)  # Выводим сопутствующее сообщение
    #     page = 0
    #     count = 0
    # # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # # --------------------------------------------------------------Ветка чат для общения----------------------------------------------------------------------------------------
    # # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # elif req[0] == '5':  # Если метка 5
    #     ChoosingTopicsResult = ChoosingTopics(tree)
    #     firstResult, endSlinding = FirstLevel(tree, ChoosingTopicsResult[int(req[0]) * 2],
    #                                           ChoosingTopicsResult)  # Вызываем функцию
    #     markup = InlineKeyboardMarkup()  # Определяем кнопку
    #     markup.add(InlineKeyboardButton(text=firstResult[0], url='https://vk.com/'))  # Создаем соответствующие кнопки
    #     markup.add(InlineKeyboardButton(text='Вернуться на главную',
    #                                     callback_data='start'))  # Создаем кнопку возврата на главную страницу
    #     bot.edit_message_text(emoji.emojize(f"А вот и ссылочка на чат для общения) 	:smiling_face_with_heart-eyes:"),
    #                           reply_markup=markup, chat_id=call.message.chat.id,
    #                           message_id=call.message.message_id)  # Выводим сопутствующее сообщение

# Обработчик входящих сообщений



# @bot.message_handler()  # Обрабатываем текстовые сообщения
# def start(m):
#     bot.send_message(m.from_user.id, emoji.emojize(
#         "Увы! :weary_face: Извините! Я еще плохо умею общаться 	:woman_facepalming:"))  # Выводим сопутствующее сообщение

if __name__ == '__main__':

    bot.polling(none_stop=True)
