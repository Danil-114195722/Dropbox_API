import asyncio

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from dropbox import Dropbox

from database.db_connect import get_user_api_token
from utils.exceptions.exceptions import NotFoundDir
from utils.state_machines.states import DirContentState
from utils.keyboards.keyboard import go_back_kb
from utils.dropbox_api.api_functions import get_files_list
from utils.handlers.base_handlers import start_command


async def get_dirname_to_get_content(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(
        text='''Пришли полный путь до папки на dropbox, из которой хочешь получить всё содержимое.
Например, можно написать так: <b><i>/work/october</i></b>. Тогда по итогу я выведу тебе все файлы и папки, содержащиеся в папке <b><i>/work/october</i></b>
Если нужно узнать содержимое коренной папки, то напиши <b><i>/</i></b>''',
        parse_mode='HTML',
        reply_markup=go_back_kb
    )
    await DirContentState.dir_content.set()


async def get_dir_content(message: Message, state: FSMContext) -> None:
    # сохраняем выбранную функцию dropbox
    await state.update_data(dir_content=True)

    try:
        # папка для поиска
        dir_name = message.text if message.text != '/' else ''

        api_token = get_user_api_token(tg_id=message.from_user.id)
        dropbox_client = Dropbox(api_token)
        content_result = get_files_list(dropbox_client=dropbox_client, dropbox_dir_path=dir_name)
        if not content_result:
            raise NotFoundDir

        text = 'Выбранная папка содержит:'
        for content in content_result:
            text += f'\n<b><i>({content[0]}) -- {content[1]}</i></b>'
        await message.answer(
            text=text,
            parse_mode='HTML',
            reply_markup=None
        )

    except Exception as error:
        await message.answer(
            text='''Папка не найдена или не содержит ничего!''',
            reply_markup=None
        )
        print(f'\n{str(error)}\n')
    finally:
        asyncio.create_task(start_command(message=message, state=state, exit_from_api_func=True))
