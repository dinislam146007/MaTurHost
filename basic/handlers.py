from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.inline import *
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData
from aiogram.filters.state import State, StatesGroup
# from config import config
import database.db as db

ITEMS_PER_PAGE=1

router = Router()

class SendRequest(StatesGroup):
    phone = State()
    fio = State()

class SendRequestClient(StatesGroup):
    phone = State()
    fio = State()

class AddApartament(StatesGroup):
    city = State()
    address = State()
    apartment = State()
    wifi_login = State()
    wifi_password = State()

# CallbackData для обработки пагинации
class PaginationCallback(CallbackData, prefix="paginate"):
    action: str  # Действие (prev, next)
    page: int    # Номер текущей страницы



@router.message(Command(commands=["start"]))
async def start_message(message: Message):
    if db.get_host(message.from_user.id):
        text = "Добро пожаловать в систему Ma-Tur для собственников и управляющих квартир и апартаментов для посуточной аренды"
        await message.answer(
            text=text,
            reply_markup=partner_start()
        )
    else:
        text = "Добро пожаловать в систему Ma-Tur для собственников и управляющих квартир и апартаментов для посуточной аренды"
        await message.answer(
            text=text,
            reply_markup=first_start()
        )



@router.callback_query(F.data.startswith("first"))
async def first(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
    except Exception:
        pass
    action = callback.data.split()[1]
    if action == "partner":
        await callback.message.edit_text(
            text="Текст для партнера", 
            reply_markup=partner_start()
        )
    elif action == "start":
        await callback.message.edit_text(
            text='Текст', 
            reply_markup=first_start()
        )

@router.callback_query(F.data == "request")
async def send_request(callback: CallbackQuery, state: FSMContext):
    msg = await callback.message.edit_text(
        text="Введите ФИО",
        reply_markup=close_state('first start')
    )
    await state.set_state(SendRequest.fio)
    await state.update_data(last_msg=msg.message_id)

@router.message(SendRequest.fio)
async def send_request_fio(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(fio=message.text)
    data = await state.get_data()
    try:
        await bot.delete_message(message_id=data['last_msg'], chat_id=message.from_user.id)
    except Exception:
        pass
    msg = await message.answer("Введите ваш телефон", reply_markup=close_state('first start'))
    await state.set_state(SendRequest.phone)
    await state.update_data(last_msg=msg.message_id)

@router.message(SendRequest.phone)
async def send_request_phone(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    try:
        await bot.delete_message(message_id=data['last_msg'], chat_id=message.from_user.id)
    except Exception:
        pass
    msg = await message.answer("Ваши данные успешно отправлены, ждите ответа от администратора.", reply_markup=back_to_menu('first start'))
    await state.clear()
    text = "Новая заявка\n\n"
    text += f"ФИО: {data['fio']}\n"
    text += f"Телефон: {data['phone']}"
    await db.set_host(message.from_user.id, data['fio'], data['phone'])
    await bot.send_message(
        text=text,
        chat_id=-1002393597256,
        reply_markup=verification_inline(message.from_user.id)
    )


    


@router.callback_query(F.data == "add_client_phone")
async def add_client_phone(callback: CallbackQuery, state: FSMContext,bot:Bot):
    msg = await callback.message.edit_text(
        text="Введите имя клиента",
        reply_markup=close_state('first partner')
    )
    await state.set_state(SendRequestClient.fio)
    await state.update_data(last_msg=msg.message_id)

@router.message(SendRequestClient.fio)
async def send_request_fio(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(fio=message.text)
    data = await state.get_data()
    try:
        await bot.delete_message(message_id=data['last_msg'], chat_id=message.from_user.id)
    except Exception:
        pass
    msg = await message.answer("Введите ваш телефон", reply_markup=close_state('first start'))
    await state.set_state(SendRequestClient.phone)
    await state.update_data(last_msg=msg.message_id)

@router.message(SendRequestClient.phone)
async def send_request_phone(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    try:
        await bot.delete_message(message_id=data['last_msg'], chat_id=message.from_user.id)
    except Exception:
        pass
    msg = await message.answer("Данные успешно отправлены!", reply_markup=back_to_menu('first partner'))
    await state.clear()
    host = await db.get_host(message.from_user.id)
    text = "Прямой номер клиента\n\n"
    text += f"ФИО: {data['fio']}\n"
    text += f"Телефон: {data['phone']}\n\n"
    text += f"ФИО хоста: {host['fio']}\n"
    text += f"Телефон хоста: {host['phone']}\n"
    text += f"TG username: @{message.from_user.username}\n"


    # await db.set_host(message.from_user.id, data['fio'], data['phone'])
    await bot.send_message(
        text=text,
        chat_id=-1002393597256,
        # reply_markup=verification_inline(message.from_user.id)
    )



# Обработчик для callback_data "add_apartament"
@router.callback_query(F.data == "add_apartament")
async def start_add_apartament(callback: CallbackQuery, state: FSMContext):
    msg = await callback.message.edit_text(
        text="Введите город",
        reply_markup=close_state('first start')
    )
    await state.set_state(AddApartament.city)
    await state.update_data(last_msg=msg.message_id)

@router.message(AddApartament.city)
async def add_apartament_city(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(city=message.text)
    data = await state.get_data()
    try:
        await bot.delete_message(message_id=data['last_msg'], chat_id=message.from_user.id)
    except Exception:
        pass
    msg = await message.answer("Введите адрес", reply_markup=close_state('first start'))
    await state.set_state(AddApartament.address)
    await state.update_data(last_msg=msg.message_id)

@router.message(AddApartament.address)
async def add_apartament_address(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(address=message.text)
    data = await state.get_data()
    try:
        await bot.delete_message(message_id=data['last_msg'], chat_id=message.from_user.id)
    except Exception:
        pass
    msg = await message.answer("Введите номер квартиры", reply_markup=close_state('first start'))
    await state.set_state(AddApartament.apartment)
    await state.update_data(last_msg=msg.message_id)

@router.message(AddApartament.apartment)
async def add_apartament_apartment(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(apartment=message.text)
    data = await state.get_data()
    try:
        await bot.delete_message(message_id=data['last_msg'], chat_id=message.from_user.id)
    except Exception:
        pass
    msg = await message.answer("Введите логин Wi-Fi", reply_markup=close_state('first start'))
    await state.set_state(AddApartament.wifi_login)
    await state.update_data(last_msg=msg.message_id)

@router.message(AddApartament.wifi_login)
async def add_apartament_wifi_login(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(wifi_login=message.text)
    data = await state.get_data()
    try:
        await bot.delete_message(message_id=data['last_msg'], chat_id=message.from_user.id)
    except Exception:
        pass
    msg = await message.answer("Введите пароль Wi-Fi", reply_markup=close_state('first start'))
    await state.set_state(AddApartament.wifi_password)
    await state.update_data(last_msg=msg.message_id)

@router.message(AddApartament.wifi_password)
async def add_apartament_wifi_password(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(wifi_password=message.text)
    data = await state.get_data()
    try:
        await bot.delete_message(message_id=data['last_msg'], chat_id=message.from_user.id)
    except Exception:
        pass

    # Добавление данных в базу
    user_id = message.from_user.id
    # await db.create_apartament_table()
    await db.add_apartament(
        user_id=user_id,
        city=data['city'],
        address=data['address'],
        apartment=data['apartment'],
        wifi_login=data['wifi_login'],
        wifi_password=data['wifi_password']
    )

    await message.answer("Объект успешно добавлен в сеть.")
    await state.clear()

@router.callback_query(F.data == "my_host")
async def show_my_apartments(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    apartments = await db.get_apartaments(user_id)

    if not apartments:
        await callback.message.edit_text("У вас нет добавленных объектов.", reply_markup=close_state('first start'))
        return

    await state.update_data(apartments=apartments, current_index=0)
    await show_apartment(callback, state)

async def show_apartment(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    apartments = data['apartments']
    current_index = data['current_index']

    apartment = apartments[current_index]
    text = (
        f"<b>Город:</b> {apartment['city']}\n"
        f"<b>Адрес:</b> {apartment['address']}\n"
        f"<b>Квартира:</b> {apartment['apartment']}\n"
        f"<b>Wi-Fi логин:</b> {apartment['wifi_login']}\n"
        f"<b>Wi-Fi пароль:</b> {apartment['wifi_password']}\n\n"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{current_index + 1} из {len(apartments)}",callback_data="fff")],
        [
            InlineKeyboardButton(
                text="⬅️ Назад", callback_data="previous_apartment"
            ),
            InlineKeyboardButton(
                text="Вперёд ➡️", callback_data="next_apartment"
            )
        ],
        [InlineKeyboardButton(text="Закрыть", callback_data="close")]
    ])

    await callback.message.edit_text(text, reply_markup=keyboard)

@router.callback_query(F.data == "previous_apartment")
async def previous_apartment(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_index = data['current_index']

    if current_index > 0:
        current_index -= 1
        await state.update_data(current_index=current_index)
        await show_apartment(callback, state)

@router.callback_query(F.data == "next_apartment")
async def next_apartment(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_index = data['current_index']
    apartments = data['apartments']

    if current_index < len(apartments) - 1:
        current_index += 1
        await state.update_data(current_index=current_index)
        await show_apartment(callback, state)

@router.callback_query(F.data == "close")
async def close_apartments(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Просмотр объектов завершён.", reply_markup=close_state('first start'))
    await state.clear()


def generate_pagination_keyboard(current_page: int, total_pages: int):
    keyboard = []

    # Кнопки пагинации
    pagination_buttons = []
    if current_page > 1:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="⬅ Назад",
                callback_data=PaginationCallback(action="prev", page=current_page - 1).pack()
            )
        )
    if current_page < total_pages:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="Вперед ➡",
                callback_data=PaginationCallback(action="next", page=current_page + 1).pack()
            )
        )
    
    # Добавляем кнопки пагинации в клавиатуру, если они есть
    if pagination_buttons:
        keyboard.append(pagination_buttons)

    # Кнопка "🔙 Назад"
    keyboard.append([
        InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="first partner"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Хендлер для кнопки "Активные услуги"
@router.callback_query(F.data == "active_service")
async def show_active_services(callback: CallbackQuery):
    user_id = callback.from_user.id
    page = 1  # Начинаем с первой страницы

        # Получаем общее количество услуг
    total_services = await db.count_services(user_id)
    total_pages = (total_services + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    # Получаем услуги для текущей страницы
    services = await db.get_services(user_id, offset=(page - 1) * ITEMS_PER_PAGE, limit=ITEMS_PER_PAGE)

    if not services:
        await callback.message.answer("У вас пока нет активных услуг.")
        return

    # Формируем текст с услугами
    text = f"Активные услуги (стр. {page}/{total_pages}):\n\n"
    for service in services:
        text += f"🏙 Город: {service['city']}\n📋 Описание: {service['description']}\n\n"

    # Клавиатура для навигации
    keyboard = generate_pagination_keyboard(current_page=page, total_pages=total_pages)

    # Отправляем сообщение
    if callback.message:
        await callback.message.edit_text(text, reply_markup=keyboard)

# Хендлер для обработки пагинации
@router.callback_query(PaginationCallback.filter())
async def paginate_services(callback: CallbackQuery, callback_data: PaginationCallback):
    user_id = callback.from_user.id
    page = callback_data.page  # Текущая страница

        # Получаем общее количество услуг
    total_services = await db.count_services(user_id)
    total_pages = (total_services + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    # Получаем услуги для текущей страницы
    services = await db.get_services(user_id, offset=(page - 1) * ITEMS_PER_PAGE, limit=ITEMS_PER_PAGE)

    # Формируем текст с услугами
    text = f"Активные услуги (стр. {page}/{total_pages}):\n\n"
    for service in services:
        text += f"🏙 Город: {service['city']}\n📋 Описание: {service['description']}\n\n"

    # Клавиатура для навигации
    keyboard = generate_pagination_keyboard(current_page=page, total_pages=total_pages)

    # Обновляем сообщение
    if callback.message:
        await callback.message.edit_text(text, reply_markup=keyboard)

@router.callback_query(F.data == "action_inf")
async def user_view_promotions(callback: CallbackQuery):
    page = 1
    total_items = await db.count_promotions()
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    promotions = await db.get_promotions(offset=(page - 1) * ITEMS_PER_PAGE, limit=ITEMS_PER_PAGE)

    text = f"Акции (стр. {page}/{total_pages}):\n\n"
    for promo in promotions:
        text += f"📌 {promo['title']}\n{promo['description']}\n\n"

    keyboard = generate_user_keyboard(page, total_pages)

    await callback.message.edit_text(text, reply_markup=keyboard)

def generate_user_keyboard(current_page: int, total_pages: int):
    keyboard = []

    if current_page > 1:
        keyboard.append([
            InlineKeyboardButton("⬅ Назад", callback_data=f"user_prev_{current_page - 1}")
        ])
    if current_page < total_pages:
        keyboard.append([
            InlineKeyboardButton("Вперед ➡", callback_data=f"user_next_{current_page + 1}")
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
