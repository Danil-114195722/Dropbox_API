from aiogram.types import \
    InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, KeyboardButton

all_funcs_kb = InlineKeyboardMarkup(row_width=1)
all_funcs_kb.add(InlineKeyboardButton(text='Загрузка файла на dropbox', callback_data='upload'))
all_funcs_kb.add(InlineKeyboardButton(text='Удаление файла из dropbox', callback_data='remove'))
all_funcs_kb.add(InlineKeyboardButton(text='Переименование файла на dropbox', callback_data='rename'))
all_funcs_kb.add(InlineKeyboardButton(text='Перемещение файла на dropbox', callback_data='transport'))
all_funcs_kb.add(InlineKeyboardButton(text='Создание папки на dropbox', callback_data='create_dir'))
all_funcs_kb.add(InlineKeyboardButton(text='Поиск файла на dropbox по названию', callback_data='search'))
all_funcs_kb.add(InlineKeyboardButton(text='Вывод содержимого папки на dropbox', callback_data='get_content'))

registr_user_kb = InlineKeyboardMarkup(row_width=1)
registr_user_kb.add(InlineKeyboardButton(text='Зарегистрировать API токен', callback_data='registr_user'))

refresh_token_kb = InlineKeyboardMarkup(row_width=1)
refresh_token_kb.add(InlineKeyboardButton(text='Обновить API токен', callback_data='refresh_token'))

go_back_kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
go_back_kb.add(KeyboardButton(text='Вернуться назад'))

