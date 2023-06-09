from aiogram.dispatcher.filters.state import State, StatesGroup


# регистрация юзера с API токеном
class RegTokenState(StatesGroup):
    # API токен юзера от dropbox
    token = State()


# обновление API токена юзера
class RefreshTokenState(StatesGroup):
    # API токен юзера от dropbox
    token = State()


# класс состояния для загрузки файла на dropbox
class UploadState(StatesGroup):
    # путь до загруженного файла
    local_file_path = State()
    # путь на dropbox до файла
    dropbox_file_path = State()


# класс состояния для удаления файла из dropbox
class DropState(StatesGroup):
    # путь на dropbox до файла
    dropbox_file_path = State()


# класс состояния для переименования файла на dropbox
class RenameState(StatesGroup):
    # переменная для активации функции переименования
    rename = State()


# класс состояния для перемещения файла на dropbox
class TransportState(StatesGroup):
    # переменная для активации функции переименования
    transport = State()


# класс состояния для создания папки на dropbox
class CreateDirState(StatesGroup):
    # переменная для активации функции переименования
    create_dir = State()


# класс состояния для поиска файла на dropbox
class SearchFileState(StatesGroup):
    # переменная для активации функции переименования
    search_file = State()


# класс состояния для вывода содержимого папки на dropbox
class DirContentState(StatesGroup):
    # переменная для активации функции переименования
    dir_content = State()
