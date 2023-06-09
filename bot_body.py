import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from data.config import API_TOKEN
from data.constants import BOT
from database.db_connect import prepare_tables
from utils.handlers import base_handlers, upload_file_handler, drop_file_handler, rename_file_handler, \
    transport_file_handler, make_dir_handler, search_file_handler, get_dir_content_handler
from utils.state_machines.states import UploadState, DropState, RenameState, TransportState,    \
    CreateDirState, SearchFileState, DirContentState, RegTokenState, RefreshTokenState


# настройка бота и временного хранилища
STORAGE = MemoryStorage()
dispatcher = Dispatcher(bot=BOT, storage=STORAGE)


async def on_startup(disp: Dispatcher) -> None:
    # подготовка БД
    prepare_tables()

    # базовые функции
    disp.register_message_handler(base_handlers.start_command, commands=['start'], state='*')
    disp.register_message_handler(base_handlers.cancel_command, commands=['cancel'], state='*')
    disp.register_message_handler(base_handlers.cancel_command, text='Вернуться назад', state='*')
    disp.register_message_handler(base_handlers.help_command, commands=['help'], state='*')
    # регистрация и обновление API токена
    disp.register_callback_query_handler(base_handlers.reg_api_token, text='registr_user')
    disp.register_message_handler(base_handlers.add_reg_user, state=RegTokenState.token)
    disp.register_callback_query_handler(base_handlers.refresh_api_token, text='refresh_token')
    disp.register_message_handler(base_handlers.change_user_token, state=RefreshTokenState.token)

    # функции для загрузки файла на dropbox
    disp.register_callback_query_handler(upload_file_handler.get_user_file, text='upload')
    disp.register_message_handler(upload_file_handler.get_local_path_to_upload, content_types=['document'], state=UploadState.local_file_path)
    disp.register_message_handler(upload_file_handler.get_dropbox_path_to_upload, state=UploadState.dropbox_file_path)
    # функции для удаления файла из dropbox
    disp.register_callback_query_handler(drop_file_handler.get_dropbox_path_to_drop, text='remove')
    disp.register_message_handler(drop_file_handler.drop_file_from_dropbox, state=DropState.dropbox_file_path)
    # функции для переименования файла на dropbox
    disp.register_callback_query_handler(rename_file_handler.get_dropbox_path_to_rename, text='rename')
    disp.register_message_handler(rename_file_handler.rename_file_from_dropbox, state=RenameState.rename)
    # функции для перемещения файла на dropbox
    disp.register_callback_query_handler(transport_file_handler.get_dropbox_paths_to_transport, text='transport')
    disp.register_message_handler(transport_file_handler.transport_file_on_dropbox, state=TransportState.transport)
    # функции для создания папки на dropbox
    disp.register_callback_query_handler(make_dir_handler.get_dropbox_paths_to_create_dir, text='create_dir')
    disp.register_message_handler(make_dir_handler.create_dir_on_dropbox, state=CreateDirState.create_dir)
    # функции для поиска файлов на dropbox
    disp.register_callback_query_handler(search_file_handler.get_filename_to_search_on_dropbox, text='search')
    disp.register_message_handler(search_file_handler.search_file_on_dropbox, state=SearchFileState.search_file)
    # функции для вывода содержимого папки на dropbox
    disp.register_callback_query_handler(get_dir_content_handler.get_dirname_to_get_content, text='get_content')
    disp.register_message_handler(get_dir_content_handler.get_dir_content, state=DirContentState.dir_content)


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)
