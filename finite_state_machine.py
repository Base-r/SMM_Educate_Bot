# -*- coding: utf-8 -*-
import asyncio
import datetime
import logging, time
import os
import sys
from os import getenv
from typing import Any, Dict
from glob import glob
from dimpleCalendar import calendar_callback as simple_cal_callback, SimpleCalendar
import csv
from aiogram.methods import TelegramMethod, SendMessage
from config import *
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    InlineKeyboardButton,
    Message, Chat,
    ReplyKeyboardMarkup,CallbackQuery,
    ReplyKeyboardRemove,
    ContentType,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder, ReplyKeyboardBuilder
from itertools import chain
from time import mktime
from database import *
from kassa import *
form_router = Router()

sd = FoobarDB('workers.txt')

knopki = {
    'menu': {'🧮':'Тарифы',#'📆':'Добавить договор',
             '✍️':'Оставить отзыв', '💼':'Личный кабинет'},

    'menu_dop': {'🗞':'Новости',
           '⚙️': 'Настройки', '🧚🏽': 'Помощь'},
    'menu_vse': {'💼':'Заказ', '🗞': 'Новости',
                 '⚙️': 'Настройки', '🧚🏽': 'Помощь'},

    'da': {'🙂':'Да','🙃':'Нет','❌':'Отмена'},
    'next':{'⏭':'Пропустить'},
    'cansel':{'❌':'Отмена'},

    'settings': {
        'Имя': '', 'Адрес': '',
        'Телефон': '', 'Уведомления': True}
    }

class Smm(StatesGroup):
    # состояние оплата
    oplata = State()


class Na4alo(CallbackData, prefix="go"):
    status: str
    msgid : int

class Reg_callback(CallbackData, prefix="lk"):
    status: str
    msgid : int

class Tariff(CallbackData, prefix="tarif"):
    id_: str
    status: str
    msgid : int

class Lesson(CallbackData, prefix="lesson"):
    id_: str
    status:str
    msgid : int


def keybrd_na4alo(msgid):
    markup = InlineKeyboardBuilder()
    msgid = str(msgid)

        #lesson.subtitle = new_subtitle
    markup.row(InlineKeyboardButton(text="Готовы продолжить?",
                                    callback_data=
                                    Na4alo(
                                        status="Готовы начать?",
                                        msgid=msgid
                                    ).pack()
                                    ), width=1
               )
    return markup.as_markup()
def keybrd_tarif(msgid, status):
    markup = InlineKeyboardBuilder()
    msgid = str(msgid)
    tarif = get_aLL_tarifs()
    for item in tarif:
        markup.row(InlineKeyboardButton(text=item.name,
                                    callback_data=
                                    Tariff(
                                        id_=str(item.id),
                                        status=status,
                                        msgid=str(msgid)
                                    ).pack()
                                    ), width=1
               )
    return markup.as_markup()

def keybrd_lesson(msgid, status):
    markup = InlineKeyboardBuilder()
    msgid = str(msgid)
    lesson = get_aLL_lesson()
    #items = Урок()
    for item in lesson:
        markup.row(InlineKeyboardButton(text=item.title + ': ' + item.subtitle,
                                    callback_data=
                                    Lesson(
                                        id_=str(item.id),
                                        status=status,
                                        msgid=str(msgid)
                                    ).pack()
                                    ), width=1
               )
    return markup.as_markup()

def cmd_keybd(menu_txt, big=False):
    try:
        menu = knopki[menu_txt]
    except:
        menu = menu_txt


    keyboard = []
    kb_row = []
    for i, value in enumerate(menu.keys()):
        if big:
            text = value+menu[value]
        else:
            text = value

        kb_row.append(KeyboardButton(text=text))
    keyboard.append(kb_row)

    return keyboard

def cmd_spisok(menu_txt, b=1):
    keyboard = []
    kb_row = []
    for i, value in enumerate(menu_txt):
        if not i & b:
            kb_row = []
        kb_row.append(KeyboardButton(text=value))
        if i & b:
            keyboard.append(kb_row)
    return keyboard
def cmd_menu(keyboard):
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        #input_field_placeholder="это главное меню",
        keyboard=keyboard)

@form_router.callback_query(Na4alo.filter(F.status == "начало"))#, Dokum.EGname)
async def vibor1(call: CallbackQuery, callback_data: Na4alo,state: FSMContext):
    #await call.answer()
    await call.message.edit_text(text=f'Выбирайте наши уроки',
                                 reply_markup=keybrd_tarif(call.message.message_id, "gettar")
                                 # chat_id=call.from_user.id,
                                 # message_id=call.message.message_id
                                 )
@form_router.callback_query(Tariff.filter(F.status == "gettar"))#, Dokum.EGname)
async def vibor2(call: CallbackQuery, callback_data: Tariff, state: FSMContext):
    #await call.answer()
    key = False
    if callback_data.id_ == "1":
        text = f'Выберите один из уроков'
        keybrd = keybrd_lesson(call.message.message_id, "lesson_buy1")

        key = True
    elif callback_data.id_ == "2" or callback_data.id_ == "3":
        tarif1 = get_tarif(int(callback_data.id_))
        sum_pay = tarif1.price
        descrip = tarif1.name
        # как тольк активируем апи юкассы
        #(pay_id, pay_url) = payment_create(sum_pay, descrip)
        await call.message.answer(text='тут будет оплата, а пока. вернемся в начало',
                                     reply_markup=keybrd_tarif(call.message.message_id, "gettar")
                                     # chat_id=call.from_user.id,
                                     # message_id=call.message.message_id
                                     )
        #await call.message.answer(f'Оплата в сумме: {sum_pay} за тариф {descrip}')
        #check = await check_payment(payment_id=pay_id)
        #if check:
        #    if callback_data.id_ == "2":
        #        k = 5
        #    if callback_data.id_ == "3":
        #        k = 6
        #    for ids in range(1, k):
        #        add_available_lesson(call.from_user.id, ids)

        # тут ссылка на покупку курса



    if not key:
        text = 'Этот урок уже не активен, выбирайте другой'
        keybrd = keybrd_tarif(call.message.message_id, "gettar")
    await call.message.edit_text(text=text,
                                 reply_markup=keybrd
                                 # chat_id=call.from_user.id,
                                 # message_id=call.message.message_id
                                 )

@form_router.callback_query(Lesson.filter(F.status == "lesson_buy1"))#, Dokum.EGname)
async def vibor3(call: CallbackQuery, callback_data: Lesson,state: FSMContext):
    print('ok', callback_data.status)
    # выбран базовый
    tarif1 = get_tarif(1)
    sum_pay = tarif1.price
    descrip = tarif1.name
    # как тольк активируем апи юкассы
    #(pay_id, pay_url) = payment_create(sum_pay, descrip)
    await call.message.edit_text(text='тут будет оплата, а пока. вернемся в начало',
                                 reply_markup=keybrd_tarif(call.message.message_id, "gettar")
                                 # chat_id=call.from_user.id,
                                 # message_id=call.message.message_id
                                 )
    await call.message.answer(f'Оплата в сумме: {sum_pay} за тариф {descrip}')
    #check = await check_payment(payment_id=pay_id)
    #if check:
    #    add_available_lesson(call.from_user.id, int(callback_data.id_))









@form_router.message(F.content_type.in_({'text'}))
async def process_anytxt(message: Message, state: FSMContext) -> None:
    if not get_admin(message.chat.id):
        text = 'мы рады что вы вернулись.'
        await message.answer(f"Приветствую, <b>{message.from_user.full_name}!</b>\n"
                             f"{text} Вы готовы приступить к работе?",
                             reply_markup=keybrd_na4alo(message.message_id)
                             )
