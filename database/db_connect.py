from sqlalchemy import create_engine, text as sql_text
from sqlalchemy.exc import SQLAlchemyError

from data.constants import DB_USER_NAME, DB_USER_PASS, HOST, PORT, DATABASE


# делаем соединение с БД через sqlalchemy
SQL_ENGINE = create_engine(f'postgresql+psycopg2://{DB_USER_NAME}:{DB_USER_PASS}@{HOST}:{PORT}/{DATABASE}')
SQL_CONNECTION = SQL_ENGINE.connect()


# выполнение SQL запроса без отдачи
def exec_without_resp(query: str, printing: bool = False) -> bool:
    alright = False

    # выполняем SQL запрос
    try:
        SQL_CONNECTION.execute(sql_text(query))
        alright = True

        # выводим, что всё ок
        if printing:
            print(f'Query "{query.split()[0]}" OK!')

    # если произошла ошибка
    except SQLAlchemyError as error:
        # выводим ошибку
        if printing:
            print(f'''You've got error in file "db_connect.py" in query "{query.split()[0]}": {error}''')

    return alright


# выполнение SQL запроса с отдачей
def exec_with_resp(query: str, printing: bool = False) -> (bool, list):
    alright = False
    result = []

    # выполняем SQL запрос
    try:
        gotten_info = SQL_CONNECTION.execute(sql_text(query))
        result = gotten_info.fetchall()
        alright = True

        # выводим, что всё ок
        if printing:
            print(f'Query "{query.split()[0]}" OK!')

    # если произошла ошибка
    except SQLAlchemyError as error:
        # выводим ошибку
        if printing:
            print(f'''You've got error in file "db_connect.py" in query "{query.split()[0]}": {error}''')

    return alright, result


# перед работой приложения готовим БД для работы с ним
def prepare_tables():
    # создание таблицы с хранением telegram id пользователя и его API токеном от Dropbox
    create_query = '''CREATE TABLE IF NOT EXISTS bot_user (
id SERIAL NOT NULL PRIMARY KEY,
tg_id INT NOT NULL,
api_token VARCHAR(138) NULL);'''
    exec_without_resp(query=create_query, printing=True)


def main() -> None:
    prepare_tables()


if __name__ == '__main__':
    main()
