import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import df2gspread as d2g
import numpy as np
import pandas as pd

# 'chat.bot.kpi@gmail.com'

def create_table_google_sheets(table_name):
    # Подсоединение к Google Таблицам
    scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("cbappoitment-5965445a13a2.json", scope)
    client = gspread.authorize(credentials)
    client.create(table_name)


def create_writer_google_sheets(table_name, email):
    # Подсоединение к Google Таблицам
    scope = ['https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("cbappoitment-5965445a13a2.json", scope)
    client = gspread.authorize(credentials)
    client.open(table_name).share(email, perm_type='user', role='writer')

create_table_google_sheets("Unit")
create_writer_google_sheets("Unit", "chat.bot.kpi@gmail.com")