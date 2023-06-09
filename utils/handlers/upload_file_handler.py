import asyncio
from os import remove as os_remove

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from dropbox import Dropbox

from data.constants import BOT, FILES_PATH
from database.db_connect import get_user_api_token
from utils.exceptions.exceptions import NotUploadFile
from utils.state_machines.states import UploadState
from utils.keyboards.keyboard import go_back_kb
from utils.dropbox_api.api_functions import upload_file
from utils.handlers.base_handlers import start_command


async def get_user_file(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(
        text='Отлично, присылай файл, который хочешь загрузить на Dropbox',
        reply_markup=go_back_kb
    )

    await UploadState.local_file_path.set()


async def get_local_path_to_upload(message: Message, state: FSMContext) -> None:
    # получаем инфу об отправленном файле
    sent_file_info = await BOT.get_file(message.document.file_id)
    # получаем файл в байтах (io.BitesIO) по его пути (в тг хранилище)
    sent_file = await BOT.download_file(file_path=sent_file_info['file_path'])

    # получаем расширение отправленного файла и его имя
    file_exten = message.document.file_name.split('.')[-1]
    file_name = '.'.join(message.document.file_name.split('.')[:-1])
    # получаем id пользователя
    chat_id = message.chat.id

    # создаём локальный путь для загруженного файла
    local_file_path = f'{FILES_PATH}/{chat_id}_{file_name}.{file_exten}'
    # записываем байты в локальный файл
    with open(local_file_path, 'wb') as downloaded_file:
        downloaded_file.write(sent_file.getbuffer())

    await message.answer(
        text='''Теперь пришли полный путь до папки на dropbox, в которую хочешь загрузить свой файл.
Например, можно написать так: <b><i>/work/october</i></b>. Тогда по итогу я загружу твой файл в папку <b><i>october</i></b>.
Если нужно загрузить файл в коренную папку, то напиши <b><i>/</i></b>''',
        parse_mode='HTML'
    )

    # сохраняем локальный путь присланного файла в состояние
    await state.update_data(local_file_path=local_file_path)
    await UploadState.dropbox_file_path.set()


async def get_dropbox_path_to_upload(message: Message, state: FSMContext) -> None:
    dropbox_file_path = message.text if message.text != '/' else ''
    # сохраняем путь до папки с файлом в состояние
    await state.update_data(dropbox_file_path=dropbox_file_path)

    state_data = await state.get_data()

    # парсим из локального пути первоначальное имя файла
    local_file_path = state_data.get('local_file_path')
    file_name = '_'.join((local_file_path.split('/')[-1]).split('_')[1:])
    dropbox_path = f'{dropbox_file_path}/{file_name}'

    try:
        api_token = get_user_api_token(tg_id=message.from_user.id)
        dropbox_client = Dropbox(api_token)
        bool_result = upload_file(dropbox_client=dropbox_client, local_file_path=local_file_path, dropbox_file_path=dropbox_path)
        if not bool_result:
            raise NotUploadFile
        await message.answer(
            text='Файл был загружен!',
            reply_markup=None
        )

    except Exception as error:
        await message.answer(
            text='Файл не был загружен! Проверьте, верно ли вы указали папку назначения на dropbox',
            reply_markup=None
        )
        print(f'\n{str(error)}\n')

    finally:
        # удаляем загруженный файл
        os_remove(path=local_file_path)
        asyncio.create_task(start_command(message=message, state=state, exit_from_api_func=True))
