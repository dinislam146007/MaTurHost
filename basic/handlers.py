from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from keyboards.inline import *


router = Router()

@router.message(CommandStart)
async def start_message(message: Message):
    text = "Добро пожаловать в систему Ma-Tur для собственников и управляющих квартир и апартаментов для посуточной аренды, просим  указать Вы уже наш партнер или нет"
    await message.answer(
        text=text,
        reply_markup=start_inline()
    )


@router.callback_query(F.data.startswith("first"))
async def first(callback: CallbackQuery):
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