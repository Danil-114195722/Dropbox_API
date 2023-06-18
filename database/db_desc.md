### Создание БД:
```
CREATE DATABASE dropbox_tgbot WITH ENCODING "utf-8";
```

### Создание таблицы с хранением telegram id пользователя и его API токеном от Dropbox
```
CREATE TABLE IF NOT EXISTS bot_user (
id SERIAL NOT NULL PRIMARY KEY,
tg_id BIGINT NOT NULL,
api_token VARCHAR(138) NOT NULL);
```
