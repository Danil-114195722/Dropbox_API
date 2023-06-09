from sqlalchemy import create_engine, text as sql_text
from sqlalchemy.exc import SQLAlchemyError

from data.constants import DB_USER_NAME, HOST, PORT, DATABASE
from data.config import DB_USER_PASS


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
api_token VARCHAR(138) NOT NULL);'''
    exec_without_resp(query=create_query, printing=False)


# добавление юзера
def add_user(tg_id: int, api_token: str):
    insert_query = f'''INSERT INTO bot_user (tg_id, api_token) VALUES ({tg_id}, '{api_token}');'''
    exec_without_resp(query=insert_query, printing=False)


# смена API токена
def change_api_token(tg_id: int, new_api_token: str):
    update_query = f'''UPDATE bot_user SET api_token = '{new_api_token}' WHERE tg_id = {tg_id};'''
    exec_without_resp(query=update_query, printing=False)


# получение списка со всеми id зарегистрированных юзеров
def get_tg_users_list() -> list:
    result_list = []
    select_query = 'SELECT tg_id FROM bot_user;'

    dirty_list = exec_with_resp(query=select_query, printing=False)[1]
    for user in dirty_list:
        result_list.append(user[0])

    return result_list


# получение API токена по телеграм id юзера
def get_user_api_token(tg_id: int) -> str:
    select_query = f'SELECT api_token FROM bot_user WHERE tg_id = {tg_id};'
    api_token = exec_with_resp(query=select_query, printing=False)[1][0][0]
    return api_token


def main() -> None:
    # prepare_tables()
    # add_user(tg_id=12345678, api_token='vnjvbnekbgrlsghueghiseliuhy5897yghiesh7w3hf4wg6w4g47evhb4e7gh7485ghwo48')
    # add_user(tg_id=87654321, api_token='cmvdlgje85yuso9483a3phw4fh4eigs5hg7dyh86uroh97ujptd9ijrj5uyhshg57hsoyh7')
    # add_user(tg_id=54637281, api_token='58ylmvfhse8gsh5i7heiohsguiserigohguseo3w9ua2pte5o8u6o8ayf94wpiut95u96uy')

    # change_api_token(tg_id=87654321, new_api_token='mvsldjkgsroghelghriosje8oh5hsueorgj5huap943t039tj93u2pta08p839hfehweufh')

    # print(get_tg_users_list())
    pass


if __name__ == '__main__':
    main()
