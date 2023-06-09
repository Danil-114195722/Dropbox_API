import asyncio

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from dropbox import Dropbox

from database.db_connect import get_user_api_token
from utils.exceptions.exceptions import NotFoundFile
from utils.state_machines.states import SearchFileState
from utils.keyboards.keyboard import go_back_kb
from utils.dropbox_api.api_functions import full_search_by_name
from utils.handlers.base_handlers import start_command


async def get_filename_to_search_on_dropbox(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(
        text='''Пришли название файла на dropbox, до которого хочешь найти путь.
Например, можно написать так: <b><i>test_file.txt</i></b>. Тогда по итогу я выведу тебе все полные пути до файлов с названием <b><i>test_file.txt</i></b>''',
        parse_mode='HTML',
        reply_markup=go_back_kb
    )
    await SearchFileState.search_file.set()


async def search_file_on_dropbox(message: Message, state: FSMContext) -> None:
    # сохраняем выбранную функцию dropbox
    await state.update_data(search_file=True)

    try:
        # название для поиска
        file_name = message.text

        api_token = get_user_api_token(tg_id=message.from_user.id)
        dropbox_client = Dropbox(api_token)
        search_result = full_search_by_name(dropbox_client=dropbox_client, dropbox_file_name=file_name)
        if not search_result:
            raise NotFoundFile

        text = 'Были найдены следующие файлы:'
        for path in search_result:
            text += f'\n<b><i>{path}</i></b>'
        await message.answer(
            text=text,
            parse_mode='HTML',
            reply_markup=None
        )

    except Exception as error:
        await message.answer(
            text='''Файлов не найдено!''',
            reply_markup=None
        )
        print(f'\n{str(error)}\n')
    finally:
        asyncio.create_task(start_command(message=message, state=state, exit_from_api_func=True))
