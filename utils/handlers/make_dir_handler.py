import asyncio

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from dropbox import Dropbox

from database.db_connect import get_user_api_token
from utils.exceptions.exceptions import NotCreateDir
from utils.state_machines.states import CreateDirState
from utils.keyboards.keyboard import go_back_kb
from utils.dropbox_api.api_functions import create_dir
from utils.handlers.base_handlers import start_command


async def get_dropbox_paths_to_create_dir(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(
        text='''Пришли полный путь до новой папки с её названием на dropbox, которую хочешь создать.
Например, можно написать так: <b><i>/work/october/first_week</i></b>. Тогда по итогу я создам папку <b><i>first_week</i></b> в папке <b><i>/work/october</i></b>''',
        parse_mode='HTML',
        reply_markup=go_back_kb
    )

    await CreateDirState.create_dir.set()


async def create_dir_on_dropbox(message: Message, state: FSMContext) -> None:
    # сохраняем выбранную функцию dropbox
    await state.update_data(create_dir=True)

    try:
        # путь до новой папки с её названием
        full_path_to_dir = message.text
        # название папки
        dir_name = full_path_to_dir.split('/')[-1]
        # путь до новой папки
        new_path_to_file = '/'.join(full_path_to_dir.split('/')[:-1]) if full_path_to_dir.replace(dir_name, '') != '/' else ''

        api_token = get_user_api_token(tg_id=message.from_user.id)
        dropbox_client = Dropbox(api_token)
        bool_result = create_dir(dropbox_client=dropbox_client, dropbox_dir_path=new_path_to_file, new_dir_name=dir_name)
        if not bool_result:
            raise NotCreateDir
        await message.answer(
            text='Папка была создана!',
            reply_markup=None
        )

    except Exception as error:
        await message.answer(
            text='''Папка не была создана! Проверьте, верно ли вы указали путь и название для новой папки на dropbox
Возможно, такая папка уже существует на dropbox''',
            reply_markup=None
        )
        print(f'\n{str(error)}\n')
    finally:
        asyncio.create_task(start_command(message=message, state=state, exit_from_api_func=True))
