from pathlib import Path
from aiogram import Bot
from data.config import BOT_TOKEN


# имя пользователя
DB_USER_NAME = 'root'
# адрес БД
HOST = 'localhost'
# порт БД
PORT = '5432'
# название БД
DATABASE = 'dropbox_tgbot'

# путь до папки с проектом
PROJECT_PATH = Path(__file__).resolve().parent.parent
# путь до папки с загружаемыми юзерами файлами
FILES_PATH = f'{PROJECT_PATH}/local_files'

# бот
BOT = Bot(token=BOT_TOKEN)
