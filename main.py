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
# # Определяем отклик
# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call):
#     req = call.data.split('_')
#     global count
#     global page


    # try:
    #     logs1 = pd.read_csv('C:/Users/50AdmNsk/Downloads/1.csv')
    #     del (logs1['Unnamed: 0'])
    #     time1 = str(datetime.datetime.now().time())
    #     dat1 = str(datetime.datetime.now().date())
    #     logs1 = logs1.concat({'date': dat1, 'time': time1, 'person_id': call.message.chat.id, 'branch_id': req[0]},
    #                          ignore_index=True)
    #     path2 = Path("C:/Users/50AdmNsk/Downloads/1.csv")
    #     logs1.to_csv(path2)
    # except:
    #     pass
    #
    # # Скачиваем таблицу состояний
    # global tree
    # path1 = Path("C:/Users/50AdmNsk/Downloads/tree.xlsx")
    # tree = pd.read_excel(path1)
    # del (tree['Unnamed: 0'])




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
@bot.message_handler(commands=['start'])  # Начинаем работу

def start(m):

    global count
    global page
    markup = InlineKeyboardMarkup()  # Определяем кнопку
    markup.add(InlineKeyboardButton(text=f'Начнем', callback_data=f'start'))
    bot.send_message(m.from_user.id, emoji.emojize(
        "Добрый день!:hand_with_fingers_splayed: Вы хотите узнать что-то про ЗОЖ?:red_question_mark: Тогда, нажмите кнопку: :play_button:"),
                    reply_markup=markup)  # Выводим сопутствующее сообщение


@bot.message_handler()  # Обрабатываем текстовые сообщения

def start(m):
    bot.send_message(m.from_user.id, emoji.emojize(
        "Увы! :weary_face: Я умею общаться только кнопками(	:woman_facepalming: Поэтому, пожалуйста, напишите мне /start, чтобы снова начать общение! :beating_heart:"))  # Выводим сопутствующее сообщение

if __name__ == '__main__':

    bot.polling(none_stop=True)
