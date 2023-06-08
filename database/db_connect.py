from sqlalchemy import create_engine, text as sql_text

from data.constants import DB_USER_NAME, DB_USER_PASS, HOST, PORT, DATABASE


# делаем соединение с БД через sqlalchemy
SQL_ENGINE = create_engine(f'postgresql+psycopg2://{DB_USER_NAME}:{DB_USER_PASS}@{HOST}:{PORT}/{DATABASE}')
SQL_CONNECTION = SQL_ENGINE.connect()


def main() -> None:
    pass


if __name__ == '__main__':
    main()
