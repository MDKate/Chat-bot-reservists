from googleapiclient.http import MediaFileUpload
import urllib.request
import os
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

async def upload_to_drive(file_path, filename):
    url = file_path
    # filename = os.path.basename(url)
    urllib.request.urlretrieve(url, filename)
    file_path = os.path.abspath(filename)

    # Инициализация учетных данных
    credentials = Credentials.from_service_account_file('cbappoitment-5965445a13a2.json', scopes=['https://www.googleapis.com/auth/drive'])

    # Создание экземпляра сервиса
    service = build('drive', 'v3', credentials=credentials)

    # Загрузка файла
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': ['1vhOEnqaZ9rSzSlaxUryrKOWf9HrBqoWS']
    }
    media = MediaFileUpload(file_path, mimetype='text/plain')
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()





async def list_folder_to_drive(root_folder_id):
    # Инициализация учетных данных
    credentials = Credentials.from_service_account_file('cbappoitment-5965445a13a2.json', scopes=['https://www.googleapis.com/auth/drive'])

    # Создание экземпляра сервиса
    service = build('drive', 'v3', credentials=credentials)

    # Получить список файлов из папки
    files = service.files().list(q=f"'{root_folder_id}' in parents and trashed=false",
                                 fields='files(id, name)').execute()

    # Преобразовать список файлов в pandas.DataFrame
    df = pd.DataFrame(files['files'])

    return df





