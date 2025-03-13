from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from keyboards.inline import *
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
# from config import config
import database.db as db
from aiogram.filters.callback_data import CallbackData
from aiogram.filters.state import StateFilter





router_admin = Router()

class PromotionStates(StatesGroup):
    adding_promotion_title = State()
    adding_promotion_description = State()


@router_admin.callback_query(F.data.startswith("ver"))
async def verification_user(callback: CallbackQuery, state: FSMContext, bot: Bot):
    action = callback.data.split()[1]
    user_id = int(callback.data.split()[2])
    if action == "yes":
        await db.verification_host(user_id)
        await bot.send_message(
            text="Вы успешно верифицировали",
            chat_id=user_id
        )

    else:
        await bot.send_message(
            text="Вам отказали в верификации",
            chat_id=user_id
        )
    await callback.message.edit_reply_markup(
        reply_markup=edit_chat_ver(action)
    )
        

@router_admin.callback_query(F.data.startswith('admin'))
async def admin(callback: CallbackQuery):
    action = callback.data.split()[1]
    if action == "start":
        await callback.message.edit_reply_markup(
            reply_markup=admin_inline()
        )

class AddServiceState(StatesGroup):
    city = State()         # Состояние для города
    description = State()  # Состояние для описания услуги

# Маршрутизатор для обработки добавления услуги
@router_admin.callback_query(F.data == "service_add")
async def start_service_addition(callback: CallbackQuery, state: FSMContext):
    # Удаляем сообщение бота
    if callback.message:
        await callback.message.delete()
    
    # Переход в состояние ввода города
    await state.set_state(AddServiceState.city)
    message = await callback.message.answer("Введите город для услуги:")
    await state.update_data(last_bot_message=message.message_id)

@router_admin.message(AddServiceState.city)
async def set_service_city(message: Message, state: FSMContext):
    # Удаляем предыдущие сообщения бота
    data = await state.get_data()
    last_bot_message_id = data.get("last_bot_message")
    if last_bot_message_id:
        try:
            await message.bot.delete_message(message.chat.id, last_bot_message_id)
        except:
            pass

    # Сохраняем город и переходим к следующему шагу
    await state.update_data(city=message.text)
    response = await message.answer("Введите описание услуги:")
    await state.set_state(AddServiceState.description)
    await state.update_data(last_bot_message=response.message_id)

@router_admin.message(AddServiceState.description)
async def set_service_description(message: Message, state: FSMContext):
    # Удаляем предыдущее сообщение бота
    data = await state.get_data()
    last_bot_message_id = data.get("last_bot_message")
    if last_bot_message_id:
        try:
            await message.bot.delete_message(message.chat.id, last_bot_message_id)
        except:
            pass

    # Сохраняем описание услуги
    service_data = await state.get_data()
    city = service_data.get("city")
    description = message.text
    # await db.create_services_table()

    # Сохраняем услугу в БД
    await db.add_service(message.from_user.id, city, description)
    # Завершаем FSM и отправляем подтверждение
    await state.clear()
    await message.answer("Услуга успешно добавлена!")

@router_admin.callback_query(F.data == "information_add")
async def add_information(callback: CallbackQuery, state: FSMContext):
    await db.create_promotions_table()
    await callback.message.answer("Введите название акции:")
    await state.set_state(PromotionStates.adding_promotion_title)

@router_admin.message(StateFilter(PromotionStates.adding_promotion_title))
async def get_promotion_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Теперь введите описание акции:")
    await state.set_state(PromotionStates.adding_promotion_description)

@router_admin.message(StateFilter(PromotionStates.adding_promotion_description))
async def get_promotion_description(message: Message, state: FSMContext):
    data = await state.get_data()
    title = data['title']
    description = message.text

    await db.add_promotion(title, description)
    await message.answer("Акция успешно добавлена!")
    await state.clear()


ITEMS_PER_PAGE = 1

@router_admin.callback_query(F.data.startswith("information_view"))
async def admin_view_promotions(callback: CallbackQuery):
    # Получаем текущую страницу
    page = int(callback.data.split()[1])

    # Считаем общее количество акций
    total_items = await db.count_promotions()
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    # Получаем список акций для текущей страницы
    promotions = await db.get_promotions(offset=(page - 1) * ITEMS_PER_PAGE, limit=ITEMS_PER_PAGE)

    # Формируем текст для сообщения
    text = f"Акции (стр. {page}/{total_pages}):\n\n"
    for promo in promotions:
        text += f"📌 {promo['title']}\n{promo['description']}\n\n"

    # Создаем клавиатуру
    promotion_id = promotions[0]['id'] if promotions else 0
    keyboard = generate_admin_keyboard(page, total_pages)

    # Добавляем кнопку "Удалить" для каждой акции
    for promo in promotions:
        delete_button = InlineKeyboardButton(
            text="❌ Удалить",
            callback_data=f"delete_{promo['id']}"  # Корректный формат callback_data
        )
        keyboard.inline_keyboard.append([delete_button])  # Добавляем кнопку в клавиатуру

    # Обновляем сообщение
    await callback.message.edit_text(text, reply_markup=keyboard)

def generate_admin_keyboard(current_page: int, total_pages: int):
    # Создаем пустой список для кнопок
    keyboard = []

    # Если есть предыдущая страница, добавляем кнопку "Назад"
    if current_page > 1:
        keyboard.append([
            InlineKeyboardButton(
                text="⬅ Назад",  # Используем корректный параметр `text`
                callback_data=f"information_view {current_page - 1}"  # Корректный параметр `callback_data`
            )
        ])

    # Если есть следующая страница, добавляем кнопку "Вперед"
    if current_page < total_pages:
        keyboard.append([
            InlineKeyboardButton(
                text="Вперед ➡",  # Используем корректный параметр `text`
                callback_data=f"information_view {current_page + 1}"  # Корректный параметр `callback_data`
            )
        ])

    # Возвращаем объект InlineKeyboardMarkup
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
@router_admin.callback_query(F.data.startswith("delete_"))
async def delete_promotion_handler(callback: CallbackQuery):
    # Извлекаем ID акции из callback_data
    promotion_id = int(callback.data[len("delete_"):])

    try:
        # Удаляем акцию
        await db.delete_promotion(promotion_id)

        # Уведомляем пользователя
        await callback.answer("Акция удалена.", show_alert=True)

        # Обновляем список акций после удаления
        await admin_view_promotions(callback)

    except Exception as e:
        # Отправляем сообщение об ошибке
        await callback.answer(f"Ошибка при удалении: {str(e)}", show_alert=True)
