import emoji
from datetime import timedelta
import datetime
from datetime import datetime
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SQL import db_start, all_table_from_db, rename_start_from_db, mailing_from_db, del_person_db, jobreload_from_db, \
    new_row_from_db
from quickstart import  update_parametr_google_sheets, delete_person_google_sheets, perfomance_google_sheets, read_table_google_sheets
import aioschedule
import asyncio
from googleDrive import upload_to_drive
from staticParametr import static_parametr
from performonitoring import performance_monitoring



#Подключаемся к боту
botMes = Bot(open(os.path.abspath('token.txt')).read())
bot = Dispatcher(botMes)


async def on_startup(_):
    await db_start()
    asyncio.create_task(scheduler())


# --------------------------------------------Отправка видео по дате------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# Создаем обработчик, который отправляет видео в заданное время
async def job():
    # Подгружаем базу
    base = await all_table_from_db('Unit')
    # print(base)

    # Работа по отправке видео. Если текущая дата совпадает с датой из таблицы, то
    if datetime.today().strftime('%Y-%m-%d %H:%M') == base['Дата'][0]:
        # Перебираем всех НЕ преподавателей и отправляем им видео
        for i in range(1, len(base)):
            if base['Группа'][i] != 'Преподаватель':
                await botMes.send_message(int(base['user_ID'][i]), f'Посмотрите видео и пройдите тест. \n {base["Видео"][0]}', parse_mode=types.ParseMode.HTML)
            elif base['Группа'][i] == 'Преподаватель':
                await botMes.send_message(int(base['user_ID'][i]), text=f"Видео открыто для просмотра.")
    # Работа по отправке теста. Определяем время отправки теста, с учетом длительности видео
    mint = datetime.strptime(str(base['Дата'][0]), '%Y-%m-%d %H:%M')+ timedelta(minutes=int(base['Продолжительность (мин)'][0]))
    # Если текущие дата, время совпадает с расчетной отправкой теста, то
    if datetime.today().strftime('%Y-%m-%d %H:%M') == mint.strftime('%Y-%m-%d %H:%M'):
        # Перебираем всех НЕ преподавателей и высылаем кнопку на прохождение теста
        for i in range(1, len(base)):
            if base['Группа'][i] != 'Преподаватель':
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(text='Пройти тест', callback_data='testr'))
                await botMes.send_message(int(base['user_ID'][i]), text=f"Для начала тестирования нажмите на кнопку: ", reply_markup=markup)
            elif base['Группа'][i] == 'Преподаватель':
                await botMes.send_message(int(base['user_ID'][i]), text=f"Тест открыт для прохождения.")
    # Отправка домашнего задания
    if datetime.today().strftime('%Y-%m-%d %H:%M') == base['Дата домашнего задания'][0]:
        # Перебираем всех НЕ преподавателей и отправляем им видео
        for i in range(1, len(base)):
            if base['Группа'][i] != 'Преподаватель':
                await botMes.send_message(int(base['user_ID'][i]), text=f'Домашнее задание: \n {base["Домашнее задание"][0]}', parse_mode=types.ParseMode.HTML)
                await botMes.send_message(int(base['user_ID'][i]), 'Для отправки домашнего задания боту - просто отправьте файл боту. \n Внимание! Файл должен иметь расширение docx! Если вы хотите перезаписать файл, то воспользуйтесь тегом /jobreload', parse_mode=types.ParseMode.HTML)
            elif base['Группа'][i] == 'Преподаватель':
                await botMes.send_message(int(base['user_ID'][i]), text=f"Домашнее задание открыто для учеников.")
    if base['Даты начала и конца блока'][0] != "start":
        for i in range(1, len(base)):
            await botMes.send_message(int(base['user_ID'][i]), text=f"Инициирован {base['Блок: Начало'][1]}. Даты начала и конца блока: {base['Даты начала и конца блока'][1]}.")
            base['Даты начала и конца блока'][0] = "start"
            await rename_start_from_db('Unit')
            await update_parametr_google_sheets('Unit', 2, 4, 'Start')
    # Бежим по столбцу комментариев. Если он есть, то отправить всем ученикам и стереть, преподавателя предупредить
    for a in range(1, len(base)):
        if not str(base['Комментарий'][a]) is None and str(base['Комментарий'][a]) != "" and str(base['Комментарий'][a]) != " " and str(base['Комментарий'][a]) != "comm":
            for j in range(1, len(base)):
                if str(base['Группы рассылки'][a]) != 'Все':
                    if (base['Группа'][j] != "Преподаватель" and (str(base['Группа'][j])) in str(base['Группы рассылки'][a])):
                        await botMes.send_message(int(base['user_ID'][j]), text=base['Комментарий'][a])
                    if base['Группа'][j] == "Преподаватель":
                        await botMes.send_message(int(base['user_ID'][j]), text='Сообщение отправлено')
                else:
                    if base['Группа'][j] != "Преподаватель":
                        await botMes.send_message(int(base['user_ID'][j]), text=base['Комментарий'][a])
                    if base['Группа'][j] == "Преподаватель":
                        await botMes.send_message(int(base['user_ID'][j]), text='Сообщение отправлено')
            base['Комментарий'][a] = ""
            await mailing_from_db('Unit', '`Комментарий`', base['user_ID'][a])
            await update_parametr_google_sheets('Unit', a, 24, '')
            base['Группы рассылки'][a] = ""
            await mailing_from_db('Unit', '`Группы рассылки`', base['user_ID'][a])
            await update_parametr_google_sheets('Unit', a, 25, '')
#
    # отправка оповещений ученикам
    dtC1 = 15  # первый контроль (через 15 дней)
    dtC2 = 27  # второй контроль (через 27 дней)
    # Работа по отправке оповещения. Если текущая дата совпадает с датой из таблицы, то
    # Перебираем всех НЕ преподавателей и отправляем им видео

    dt1 = datetime.today() + timedelta(days=dtC1)  # к текущей дате добавляем 15 дней
    dt2 = datetime.today() + timedelta(days=dtC2)  # к текущей дате добавляем 27 дней
    # отослать оповещение о необходимости тестирования и сдачи ДЗ
    # В поле 'Дата' - дата предоставления теста
    if (dt1.strftime('%Y-%m-%d %H:%M') == base['Дата'][0]) or (dt2.strftime('%Y-%m-%d %H:%M') == base['Дата'][0]):
        # пора напомнить о тестировании
        for i in range(1, len(base)):
            # Перебираем всех НЕ преподавателей
            if (base['Группа'][i] != 'Преподаватель') and (base['Отметка о прохождении теста'][i] != 'Пройдено'):
                await botMes.send_message(int(base['user_ID'][i]),
                                    text='Уважаемый ' + base['Участники курса'][i] + ", пройти тест необходимо до " +
                                        base['Дата'][0])
    # В поле 'Дата домашнего задания' - дата предоставления ДЗ
    if (dt1.strftime('%Y-%m-%d %H:%M') == base['Дата домашнего задания'][0]) or (
            dt2.strftime('%Y-%m-%d %H:%M') == base['Дата домашнего задания'][0]):
        for i in range(1, len(base)):
            # Перебираем всех НЕ преподавателей
            if (base['Группа'][i] != 'Преподаватель') and ((base['Отметка об отправке ДЗ'][i] != 'Загружено') and (
                    base['Отметка об отправке ДЗ'][i] != 'Перезагружено')):
                await botMes.send_message(int(base['user_ID'][i]),
                                    text='Уважаемый ' + base['Участники курса'][i] + ", Необходимо сдать ДЗ " +
                                        base['Дата домашнего задания'][0])
#
# Контроллер, который выполняет работу каждую минуту
async def scheduler():
    # print(0)
    aioschedule.every(1).minutes.do(job)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)



# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# # Инициирование нового блока
# @bot.message_handler(commands=['massmessage'])
# def start_message(message, ):
#     base = pd.read_excel("C:/Users/50AdmNsk/PycharmProjects/Chat-bot-reservists/testBase.xlsx")
#     del (base['Unnamed: 0'])

@bot.message_handler(commands=['grade_synchronization'])
async def start_message(message):
    #Получение списка оценок учеников с гугл диска
    base = await all_table_from_db('Unit')
    if base[base['user_ID'] == str(message.chat.id)]['Группа'].values[0] == "Преподаватель":
        df = await performance_monitoring()
        # print(df)
        await perfomance_google_sheets(df)
        await botMes.send_message(message.chat.id, text='Перейдите по ссылке, чтобы сверить оценки: https://docs.google.com/spreadsheets/d/1ZhNTjrrJF3NTNqAMcRK497vjR5JHzxAblerf1qS4DYY/edit?usp=sharing \n После выставления оценок воспользуйтесь тегом /put_down_marks, чтобы оценки были внесены в таблицу')
    else:
        await botMes.send_message(message.chat.id, text='Ученик не может воспользоваться этой функцией')


@bot.message_handler(commands=['put_down_marks'])
async def start_message(message):
    #Получение списка оценок учеников с гугл диска
    base = await all_table_from_db('Unit')
    if base[base['user_ID'] == str(message.chat.id)]['Группа'].values[0] == "Преподаватель":
        performance = await read_table_google_sheets('Unit', 'Performance')
        unit = await read_table_google_sheets('Unit', 'Unit')
        for i in range(0, len(performance)):
            for j in range(1, len(unit)):
                # print(performance['name'][i].replace(' ', ''), ", ", unit['Участники курса'][j].replace(' ', ''), ", ", performance['name'][i].replace(' ', '') == unit['Участники курса'][j].replace(' ', ''))
                if performance['name'][i].replace(' ', '') == unit['Участники курса'][j].replace(' ', ''):
                    await jobreload_from_db("Unit", "Отметка за ДЗ", base['user_ID'][j], performance['folder'][j])
                    await update_parametr_google_sheets('Unit', j + 2, 20, performance['folder'][j])
                    unit['Отметка за ДЗ'][i] = performance['folder'][j]
        # unit.to_excel(os.path.abspath('un.xlsx'))
        await botMes.send_message(message.chat.id, text='Оценки выставлены!')
    else:
        await botMes.send_message(message.chat.id, text='Ученик не может воспользоваться этой функцией')


# Если преподаватель хочет отправить массовый комментарий, то
@bot.message_handler(commands=['massmessage'])
async def start_message(message, ):
    base = await all_table_from_db('Unit')
    # Найти пользователя
    for i in range(1, len(base)):
        if str(message.chat.id) == base['user_ID'][i]:
            if base['Группа'][i] == 'Преподаватель':
                await botMes.send_message(message.chat.id, text='Напишите список групп, которые должны получить сообщение, в следующем виде: "Грп: 1, 2 ..., n". \n Если хотите, чтобы сообщение получили все ученики, то напишите "Всем грп".', )
            elif base['Группа'][i] != 'Преподаватель':
                await botMes.send_message(message.chat.id, text='Ученик не могут отправлять массовые комментарии!', )

# Обработка тега повторного прохождения теста
@bot.message_handler(commands=['opentest'])
async def start_message(message, ):
    base = await all_table_from_db('Unit')
    for i in range(1, len(base)):
        if base['user_ID'][i] == str(message.chat.id):
            if base['Группа'][i] == 'Преподаватель':
                await botMes.send_message(message.chat.id, text='Чтобы открыть тест ученику напишите: "Открыть тест: ФИО группа". Например: "Открыть тест: Иванов Иван Иванович 1"', )
            else:
                await botMes.send_message(message.chat.id, text='Ученик не может сам открыть тест!', )

# Число зарегистрированных учеников
@bot.message_handler(commands=['students'])
async def start_message(message, ):
    base = await all_table_from_db('Unit')
    cou = 0
    for i in range(1, len(base)):
        if base['Группа'][i] != 'Преподаватель':
            cou += 1
    await botMes.send_message(message.chat.id, text=f'На данный момент в боте зарегистрировано учеников: {cou}', )


# Если ученик хочет оставить рефлексию, то создаем кнопки
@bot.message_handler(commands=['reflection'])
async def start_message(message):
    buttons = InlineKeyboardMarkup()
    buttons.add(InlineKeyboardButton(text='О качестве курса', callback_data='course'))
    buttons.add(InlineKeyboardButton(text='О способе коммуникации', callback_data='communic'))
    buttons.add(InlineKeyboardButton(text='Общее', callback_data='general'))

    await botMes.send_message(message.chat.id, text='О чем вы хотите написать отзыв?', reply_markup=buttons)


# Если ученик хочет перерегистрироваться, то удаляем его запись и просим зарегиситрироваться
@bot.message_handler(commands=['reregistration'])
async def start_message(message, ):
    base = await all_table_from_db('Unit')
    # Найти пользователя
    for i in range(1, len(base)):
        if str(message.chat.id) == base['user_ID'][i]:
            await botMes.send_message(message.chat.id, text='Введите ваши фамилию, имя и отчество.')
            await del_person_db('Unit', base['user_ID'][i])
            await delete_person_google_sheets('Unit', i+2)


#
#
# Подсказка о возможностях чат-бота
@bot.message_handler(commands=['help'])
async def start_message(message, ):
    await botMes.send_message(message.chat.id, text='Чат-бот может отвечать только по программе, либо по запросам тегов. Если ему задать произвольные вопросы – он их не поймет. \n Теги: \n '
                                           '/help – описание всех возможностей бота \n /massmessage – отправка сообщения всем ученикам (только преподаватель) \n /reflection – оставить отзыв \n '
                                           '/reregistration – повторная регистрация на курс \n /jobreload – перезагрузка домашнего задания \n /opentest - открыть тест повторно (для преподавателя) \n /start – начало работы с ботом (регистрация) \n '
                                           'Ученик в определенное время получает ссылку на видео. После просмотра видео появляется кнопка доступа к тестированию. Тест проходится один раз. '
                                           'После прохождения теста бот, в определенное время, отправляет домашнее задание. Ученик может перезагружать домашнее задание. \n '
                                           'Преподаватель может назначать даты и видеть полную картину активности учеников. Бот отправляет преподавателю отчет о действии всех учеников. '
                                           'Преподаватель может инициировать новый блок обучения раньше, а может раньше закончить текущий блок.' )



# Обработка тега перезагрузки ДЗ
@bot.message_handler(commands=['jobreload'])
async def start_message(message):
    base = await all_table_from_db('Unit')
    # Найти пользователя и изменить значение в таблице
    for i in range(1, len(base)):
        if str(message.chat.id) == base['user_ID'][i]:
            await botMes.send_message(message.chat.id, "Жду вашу работу.")
            # print(await jobreload_from_db("Unit", "`Отметка об отправке ДЗ`", base['user_ID'][i], "Перезагружено+"))
            await jobreload_from_db("Unit", "Отметка об отправке ДЗ", base['user_ID'][i], "Перезагружено+")
            await update_parametr_google_sheets('Unit', i+2, 19, 'Перезагружено+')


# Обработка документов
@bot.message_handler(content_types=["document"])
async def handle_docs_audio(message):
    document_id = message.document.file_id
    file_info = await botMes.get_file(document_id)
    base = await all_table_from_db('Unit')
    # Определяем ID пользователя
    for i in range(0, len(base)):
        if base['user_ID'][i] == str(message.chat.id):
            ind = i
    # Если это первичная перезагрузка, то сохраняем файл с новым названием
    if base['Отметка об отправке ДЗ'][ind] == "Перезагружено+":
        base['Отметка об отправке ДЗ'][ind] = "Перезагружено"
        await jobreload_from_db("Unit", 'Отметка об отправке ДЗ', base['user_ID'][ind], 'Перезагружено')
        await update_parametr_google_sheets('Unit', ind + 2, 19, 'Перезагружено')
        try:
            await upload_to_drive(file_path=f'http://api.telegram.org/file/bot{open(os.path.abspath("token.txt")).read()}/{file_info.file_path}', filename=(str(base['Участники курса'][ind]) + '_reload.docx'))
        except:
            pass
        os.remove(os.path.abspath((str(base['Участники курса'][ind]) + '_reload.docx')))
        await botMes.send_message(message.chat.id, "Работа загружена заново.")
        # Отправка оповещения преподавателю
        for i in range(1, len(base)):
            if base['Группа'][i] == 'Преподаватель':
                await botMes.send_message(base['user_ID'][i], text=f"Ученик {base['Участники курса'][ind]} повторно загрузил работу")
    # Если это загрузка домашнего задания, то
    else:
        if str(message.chat.id) == str(int(base['user_ID'][ind])):
            # if len(str(base['Отметка об отправке ДЗ'][ind])) <= 3:
            if str(base['Отметка об отправке ДЗ'][ind]) is None or str(base['Отметка об отправке ДЗ'][ind]) == "" or str(base['Отметка об отправке ДЗ'][ind]) == " ":
                try:
                    await upload_to_drive(file_path=f'http://api.telegram.org/file/bot{open(os.path.abspath("token.txt")).read()}/{file_info.file_path}', filename=(str(base['Участники курса'][ind]) + '.docx'))
                except:
                    pass
                os.remove(os.path.abspath((str(base['Участники курса'][ind]) + '.docx')))
                base['Отметка об отправке ДЗ'][ind] = 'Готово'
                await jobreload_from_db("Unit", 'Отметка об отправке ДЗ', base['user_ID'][ind], 'Готово')
                await update_parametr_google_sheets('Unit', ind + 2, 19, 'Готово')
                await botMes.send_message(message.chat.id,
                                 "Работа отправлена преподавателю на проверку.")
                # Отправка оповещения преподавателю
                for i in range(1, len(base)):
                    if base['Группа'][i] == 'Преподаватель':
                        await botMes.send_message(base['user_ID'][i],
                                     text=f"Ученик {base['Участники курса'][ind]} загрузил работу")
            # Если пользователь пытается перезагрузить ДЗ
            else:
                await botMes.send_message(message.chat.id,
                                 "Если вы хотите перезаписать файл, то воспользуйтесь тегом /jobreload")



# Обработка действий при старте бота
@bot.message_handler(commands=['start'])
async def start_message(message):
    # Считываем таблицу
    base = await all_table_from_db('Unit')
    # Если пользователь уже регистрировался, то
    if str(message.chat.id) in base['user_ID'].unique():
        await botMes.send_message(message.chat.id,
                         "Вы уже зарегистрированы! Для перерегистрации нажмите /reregistration")
    # Если пользователь регистрируется первый раз, то
    else:
        await botMes.send_message(message.chat.id, emoji.emojize(
            "Добрый день!:hand_with_fingers_splayed: Давайте начнем учиться! Для этого вы должны зарегистрироваться."))
        await botMes.send_message(message.chat.id,
                         emoji.emojize("Введите ваши фамилию, имя и отчество: :magnifying_glass_tilted_left:"))

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------Обработка текста------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Обработка входящего текста
@bot.message_handler(content_types='text')
async def next_message(message):
    # Считываем таблицу
    base = await all_table_from_db('Unit')
    # Создаем переменную для контроля сообщения о незнании
    control = 0
    # Бежим по всем колонкам рефлексии, и если где-то увидели пометку, то туда и записываем сообщение
    for i in range(1, len(base)):
        if str(message.chat.id) == base['user_ID'][i]:
            idM = i
            if not str(base['Рефлексия о курсе'][i]) is None and str(base['Рефлексия о курсе'][i]) != "" and str(base['Рефлексия о курсе'][i]) != " ":
                if str(base['Рефлексия о курсе'][i])[-6:] == 'course':
                    base['Рефлексия о курсе'][i] = base['Рефлексия о курсе'][i] + '[' + datetime.today().strftime('%Y-%m-%d %H:%M') + '] ' + message.text
                    await jobreload_from_db("Unit", 'Рефлексия о курсе', base['user_ID'][i], base['Рефлексия о курсе'][i] + '[' + datetime.today().strftime('%Y-%m-%d %H:%M') + '] ' + message.text)
                    await update_parametr_google_sheets('Unit', i + 2, 21, base['Рефлексия о курсе'][i] + '[' + datetime.today().strftime('%Y-%m-%d %H:%M') + '] ' + message.text)
                    control = 1
                    await botMes.send_message(message.chat.id, text=f"Спасибо за ваш отзыв!")
            if not str(base['Рефлексия о взаимодействии'][i]) is None and str(base['Рефлексия о взаимодействии'][i]) != "" and str(base['Рефлексия о взаимодействии'][i]) != " ":
                if str(base['Рефлексия о взаимодействии'][i][-8:]) == 'communic':
                    base['Рефлексия о взаимодействии'][i] = base['Рефлексия о взаимодействии'][i] + '[' + datetime.today().strftime('%Y-%m-%d %H:%M') + '] ' + message.text
                    await jobreload_from_db("Unit", 'Рефлексия о взаимодействии', base['user_ID'][i], base['Рефлексия о взаимодействии'][i] + '[' + datetime.today().strftime('%Y-%m-%d %H:%M') + '] ' + message.text)
                    await update_parametr_google_sheets('Unit', i + 2, 22, base['Рефлексия о взаимодействии'][i] + '[' + datetime.today().strftime('%Y-%m-%d %H:%M') + '] ' + message.text)
                    control = 1
                    await botMes.send_message(message.chat.id, text=f"Спасибо за ваш отзыв!")
            if not str(base['Рефлексия общее'][i]) is None and str(base['Рефлексия общее'][i]) != "" and str(base['Рефлексия общее'][i]) != " ":
                if str(base['Рефлексия общее'][i][-7:]) == 'general':
                    base['Рефлексия общее'][i] = base['Рефлексия общее'][i] + str('[' + str(datetime.today().strftime('%Y-%m-%d %H:%M')) + '] ' + message.text)
                    await jobreload_from_db("Unit", 'Рефлексия общее', base['user_ID'][i], base['Рефлексия общее'][i] + str('[' + str(datetime.today().strftime('%Y-%m-%d %H:%M')) + '] ' + message.text))
                    await update_parametr_google_sheets('Unit', i + 2, 23, base['Рефлексия общее'][i] + str('[' + str(datetime.today().strftime('%Y-%m-%d %H:%M')) + '] ' + message.text))
                    control = 1
                    await botMes.send_message(message.chat.id, text=f"Спасибо за ваш отзыв!")

    #Если это повторное открытие теста, то
    if len(str(message.text)) > 13:
        if "Открыть тест:" in message.text:
            text = (message.text).split()
            grp = text[-1]
            print(text)
            print(grp)
            nam=""
            for r in range(1, len(text)-2):
                nam = nam + text[1+r] + " "
                print(nam)
            for f in range(1, len(base)):
                print(base['Участники курса'][f] in nam)
                print(str(base['Группа'][f]) == grp)
                if base['Участники курса'][f] in nam and str(base['Группа'][f]) == grp:
                    base['Отметка о прохождении теста'] = ""
                    await jobreload_from_db("Unit", 'Отметка о прохождении теста', base['user_ID'][f], "")
                    await update_parametr_google_sheets('Unit', f + 2, 16, "")
                    base['Итого баллов?'] = ""
                    await jobreload_from_db("Unit", 'Итого баллов?', base['user_ID'][f], "")
                    await update_parametr_google_sheets('Unit', f + 2, 15, "")
                    await botMes.send_message(message.chat.id, text=f"Доступ открыт.")
                    markup = InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton(text='Пройти тест', callback_data='testr'))
                    await botMes.send_message(int(base['user_ID'][f]), text=f"Вам открыт доступ для повторного прохождения теста.", reply_markup=markup)

    # Если пользователь зарегистрировался и внес иформацию о своей группе, то
    # if control == 0:
    #     idM = base[base['user_ID'] == str(message.chat.id)]
    #     print(len(str(list(base[base['user_ID'] == str(message.chat.id)]['Группа'])))-2)
    #     # if str(message.chat.id) in base['user_ID'].unique() and len(str(list(base[base['user_ID'] == str(message.chat.id)]['Группа'])))-2 <= 2:
    #     if not str(message.chat.id) in base['user_ID'].unique():
    #         print(1)
    #         # print(len(str(list(base[base['user_ID'] == str(message.chat.id)]['Группа']))))
    #         # print(str(list(base[base['user_ID']] )))
    #         await botMes.send_message(message.chat.id, emoji.emojize(
    #             "Увы! :weary_face: Извините! Я еще плохо умею общаться 	:woman_facepalming:"))
    #     # if (str(message.chat.id) in base['user_ID'].unique()) and  ('Преподаватель' in list(base[base['user_ID'] == str(message.chat.id)]['Группа'])) and (not str(base['Комментарий'][idM]) is None and str(base['Комментарий'][idM]) != "" and str(base['Комментарий'][idM]) != " "):
    #     if (base[base['user_ID'] == str(message.chat.id)] is None) and  ('Преподаватель' in list(base[base['user_ID'] == str(message.chat.id)]['Группа'])) and (not str(base['Комментарий'][idM]) is None and str(base['Комментарий'][idM]) != "" and str(base['Комментарий'][idM]) != " "):
    #         print(2)
    #         # if list(base[base['user_ID'] == message.chat.id]['Группа']) == message.text:
    #         #     bot.send_message(message.chat.id, emoji.emojize(
    #         #     "Увы! :weary_face: Извините! Я еще плохо умею общаться 	:woman_facepalming:"))
    #         if len(str(message.text)) >= 5:
    #             print(3)
    #             if len(str(message.text)) >= 8:
    #                 if str(message.text)[0:8] != 'Всем грп' and str(message.text)[0:5] != 'Грп:':
    #                     if list(base[base['user_ID'] == str(message.chat.id)]['Группа']) == message.text:
    #                         await botMes.send_message(message.chat.id, emoji.emojize(
    #                             "Увы! :weary_face: Извините! Я еще плохо умею общаться 	:woman_facepalming:"))
    #             else:
    #                 print(4)
    #                 if str(message.text)[0:5] != 'Грп:':
    #                     if list(base[base['user_ID'] == str(message.chat.id)]['Группа']) == message.text:
    #                         await botMes.send_message(message.chat.id, emoji.emojize(
    #                             "Увы! :weary_face: Извините! Я еще плохо умею общаться 	:woman_facepalming:"))
    #
    #     elif  (base[base['user_ID'] == str(message.chat.id)] is None) and  ('Преподаватель' in list(base[base['user_ID'] == str(message.chat.id)]['Группа'])) and (not str(base['Комментарий'][idM]) is None and str(base['Комментарий'][idM]) != "" and str(base['Комментарий'][idM]) != " "):
    #         print(5)
    #         # bot.send_message(message.chat.id, emoji.emojize(
    #         #     "Увы! :weary_face: Извините! Я еще плохо умею общаться 	:woman_facepalming:"))
    #         if len(str(message.text)) >= 5:
    #             if len(str(message.text)) >= 8:
    #                 print(6)
    #                 if str(message.text)[0:8] != 'Всем грп' and str(message.text)[0:5] != 'Грп:' and not(str(message.text)[0:5] != 'Открыть тест:'):
    #                     await botMes.send_message(message.chat.id, emoji.emojize(
    #             	"Увы! :weary_face: Извините! Я еще плохо умею общаться 	:woman_facepalming:"))
    #             else:
    #                 print(7)
    #                 if str(message.text)[0:5] != 'Грп:':
    #                     await botMes.send_message(message.chat.id, emoji.emojize(
    #             	"Увы! :weary_face: Извините! Я еще плохо умею общаться 	:woman_facepalming:"))

    # Если пользователь еще не зарегистрирован, то
    if control==0 :
        print(1111)
        idM = base[base['user_ID'] == str(message.chat.id)]
        # Проверяем, зарегистрировал ли человек имя и, если да, то определяем, где его строчка в таблице
        base = await all_table_from_db('Unit')
        for i in range(0, len(base)):
            if len(str(base['user_ID'][i])) > 3:
                if str(message.chat.id) == str(int(base['user_ID'][i])):
                    idM = i
                    if base['Комментарий'][i] == 'comm':
                        base['Комментарий'][i] = str(message.text)
                        await jobreload_from_db("Unit", 'Комментарий', base['user_ID'][i], str(message.text))
                        await update_parametr_google_sheets('Unit', i + 2, 24, str(message.text))
                        await botMes.send_message(message.chat.id, text='Сообщение будет разослано.', )

                    # Если пользователь ввел имя и группу, то
                    # print(len(base['Группа'][idM]))
                    if (base['Группа'][idM] is None or base['Группа'][idM] == "") and (not str(base['Участники курса'][idM]) is None and str(base['Участники курса'][idM]) != "" and str(base['Участники курса'][idM]) != " "):
                        print(2222)
                        # Дозаписываем данные и сохраняем таблицу
                        group = message.text
                        # try:

                        # except:
                        #     pass

                        # base.loc[:, ('Группа',idM) ] = group

                        await botMes.send_message(message.chat.id, 'Отлично! Давайте приступим к работе!')
                        await botMes.send_message(message.chat.id,
                                         'Для начала, необходимо ознакомиться с некоторыми правилами. \n У вас есть несколько учебных блоков, '
                                         'к каждому из которых есть обязательное задание. Блок состоит из обучающего видео, проверочного теста и домашнего задания. \n '
                                         'Выполняйте все задания в срок! \n Иногда вам будут приходить напоминания, что пора приступить к работе и сообщения от преподавателя. Если вы захотите '
                                         'перезагрузить домашнюю работу - воспользуйтесть тегом /jobreload. Если вы захотите оставить рефлексию - воспользуйтесь тегом /reflection. '
                                         'Если вы хотите вспомнить, какие теги за что отвечают, то воспользуйтесь тегом /help \n '
                                         'Желаю успешной учебы!')
                        base = await static_parametr(base, idM, group)
                    # elif base['Группа'][idM] is None or base['Группа'][idM] == "":
                    #     await botMes.send_message(message.chat.id, 'Вы пытаетесь повторно внести название группы! Для перерегистрации нажмите тег /reregistration')
                # else: idM=0
            else: idM=0
        # Если пользователь ввел имя, но не ввел группу, то
        if idM==0:

            # Дозаписываем данные и сохраняем таблицу
            name = message.text
            await new_row_from_db('Unit', name, str(message.chat.id))
            await update_parametr_google_sheets('Unit', len(base)+2, 1, name)
            # Создаем кнопки
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(text='Преподаватель', callback_data='but1'))
            markup.add(InlineKeyboardButton(text='Ученик', callback_data='but2'))
            await botMes.send_message(message.chat.id, text=f"Выберите вашу роль: ", reply_markup=markup)

    if str(message.text)[0:4] == 'Грп:' or str(message.text)[0:8] == 'Всем грп':
        for i in range(1, len(base)):
            if str(message.chat.id) == base['user_ID'][i]:
                base['Комментарий'][i] = 'comm'
                await jobreload_from_db("Unit", 'Комментарий', base['user_ID'][i], 'comm')
                await update_parametr_google_sheets('Unit', i + 2, 24, 'comm')
                if str(message.text)[0:4] == 'Грп:':
                    base['Группы рассылки'][i] = str(message.text)[4:]
                    await jobreload_from_db("Unit", 'Группы рассылки', base['user_ID'][i], str(message.text)[4:])
                    await update_parametr_google_sheets('Unit', i + 2, 25, str(message.text)[4:])
                if str(message.text)[0:8] == 'Всем грп':
                    base['Группы рассылки'][i] = 'Все'
                    await jobreload_from_db("Unit", 'Группы рассылки', base['user_ID'][i], 'Все')
                    await update_parametr_google_sheets('Unit', i + 2, 25, 'Все')
                await botMes.send_message(message.chat.id, text=f"Напишите сообщение, и я его перешлю.")


# Обработка кнопок
@bot.callback_query_handler()
async def callback_query(callback: types.CallbackQuery):
    call = callback
    req = call.data.split('_')
    print(req[0])
    # Считываем таблицу
    base = await all_table_from_db('Unit')
    iDM = base[base['user_ID'] == str(call.message.chat.id)]
    for i in range(1, len(base)):
        if str(call.message.chat.id) == base['user_ID'][i]:
            iDM = i
    # Если выбранная группа - ученик, то
    if req[0] == 'but2':
        await botMes.send_message(call.message.chat.id, 'Введите вашу группу:')
    # Если нажата кнопка прохождения теста
    elif req[0] == 'testr':
        # Ищем человека в базе и, в его строку, вносим пометку о просмотре видео
        for i in range(1, len(base)):
            if str(call.message.chat.id) == base['user_ID'][i]:
                base['Отметка о просмотре'][i] = 'Пройдено'
                await jobreload_from_db("Unit", 'Отметка о просмотре', base['user_ID'][i], 'Пройдено')
                await update_parametr_google_sheets('Unit', i + 2, 8, 'Пройдено')
                # Отправка оповещения преподавателю
                for a in range(1, len(base)):
                    if base['Группа'][a] == 'Преподаватель' and (str(base['Отметка о просмотре'][i]) is None or str(base['Отметка о просмотре'][i]) == "" or str(base['Отметка о просмотре'][i]) == " "):
                        await botMes.send_message(base['user_ID'][a],
                                         text=f"Ученик {base['Участники курса'][i]} просмотрел видео")
                iDM=i
        # Если человек пытается повторно пройти тест, то
        if base['Итого баллов?'][iDM] >= '0':
            await botMes.send_message(call.message.chat.id,
                             text='Внимание! Без разрешения преподавателя проходить тест повторно запрещено!')
        # Если человек первый раз проходит тест, то  выводим первый вопорос
        else:
            question = base['Тест 1'][0]
            buttons = InlineKeyboardMarkup()
            buttons.add(InlineKeyboardButton(text='1', callback_data='t1v1'))
            buttons.add(InlineKeyboardButton(text='2', callback_data='t1v2'))
            buttons.add(InlineKeyboardButton(text='3', callback_data='t1v3'))
            buttons.add(InlineKeyboardButton(text='4', callback_data='t1v4'))
            await botMes.send_message(call.message.chat.id, text=str(question), reply_markup=buttons)
    # Если это ответ на первый вопрос, то
    elif 't1' in req[0] and not('but' in req[0]):
        if base['Отметка о прохождении теста'][iDM] != "Пройдено":
            # Задаем начальное число баллов, раное нулю
            for i in range(1, len(base)):
                if str(call.message.chat.id) == base['user_ID'][i]:
                    iDM = i
                    base['Итого баллов?'][iDM] = 0
                    await jobreload_from_db("Unit", 'Итого баллов?', base['user_ID'][iDM], '0')
                    await update_parametr_google_sheets('Unit', iDM + 2, 15, '0')
            answer = ""
            # Получаем ответ на вопрос
            if req[0] == 't1v1': answer = "1"
            if req[0] == 't1v2': answer = "2"
            if req[0] == 't1v3': answer = "3"
            if req[0] == 't1v4': answer = "4"
            # Если ответ верен, то присваиваем балл
            if str(base['Ответ 1'][0]) == answer:
                base['Итого баллов?'][iDM] = int(base['Итого баллов?'][iDM])+1
                await jobreload_from_db("Unit", 'Итого баллов?', base['user_ID'][iDM], str(int(base['Итого баллов?'][iDM])))
                await update_parametr_google_sheets('Unit', iDM + 2, 15, str(int(base['Итого баллов?'][iDM])))
            # Создаем кнопки для второго вопроса
            question = base['Тест 2'][0]
            buttons = InlineKeyboardMarkup()
            buttons.add(InlineKeyboardButton(text='1', callback_data='t2v1'))
            buttons.add(InlineKeyboardButton(text='2', callback_data='t2v2'))
            buttons.add(InlineKeyboardButton(text='3', callback_data='t2v3'))
            buttons.add(InlineKeyboardButton(text='4', callback_data='t2v4'))
            await botMes.send_message(call.message.chat.id, text=str(question), reply_markup=buttons)
        else:
            await botMes.send_message(call.message.chat.id,
                             text='Внимание! Без разрешения преподавателя проходить тест повторно запрещено!')
    # Если это ответ на второй вопрос, то
    elif 't2' in req[0] and not('but' in req[0]):
        if base['Отметка о прохождении теста'][iDM] != "Пройдено":
            for i in range(1, len(base)):
                if str(call.message.chat.id) == base['user_ID'][i]:
                    iDM = i
            answer = ""
            # Получаем ответ на вопрос
            if req[0] == 't2v1': answer = "1"
            if req[0] == 't2v2': answer = "2"
            if req[0] == 't2v3': answer = "3"
            if req[0] == 't2v4': answer = "4"
            # Если ответ правильный, то присваиваем балл
            if str(base['Ответ 2'][0]) == answer:
                base['Итого баллов?'][iDM] = int(base['Итого баллов?'][iDM]) + 1
                await jobreload_from_db("Unit", 'Итого баллов?', base['user_ID'][iDM], str(int(base['Итого баллов?'][iDM])))
                await update_parametr_google_sheets('Unit', iDM + 2, 15, str(int(base['Итого баллов?'][iDM])))
            # Создаем третий вопрос
            question = base['Тест 3'][0]
            buttons = InlineKeyboardMarkup()
            buttons.add(InlineKeyboardButton(text='1', callback_data='t3v1'))
            buttons.add(InlineKeyboardButton(text='2', callback_data='t3v2'))
            buttons.add(InlineKeyboardButton(text='3', callback_data='t3v3'))
            buttons.add(InlineKeyboardButton(text='4', callback_data='t3v4'))
            await botMes.send_message(call.message.chat.id, text=str(question), reply_markup=buttons)
        else:
            await botMes.send_message(call.message.chat.id,
                             text='Внимание! Без разрешения преподавателя проходить тест повторно запрещено!')
    # Если это ответ на третий вопрос, то
    elif 't3' in req[0] and not('but' in req[0]):
        if base['Отметка о прохождении теста'][iDM] != "Пройдено":
            for i in range(1, len(base)):
                if str(call.message.chat.id) == base['user_ID'][i]:
                    iDM = i
            answer = ""
            # Получаем ответ на вопрос
            if req[0] == 't3v1': answer = "1"
            if req[0] == 't3v2': answer = "2"
            if req[0] == 't3v3': answer = "3"
            if req[0] == 't3v4': answer = "4"
            # Если ответ правильный, то присваиваем балл
            if str(base['Ответ 3'][0]) == answer:
                base['Итого баллов?'][iDM] = int(base['Итого баллов?'][iDM]) + 1
                await jobreload_from_db("Unit", 'Итого баллов?', base['user_ID'][iDM], str(int(base['Итого баллов?'][iDM])))
                await update_parametr_google_sheets('Unit', iDM + 2, 15, str(int(base['Итого баллов?'][iDM])))
            base = await all_table_from_db('Unit')
            # Если тест пройден, то
            if int(float(base["Итого баллов?"][iDM]) * 100 / 3) > 50:
                base['Отметка о прохождении теста'][iDM] = "Пройдено"
                base = await all_table_from_db('Unit')
                await botMes.send_message(call.message.chat.id,
                                 f'Вы сдали тест на :{int(float(base["Итого баллов?"][iDM]) * 100 / 3)}%. \n Теперь вы можете приступить к выполнению домашнего задания.')
                for i in range(1, len(base)):
                    if base['Группа'][i] == 'Преподаватель':
                        await botMes.send_message(base['user_ID'][i],
                                         text=f"Ученик {base['Участники курса'][iDM]} прошел тест с баллом {int(float(base['Итого баллов?'][iDM]) * 100 / 3)}%.")
            # Если тест не пройден, то
            else:
                await botMes.send_message(call.message.chat.id,
                                 f'Вы не прошли тест. Обратитесь к преподавателю.')
                for i in range(1, len(base)):
                    if base['Группа'][i] == 'Преподаватель':
                        await botMes.send_message(base['user_ID'][i],
                                         text=f"Ученик {base['Участники курса'][iDM]} не прошел тест")
        else:
            await botMes.send_message(call.message.chat.id,
                             text='Внимание! Без разрешения преподавателя проходить тест повторно запрещено!')
    # Если это один из видов рефлексии, то
    elif req[0] == 'course' or req[0] == 'communic' or req[0] == 'general':
        await botMes.send_message(call.message.chat.id, text=f"Жду ваше сообщение.")
        # Перебираем столбцы рефлексии и, в зависимости от пустоты ячейки, записываем в нее пометку
        for i in range(1, len(base)):
            if str(call.message.chat.id) == base['user_ID'][i]:
                if not str(base['Рефлексия о курсе'][i]) is None and str(base['Рефлексия о курсе'][i]) != "" and str(base['Рефлексия о курсе'][i]) != " " and req[0] == 'course':
                    base['Рефлексия о курсе'][i] = base['Рефлексия о курсе'][i] + 'course'
                    await jobreload_from_db("Unit", 'Рефлексия о курсе', base['user_ID'][i], base['Рефлексия о курсе'][i] + 'course')
                    await update_parametr_google_sheets('Unit', i + 2, 21, base['Рефлексия о курсе'][i] + 'course')
                elif (str(base['Рефлексия о курсе'][i]) is None or str(base['Рефлексия о курсе'][i]) == "" or str(base['Рефлексия о курсе'][i]) == " ") and req[0] == 'course':
                    base['Рефлексия о курсе'][i] = 'course'
                    await jobreload_from_db("Unit", 'Рефлексия о курсе', base['user_ID'][i], 'course')
                    await update_parametr_google_sheets('Unit', i + 2, 21, 'course')
                if not str(base['Рефлексия о взаимодействии'][i]) is None and str(base['Рефлексия о взаимодействии'][i]) != "" and str(base['Рефлексия о взаимодействии'][i]) != " " and req[0] == 'communic':
                    base['Рефлексия о взаимодействии'][i] = base['Рефлексия о взаимодействии'][i] + 'communic'
                    await jobreload_from_db("Unit", 'Рефлексия о взаимодействии', base['user_ID'][i], base['Рефлексия о взаимодействии'][i] + 'communic')
                    await update_parametr_google_sheets('Unit', i + 2, 22, base['Рефлексия о взаимодействии'][i] + 'communic')
                elif (str(base['Рефлексия о взаимодействии'][i]) is None or str(base['Рефлексия о взаимодействии'][i]) == "" or str(base['Рефлексия о взаимодействии'][i]) == " ") and req[0] == 'communic':
                    base['Рефлексия о взаимодействии'][i] =  'communic'
                    await jobreload_from_db("Unit", 'Рефлексия о взаимодействии', base['user_ID'][i], 'communic')
                    await update_parametr_google_sheets('Unit', i + 2, 22, 'communic')
                if not str(base['Рефлексия общее'][i]) is None and str(base['Рефлексия общее'][i]) != "" and str(base['Рефлексия общее'][i]) != " " and req[0] == 'general':
                    base['Рефлексия общее'][i] = base['Рефлексия общее'][i] + 'general'
                    await jobreload_from_db("Unit", 'Рефлексия общее', base['user_ID'][i], base['Рефлексия общее'][i] + 'general')
                    await update_parametr_google_sheets('Unit', i + 2, 23, base['Рефлексия общее'][i] + 'general')
                elif (str(base['Рефлексия общее'][i]) is None or str(base['Рефлексия общее'][i]) == "" or str(base['Рефлексия общее'][i]) == " ") and req[0] == 'general':
                    base['Рефлексия общее'][i] = 'general'
                    await jobreload_from_db("Unit", 'Рефлексия общее', base['user_ID'][i], 'general')
                    await update_parametr_google_sheets('Unit', i + 2, 23, 'general')
#
#
#
#
    # Если выбранная группа - преподаватель, то
    else:
        base['Группа'][base.index[-1]] = 'Преподаватель'
        await jobreload_from_db("Unit", 'Группа', base['user_ID'][base.index[-1]],  'Преподаватель')
        await update_parametr_google_sheets('Unit', base.index[-1] + 2, 2, 'Преподаватель')
        await botMes.send_message(call.message.chat.id, 'Отлично! Давайте приступим к работе!')
        await botMes.send_message(call.message.chat.id, 'По мере прохождения учебного блока, я буду писать вам о том, кто из учеников уже ознакомился с видео, кто и на какой балл прошел тест,'
                                               'пересылать домашнее задание учеников. В любое время вы можете написать мне, и я передам сообщение всем ученикам персонально. '
                                               'Для этого воспользуйтесь тегом /message Укажате номер группы, которой нужно отправить сообщение, и текст сообщения. '
                                               'Если вы хотите вспомнить, какие теги за что отвечают, то воспользуйтесь тегом /help\n '
                                               'Желаю плодотворной работы!')





if __name__ == '__main__':
    # bot.polling(none_stop=True)
    # Бесконечно запускаем бот и игнорим ошибки
    while True:
        try:
            # ScheduleMessage.start_process()
            executor.start_polling(bot, on_startup=on_startup, timeout=2)
        except:
            pass