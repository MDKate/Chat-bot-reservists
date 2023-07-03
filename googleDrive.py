from googleapiclient.http import MediaFileUpload
import urllib.request
import os
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





