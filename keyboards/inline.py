from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_inline():
    kb = [
        [
            InlineKeyboardButton(text='Я ваш партнер', callback_data="first partner"),
            InlineKeyboardButton(text='Я впревые тут', callback_data="first start")
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def first_start():
    kb = [
        [
            InlineKeyboardButton(text='О проекте', url="https://kzntur.ru/excursions/?AGENT_ID=114"),
            InlineKeyboardButton(text='Публичная оферта', url="https://docs.google.com/document/d/1a7mwfFF9jHp_oeSoE222lwz_6tutSnWINNzy_GYmIaI/edit?tab=t.0")
         
         ],
         [InlineKeyboardButton(text="Подать заявку на вступление", callback_data='request')],
         [InlineKeyboardButton(text='Поддержка', url='https://t.me/marat_eps')]

    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def partner_start():
    kb = [
        [InlineKeyboardButton(text='Ваши заказы', callback_data="order")],
        [InlineKeyboardButton(text="Добавить прямой номер клиента", callback_data="add_client_phone")],
        [InlineKeyboardButton(text="Активные услуги", callback_data="active_service")],
        [InlineKeyboardButton(text="Мои квартиры/апартаменты", callback_data="my_host")],
        [InlineKeyboardButton(text="Добавить объект в свою сеть", callback_data="add_apartament")],
        [InlineKeyboardButton(text="Информация о акциях", callback_data='action_inf')],
        [InlineKeyboardButton(text="Заказать выплату", callback_data="make_order")],
        [InlineKeyboardButton(text="Мой QR код", callback_data="my_qr_code")],
        [InlineKeyboardButton(text="Связаться с нами", url="https://t.me/marat_eps")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)