import os.path
import sqlite3 as sq
import pandas as pd
from quickstart import create_table_google_sheets, read_table_google_sheets

async def db_start(): #Создание БД
    global db, cur
    db = sq.connect('reservists.db')
    cur = db.cursor()
    table_name = 'Unit'
    sheet_name = "Unit"
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = cur.fetchone()
    if result is None:
        # data = read_table_google_sheets("Чат-бот встреча", sheet_name)
        data = await read_table_google_sheets("Unit", sheet_name)
        data['user_ID'] = ""
        # data['help_request'] = ""
        data.to_sql(table_name, sq.connect('reservists.db'), index=False)
        # ID = pd.read_excel(os.path.abspath("ID.xlsx"))
        # ID.to_sql("ID", sq.connect('appointment.db'), index=False)
        # IDTM = pd.read_excel(os.path.abspath("IDTM.xlsx"))
        # IDTM.to_sql("IDTM", sq.connect('appointment.db'), index=False)
        # IDTD = pd.read_excel(os.path.abspath("IDTD.xlsx"))
        # IDTD.to_sql("IDTD", sq.connect('appointment.db'), index=False)
        #
        # helpR = pd.DataFrame(columns=['ID_help', 'user_ID', 'text_message'])
        # helpR.to_sql("Help", sq.connect('appointment.db'), index=False)


    # table_name = 'Links'
    # sheet_name = "Links"
    # cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    # result = cur.fetchone()
    # if result is None:
    #     # data = read_table_google_sheets("Чат-бот встреча", sheet_name)
    #     data = await read_table_google_sheets("Бот: встреча", sheet_name)
    #     data.to_sql(table_name, sq.connect('appointment.db'), index=False)
    db.commit()

async def all_table_from_db(table_name_db): #Чтение всей таблицы во фрейм
    df = pd.read_sql(f"SELECT * FROM {table_name_db}", sq.connect('reservists.db'))
    return df

async def rename_start_from_db(table_name_db): #Создаем пометку о необходимости помощи
    sql_update_query = f"""Update {table_name_db} as A set `Даты начала и конца блока` = 'start' where  `Участники курса` = 'start'"""
    # df = pd.read_sql(f"SELECT `Даты начала и конца блока` FROM {table_name_db}", sq.connect('reservists.db'))
    cur.execute(sql_update_query)
    db.commit()
    # return df

async def mailing_from_db(table_name_db, parametr, user_ID): #Создаем пометку о необходимости помощи
    sql_update_query = f"""Update {table_name_db} as A set {parametr} = '' where  `user_ID` = {user_ID}"""
    cur.execute(sql_update_query)
    db.commit()

async def del_person_db(table_name_db, user_ID):
    cur.execute(f"DELETE FROM {table_name_db} WHERE `user_ID` = {user_ID}")
    db.commit()

async def jobreload_from_db(table_name_db, parametr, user_ID, reload): #Создаем пометку о необходимости помощи
    sql_update_query = f"""Update {table_name_db} as A set `{parametr}` = '{reload}' where  `user_ID` = '{user_ID}'"""
    cur.execute(sql_update_query)
    db.commit()

async def new_row_from_db(table_name_db, name, user_ID): #Создаем пометку о необходимости помощи
    sql_update_query = f"""INSERT INTO {table_name_db}(`Участники курса`, `Группа`, `Блок: Начало`, `Даты начала и конца блока`, `Дата`, `Видео`, `Продолжительность (мин)`, `Отметка о просмотре`, `Тест 1`, `Ответ 1`, `Тест 2`, `Ответ 2`, `Тест 3`, `Ответ 3`, `Итого баллов?`, `Отметка о прохождении теста`, `Дата домашнего задания`, `Домашнее задание`, `Отметка об отправке ДЗ`, `Отметка за ДЗ`, `Рефлексия о курсе`, `Рефлексия о взаимодействии`, `Рефлексия общее`, `Комментарий`, `Группы рассылки`, `user_ID`)  VALUES ('{name}', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', {user_ID})"""
    cur.execute(sql_update_query)
    db.commit()

