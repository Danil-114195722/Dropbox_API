import asyncio

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from dropbox import Dropbox

from database.db_connect import get_user_api_token
from utils.exceptions.exceptions import NotTransportFile
from utils.state_machines.states import TransportState
from utils.keyboards.keyboard import go_back_kb
from utils.dropbox_api.api_functions import transport_file
from utils.handlers.base_handlers import start_command


async def get_dropbox_paths_to_transport(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(
        text='''Пришли полный путь до файла на dropbox, который хочешь переместить, и его папку назначения через пробел.
Например, можно написать так: <b><i>/work/october/test_file.txt /work/all</i></b>. Тогда по итогу я перемещу твой файл <b><i>test_file.txt</i></b> из <b><i>/work/october</i></b> в <b><i>/work/all</i></b>''',
        parse_mode='HTML',
        reply_markup=go_back_kb
    )

    await TransportState.transport.set()


async def transport_file_on_dropbox(message: Message, state: FSMContext) -> None:
    # сохраняем выбранную функцию dropbox
    await state.update_data(transport=True)

    try:
        # путь до старого файла с названием и путь до нового файла
        old_path_to_file, new_file_path = message.text.split(' ')
        # путь без имени файла
        file_name = old_path_to_file.split('/')[-1]
        # путь до нового файла
        new_path_to_file = f'{new_file_path if new_file_path != "/" else ""}/{file_name}'

        api_token = get_user_api_token(tg_id=message.from_user.id)
        dropbox_client = Dropbox(api_token)
        bool_result = transport_file(dropbox_client=dropbox_client, old_path_to_file=old_path_to_file, new_path_to_file=new_path_to_file)
        if not bool_result:
            raise NotTransportFile
        await message.answer(
            text='Файл был перемещён!',
            reply_markup=None
        )

    except Exception as error:
        await message.answer(
            text='Файл не был перемещён! Проверьте, верно ли вы указали путь и название файла на dropbox, а также верное название папки назначения',
            reply_markup=None
        )
        print(f'\n{str(error)}\n')
    finally:
        asyncio.create_task(start_command(message=message, state=state, exit_from_api_func=True))
