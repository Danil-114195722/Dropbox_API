import asyncio

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from database.db_connect import get_tg_users_list, add_user, change_api_token
from utils.keyboards.keyboard import all_funcs_kb, registr_user_kb, refresh_token_kb
from utils.state_machines.states import RegTokenState, RefreshTokenState


# проверка пользователя на регистрацию
async def check_reg(message: Message, state: FSMContext, user_id: int) -> bool:
    if user_id not in get_tg_users_list():
        await state.finish()

        await message.answer(
            text='''Привет! Ты ещё не зарегистрировал свой API токен! Для начала нажми на кнопку "Зарегистрировать API токен" и предоставь мне его.
''',
            reply_markup=registr_user_kb
        )
        return False
    return True


async def start_command(message: Message, state: FSMContext, exit_from_api_func: bool = False) -> None:
    await state.finish()

    user_id = message.from_user.id

    check_reg_result = await check_reg(message=message, state=state, user_id=user_id)
    if not check_reg_result:
        return

    if exit_from_api_func:
        await message.answer(
            text='Можешь вводить команду (что-то непонятно - нажми на /help)',
            reply_markup=all_funcs_kb
        )
    else:
        await message.answer(
            text='Ты перезапустил бота! Можешь вводить команду (что-то непонятно - нажми на /help)',
            reply_markup=all_funcs_kb
        )


async def cancel_command(message: Message, state: FSMContext):
    await state.finish()

    user_id = message.from_user.id

    check_reg_result = await check_reg(message=message, state=state, user_id=user_id)
    if not check_reg_result:
        return

    await message.answer(
        text='Ты отменил действие! Можешь вводить команду:',
        reply_markup=all_funcs_kb
    )


async def help_command(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    check_reg_result = await check_reg(message=message, state=state, user_id=user_id)
    if not check_reg_result:
        return

    await message.answer(
        text='''Команда /start -- перезапустить бота
Команда /cancel -- выйти из текущего режима
Команда /help -- вывести это сообщение

У бота есть такие функции:
                * Загрузка файла на dropbox
                * Удаление файла из dropbox
                * Переименование файла на dropbox
                * Перемещение файла на dropbox
                * Создание папки на dropbox
                * Поиск файла на dropbox по названию
                * Вывод содержимого папки на dropbox

Также если вы поменяли API токен, то его можно обновить при помощи кнопки ниже.''',
        reply_markup=refresh_token_kb
    )


async def reg_api_token(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(
        text='''Введи мне свой API токен от Dropbox. Затем я проведу регистрацию, и ты сможешь пользоваться всеми возможностями бота
Вот инструкция по созданию API токена и выдаче прав на просмотр и редактирование файлов Dropbox:

---Создание API ключа---

1) Перейдите на страницу <a href="https://www.dropbox.com/developers/apps?_tk=pilot_lp&_ad=topbar4&_camp=myapps"><i><b>My apps</b></i></a>
2) Выберите <i><b>"Scoped access"</b></i>
3) Выберите <i><b>"Full Dropbox–Access to all files and folders in a user's Dropbox"</b></i>
4) Назовите ваше приложение
5) Поставьте галочку на соглашение с правами
6) Нажмите на кнопку <i><b>"Create app"</b></i>

---Установка разрешений на работу с файлами посредством API---

1) Зайдите в <a href="https://www.dropbox.com/developers/apps"><i><b>консоль разработчика Dropbox</b></i></a>
2) Найдите свое приложение в списке и нажмите на его название
3) Перейдите на вкладку <i><b>"Permissions"</b></i> и найдите раздел <i><b>"Scopes"</b></i>
4) В списке разрешений найдите <i><b>"files.content.write"</b></i>, <i><b>"files.content.read"</b></i> и <i><b>"files.metadata.write"</b></i> и установите галочки напротив этих разрешений
5) Нажмите на кнопку <i><b>"Submit"</b></i> для сохранения изменений''',
        parse_mode='HTML'
    )

    await RegTokenState.token.set()


async def add_reg_user(message: Message, state: FSMContext) -> None:
    api_token = message.text
    # сохраняем API токен в состояние
    await state.update_data(token=api_token)
    user_id = message.from_user.id

    add_user(tg_id=user_id, api_token=api_token)

    await message.answer('Твой API токен был зарегистрирован! Если нужно, то ключ можно обновить (нажми на /help)')

    asyncio.create_task(start_command(message=message, state=state, exit_from_api_func=True))


async def refresh_api_token(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(
        text='''Введи мне свой новый API токен от Dropbox. Затем я обновлю твой существующий токен на новый, и ты так же сможешь пользоваться всеми возможностями бота.
Вот инструкция по созданию API токена и выдаче прав на просмотр и редактирование файлов Dropbox:

---Создание API ключа---

1) Перейдите на страницу <a href="https://www.dropbox.com/developers/apps?_tk=pilot_lp&_ad=topbar4&_camp=myapps"><i><b>My apps</b></i></a>
2) Выберите <i><b>"Scoped access"</b></i>
3) Выберите <i><b>"Full Dropbox–Access to all files and folders in a user's Dropbox"</b></i>
4) Назовите ваше приложение
5) Поставьте галочку на соглашение с правами
6) Нажмите на кнопку <i><b>"Create app"</b></i>

---Установка разрешений на работу с файлами посредством API---

1) Зайдите в <a href="https://www.dropbox.com/developers/apps"><i><b>консоль разработчика Dropbox</b></i></a>
2) Найдите свое приложение в списке и нажмите на его название
3) Перейдите на вкладку <i><b>"Permissions"</b></i> и найдите раздел <i><b>"Scopes"</b></i>
4) В списке разрешений найдите <i><b>"files.content.write"</b></i>, <i><b>"files.content.read"</b></i> и <i><b>"files.metadata.write"</b></i> и установите галочки напротив этих разрешений
5) Нажмите на кнопку <i><b>"Submit"</b></i> для сохранения изменений''',
        parse_mode='HTML'
    )
    await RefreshTokenState.token.set()


async def change_user_token(message: Message, state: FSMContext) -> None:
    api_token = message.text
    # сохраняем API токен в состояние
    await state.update_data(token=api_token)
    user_id = message.from_user.id

    change_api_token(tg_id=user_id, new_api_token=api_token)

    await message.answer('Твой API токен был успешно обновлён!')

    asyncio.create_task(start_command(message=message, state=state, exit_from_api_func=True))

