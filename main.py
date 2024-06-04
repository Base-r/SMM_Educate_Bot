# -*- coding: utf-8 -*-
#bot Учитель

import time
from os import getenv
from typing import Any, Dict, Union
from environs import Env
import datetime
from datetime import datetime as dt
from datetime import timedelta
import os, re, html
import aioschedule
from config import *
from finite_state_machine import *
from for_admins import admin_router
# новшество от Груши
from aiogram import F, html as HTML
from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.filters import Command, CommandObject
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message
from aiogram.utils.token import TokenValidationError, validate_token
import asyncio
import logging
from database import *

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery
#свои импорты
# yfghbvfvgfgdfg;ldfg;lkdf;lgkd;lfg


import sys
import asyncio


env = Env()
env.read_env()
TOKEN = env.str('TOKEN')
# All handlers should be attached to the Router (or Dispatcher)
router = Router()
# Инициализация базы данных
init_db()
#add_test_lessons()
#add_test_tarif()
#reg_callback = cd.CallbackData("key","Object","ExecuteCommand")
class Optioncallback(CallbackData, prefix="ob"):
    attr: str
    bool: bool
def is_bot_token(value: str) -> Union[bool, Dict[str, Any]]:
    try:
        validate_token(value)
    except TokenValidationError:
        return False
    return True


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    user_id = message.from_user.id
    referrer = None
    referrer_candidate = ""
    user_id = message.from_user.id
    username = message.from_user.username
    if get_user(user_id):
        text = 'Рады снова вас видеть!'
    else:
        add_user(user_id, username)
        text = 'Это телеграм бот для обучения по курсу "SMM-Старт: Основы эффективного продвижения в социальных сетях"'

    await message.answer(f"Здравствуй, <b>{message.from_user.full_name}!</b>\n"
                         f'{text}',
                        reply_markup=keybrd_na4alo(message.message_id)
                        #finite_state_machine.cmd_menu(finite_state_machine.cmd_keybd('menu_dop', big=True) ),
                        #reply_markup=keybrd_sub4ik(spisok, 'контрагентов', 1, 1, message.message_id))
                         #f"id = {user_id}\n"
                         )
    #await message.answer(
    #        f"<b>Вы не зарегистрированы.</b>\n\n"
    #        f"URL: {HTML.quote('https://t.me/Maxnagus')}\n",
    #        parse_mode='HTML',
    #        reply_markup=finite_state_machine.keyboard_contact())


@router.callback_query(F.data == "da")
async def checkin_confirm(callback: CallbackQuery):
    await callback.answer(
        "Спасибо, подтверждено!",
        show_alert=True
    )

@router.message(Command(commands=["send"]))
@router.message(F.text == "мафия")
async def echo_handler(message: types.Message, bot: Bot) -> None:
    await bot.send_message(message.chat.id,
    f'<a href="https://t.me/buut?start={str(message.from_user.id)}">Mya</a>')

def get_checkin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=InlineKeyboardButton(
    text="Подтвердить", callback_data="confirm"))
    return kb

async def scheduler():
    #aioschedule.every().day.at("15:03").do(otpravkazada4)
    while True:
#        print(aioschedule.jobs)
        await aioschedule.run_pending()
        await asyncio.sleep(10)
async def on_startup(dp: Dispatcher, bot: Bot):

    asyncio.create_task(scheduler())
    try:
        await bot.send_message(maxChat, 'перезапуск бота ' + str(time.strftime("%H:%M", time.localtime())) )

    except:
        pass
    #async def on_startup(dispatcher: Dispatcher, bot: Bot):
    #print(await bot.get_webhook_info())
async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN)
    # включить по дефолту защиту от копирования
    bot.default.protect_content = True
    bot.default.parse_mode = "HTML"
    # добавить роутеры
    dp.include_router(admin_router)
    dp.include_router(router)
    dp.include_router(form_router)
    # And the run events dispatching
    await dp.start_polling(bot)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.create_task(scheduler())
    loop.run_forever()
