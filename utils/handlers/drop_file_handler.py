import asyncio

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from dropbox import Dropbox

from database.db_connect import get_user_api_token
from utils.exceptions.exceptions import NotDropFile
from utils.state_machines.states import DropState
from utils.keyboards.keyboard import go_back_kb
from utils.dropbox_api.api_functions import delete_file
from utils.handlers.base_handlers import start_command


async def get_dropbox_path_to_drop(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(
        text='''Пришли полный путь до файла на dropbox, который хочешь удалить.
Например, можно написать так: <b><i>/work/october/test_file.txt</i></b>. Тогда по итогу я удалю твой файл <b><i>test_file.txt</i></b>''',
        parse_mode='HTML',
        reply_markup=go_back_kb
    )

    await DropState.dropbox_file_path.set()


async def drop_file_from_dropbox(message: Message, state: FSMContext) -> None:
    # сохраняем путь до файла для dropbox
    await state.update_data(dropbox_file_path=message.text)

    state_data = await state.get_data()

    try:
        api_token = get_user_api_token(tg_id=message.from_user.id)
        dropbox_client = Dropbox(api_token)
        bool_result = delete_file(dropbox_client=dropbox_client, dropbox_file_path=state_data.get('dropbox_file_path'))
        if not bool_result:
            raise NotDropFile
        await message.answer(
            text='Файл был удалён!',
            reply_markup=None
        )

    except Exception as error:
        await message.answer(
            text='Файл не был удалён! Проверьте, верно ли вы указали путь и название файла на dropbox',
            reply_markup=None
        )
        print(f'\n{str(error)}\n')

    finally:
        asyncio.create_task(start_command(message=message, state=state, exit_from_api_func=True))
