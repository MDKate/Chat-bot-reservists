import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import df2gspread as d2g
import numpy as np
import pandas as pd

# 'chat.bot.kpi@gmail.com'

async def create_table_google_sheets(table_name):
    # Подсоединение к Google Таблицам
    scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("cbappoitment-5965445a13a2.json", scope)
    client = gspread.authorize(credentials)
    client.create(table_name)


async def create_writer_google_sheets(table_name, email):
    # Подсоединение к Google Таблицам
    scope = ['https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("cbappoitment-5965445a13a2.json", scope)
    client = gspread.authorize(credentials)
    client.open(table_name).share(email, perm_type='user', role='writer')


async def read_table_google_sheets(table_name, sheet_name):
    # Подсоединение к Google Таблицам
    # print(1)
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("cbappoitment-5965445a13a2.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open(table_name).worksheet(sheet_name)
    # print(sheet.get_all_values())
    data = pd.DataFrame(sheet.get_all_values())
    data.columns = np.array(data.iloc[0])
    data = data.reindex(data.index.drop(0))
    # data = data.reindex(data.index.drop(0))
    data.reset_index(drop=True, inplace=True)
    # print(data)
    return data


async def update_table_google_sheets(table_name, sheet_name, out_table):
    # Подсоединение к Google Таблицам
    scope = ['https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("cbappoitment-5965445a13a2.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open(table_name).worksheet(sheet_name)

    set_with_dataframe(sheet, out_table, row=2, include_column_header=True)



async def update_parametr_google_sheets(table_name, row, col, parametr):
    scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('cbappoitment-5965445a13a2.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(table_name).worksheet(table_name)
    sheet.update_cell(row, col, parametr)

async def delete_person_google_sheets(table_name, row_index):
    scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('cbappoitment-5965445a13a2.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(table_name).worksheet(table_name)
    sheet.delete_row(row_index)

async def update_copy_parametr_google_sheets(table_name, base, idM, group):
    scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('cbappoitment-5965445a13a2.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(table_name).worksheet(table_name)

    sheet.update_cell(idM + 2, 2, str(group))
    sheet.update_cell(idM + 2, 3, base['Блок: Начало'][0])
    sheet.update_cell(idM + 2, 5, base['Дата'][0])
    sheet.update_cell(idM + 2, 6, base['Видео'][0])
    sheet.update_cell(idM + 2, 7, base['Продолжительность (мин)'][0])
    sheet.update_cell(idM + 2, 9, base['Тест 1'][0])
    sheet.update_cell(idM + 2, 10, base['Ответ 1'][0])
    sheet.update_cell(idM + 2, 11, base['Тест 2'][0])
    sheet.update_cell(idM + 2, 12, base['Ответ 2'][0])
    sheet.update_cell(idM + 2, 13, base['Тест 3'][0])
    sheet.update_cell(idM + 2, 14, base['Ответ 3'][0])
    sheet.update_cell(idM + 2, 17, base['Дата домашнего задания'][0])
    sheet.update_cell(idM + 2, 18, base['Домашнее задание'][0])

async def perfomance_google_sheets(df):
    scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('cbappoitment-5965445a13a2.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Unit').worksheet('Performance')

    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

