import asyncio

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from dropbox import Dropbox

from database.db_connect import get_user_api_token
from utils.exceptions.exceptions import NotRenameFile
from utils.state_machines.states import RenameState
from utils.keyboards.keyboard import go_back_kb
from utils.dropbox_api.api_functions import rename_file
from utils.handlers.base_handlers import start_command


async def get_dropbox_path_to_rename(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(
        text='''Пришли полный путь до файла на dropbox, который хочешь переименовать, и его новое имя через пробел.
Например, можно написать так: <b><i>/work/october/test_file.txt new_name.txt</i></b>. Тогда по итогу я переименую твой файл <b><i>test_file.txt</i></b> на <b><i>new_name.txt</i></b>''',
        parse_mode='HTML',
        reply_markup=go_back_kb
    )

    await RenameState.rename.set()


async def rename_file_from_dropbox(message: Message, state: FSMContext) -> None:
    # сохраняем выбранную функцию dropbox
    await state.update_data(rename=True)

    try:
        # путь до старого файла и название нового
        old_file_path, new_file_name = message.text.split(' ')
        # путь без имени файла
        file_path = '/'.join(old_file_path.split('/')[:-1]) if old_file_path else ''
        # путь до нового файла
        new_file_path = f'{file_path}/{new_file_name}'

        api_token = get_user_api_token(tg_id=message.from_user.id)
        dropbox_client = Dropbox(api_token)
        bool_result = rename_file(dropbox_client=dropbox_client, old_file_path=old_file_path, new_file_path=new_file_path)
        if not bool_result:
            raise NotRenameFile
        await message.answer(
            text='Файл был переименован!',
            reply_markup=None
        )

    except Exception as error:
        await message.answer(
            text='Файл не был переименован! Проверьте, верно ли вы указали путь и название файла на dropbox, а также новое название',
            reply_markup=None
        )
        print(f'\n{str(error)}\n')
    finally:
        asyncio.create_task(start_command(message=message, state=state, exit_from_api_func=True))
