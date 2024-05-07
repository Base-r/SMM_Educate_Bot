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
import pandas as pd
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


form_router = Router()

sd = FoobarDB('workers.txt')

knopki = {
    'menu': {'🧮':'Добавить счет','📆':'Добавить договор',
             '✍️':'Надо купить', '💼':'Заявка сбыт'},
    'menu_buh': {'🪙':'🪙CSV🪙','🧩':'Вед'},
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
