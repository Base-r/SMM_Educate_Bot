import time
import fnmatch
from aiogram import types
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, MEMBER, KICKED, IS_NOT_MEMBER, ADMINISTRATOR
from aiogram.types import ChatMemberUpdated, ChatMember
from finite_state_machine import *

admin_router = Router()
formattime = '%d.%m.%Y %H:%M'


class Addlesson(StatesGroup):
    # состояние добавления
    urok = State()
    subt = State()
    rename = State()
    v1urok = State()
    v2index = State()
    v3images = State()
    v4text = State()


class AddTariff(StatesGroup):
    rename = State()
    price = State()


@admin_router.message(Command(commands=["admin"]))
@admin_router.message(F.text.contains('🥹'))
async def cmd_test1(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    if get_admin(chat_id):
        await message.answer(
            text=f"Привет! Спасибо, что добавили меня в "
                 f'{message.chat.type} "{message.chat.title}" '
                 f"как администратора. ID чата: {message.chat.id}")
        add_admin(user_id, username)
    if message.from_user.id in adminchat_id or message.chat.id in adminchat_id:
        add_admin(user_id, username)


@admin_router.message(Command(commands=["renameLesson"]))
@admin_router.message(F.text.contains("😃"))
async def add_less(message: Message, state: FSMContext) -> None:
    if get_admin(message.from_user.id) or message.from_user.id in adminchat_id:
        await message.answer(
            "выберите номер урока, который хотите переименовать:",
            reply_markup=keybrd_lesson(message.message_id, 'rename'))


#        await state.update_data(podr="")
@admin_router.callback_query(Lesson.filter(F.status == "rename"))
async def less_rename(call: CallbackQuery, callback_data: Lesson, state: FSMContext):
    print('rename', callback_data.status)
    await call.message.edit_text(text=f'index урока {callback_data.id_} вводите описание')
    await state.set_state(Addlesson.rename)
    await state.update_data(id=callback_data.id_)
    await state.update_data(msgid=call.message.message_id)


@admin_router.message(Addlesson.rename)
async def add_etap(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    update_lesson(int(data['id']), "Урок " + data['id'], message.text)
    await message.answer(
        "переименовано")
    await state.clear()


@admin_router.message(Command(commands=["update_tariff"]))
@admin_router.message(F.text.contains("🤓"))
async def add_tariff(message: Message, state: FSMContext) -> None:
    if get_admin(message.from_user.id) or message.from_user.id in adminchat_id:
        await message.answer(
            "Выберите номер тарифа, который хотите изменить:", reply_markup=keybrd_tarif(message.message_id, 'rename'))


#        await state.update_data(podr="")


@admin_router.callback_query(Tariff.filter(F.status == "rename"))
async def tariff_rename(call: CallbackQuery, callback_data: Tariff, state: FSMContext):
    print('rename', callback_data.status)
    await call.message.edit_text(text=f'Тариф {callback_data.id_} вводите новое название')
    await state.set_state(AddTariff.rename)
    await state.update_data(id=callback_data.id_)
    await state.update_data(msgid=call.message.message_id)


@admin_router.message(AddTariff.rename)
async def tariff_new_price(message: Message, state: FSMContext) -> None:
    print('price')
    await message.answer(text=f'Название тарифа переименовано\\. Введите новую цену: ')
    await state.set_state(AddTariff.price)
    await state.update_data(text=message.text)
    

@admin_router.message(AddTariff.price)
async def update_tariff(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    
    upadate_tariff(int(data['id']), new_name=data['text'], new_price=float(message.text.replace('.',',')))
    await message.answer("Название и цена тарифа успешно обновлены!")
    await state.clear()

# добавить урок командой в боте /addU
# или текстом содержащим смайлик
@admin_router.message(Command(commands=["addU"]))
@admin_router.message(F.text.contains(":)"))
async def add_urok(message: Message, state: FSMContext) -> None:
    if get_admin(message.from_user.id) or message.from_user.id in adminchat_id:
        await message.answer(
            "Напишите название урока:")
        await state.set_state(Addlesson.urok)
            #reply_markup=keybrd_lesson(message.message_id, 'addU'))
@admin_router.message(Addlesson.urok)
async def add_urok1(message: types.Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(Addlesson.subt)
    await message.answer(text=f'описание урока')
@admin_router.message(Addlesson.subt)
async def add_urok2(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    lesson1_id = add_lesson(data['title'], message.text)
    await message.answer(text=f'добавил')

# добавление этапа
@admin_router.message(Command(commands=["adde"]))
@admin_router.message(F.text.contains("😁"))
async def add_etap(message: Message, state: FSMContext) -> None:
    if get_admin(message.from_user.id) or message.from_user.id in adminchat_id:
        await message.answer(
            "выберите один из уроков, куда добавляется этап урока:",
            reply_markup=keybrd_lesson(message.message_id, 'addE'))

#        await state.set_state(Addlesson.v1urok)
@admin_router.callback_query(Lesson.filter(F.status == "addE"))
async def adde_1(call: CallbackQuery, callback_data: Lesson, state: FSMContext):
    await state.set_state(Addlesson.v2index)
    await state.update_data(id=callback_data.id_)
    await state.update_data(msgid=call.message.message_id)
    await call.message.edit_text(text=f'Урок {callback_data.id_} теперь надо указать номер этапа')


@admin_router.message(Addlesson.v2index)
async def photo_handler(message: types.Message, state: FSMContext) -> None:
    await state.update_data(index=message.text)
    await state.set_state(Addlesson.v3images)
    await message.answer(text=f'загружайте фото')


@admin_router.message(F.content_type.in_({'photo'}), Addlesson.v3images)  # , 'sticker'
async def photo_handler(message: types.Message, state: FSMContext) -> None:
    nado = False
    if message.content_type == types.ContentType.PHOTO:
        key = message.photo[-1].file_id
        # file = await bot.get_file(message.photo[-1].file_id)
        # downloaded_file = await bot.download_file(file.file_path)
        # with open('_temp/' + '22.jpg', 'wb') as f:
        #    f.write(downloaded_file.getvalue())
        images = message.photo[-1].file_id + '|' + message.photo[-2].file_id + '|' + message.photo[-3].file_id
        time.sleep(1)
        await state.set_state(Addlesson.v4text)
        await state.update_data(images=images)
        await message.answer(text=f'загружайте текст')


@admin_router.message(Addlesson.v4text)
async def photo_handler4(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    add_stage(урок_id=data['id'],
              index=data['index'],
              images=data['images'],
              lesson_text=message.text,
              lesson_speech=''
              )
    await state.clear()
    await message.answer(text=f'готово, добавить еще жми 😁')



@admin_router.message(Command(commands=["deletestage"]))
@admin_router.message(F.text.contains(":p"))
async def delete_stage(message: Message, state: FSMContext) -> None:
    if get_admin(message.from_user.id) or message.from_user.id in adminchat_id:
        await message.answer(
            "выберите урок, в котором хотите удалить этап:",
            reply_markup=keybrd_lesson(message.message_id, 'deletestage'))
@admin_router.callback_query(Lesson.filter(F.status == "deletestage"))
async def delete_stage1(call: CallbackQuery, callback_data: Lesson, state: FSMContext):
    print(callback_data.status)
    keybrd = keybrd_stage(int(callback_data.id_), call.message.message_id, 'deletestage1')
    if keybrd:
        await call.message.edit_text(
            "выберите этап, который хотите удалить:",
            reply_markup=keybrd)
    else:
        await call.message.edit_text(
            "нету этапов")
@admin_router.callback_query(Lesstage.filter(F.status == "deletestage1"))
async def delete_stage2(call: CallbackQuery, callback_data: Lesstage, state: FSMContext):
    print(callback_data.status)
    delete_lstage(int(callback_data.id_lesson), int(callback_data.id_stage))
    await call.message.edit_text(text=f'этап {callback_data.id_stage} удален')

@admin_router.message(Command(commands=["editlesson"]))
@admin_router.message(F.text.contains(";)"))
async def edit_less(message: Message) -> None:
    if get_admin(message.from_user.id) or message.from_user.id in adminchat_id:
        await message.answer(
            "выберите номер урока, который хотите редактировать:",
            reply_markup=keybrd_lesson(message.message_id, 'editlesson'))

@admin_router.callback_query(Lesson.filter(F.status == "editlesson"))
async def edit_less1(call: CallbackQuery, callback_data: Lesson, state: FSMContext):
    print(callback_data.status)
    await call.message.edit_text(text=f'Урок {callback_data.id_} удален')


@admin_router.message(Command(commands=["deletelesson"]))
@admin_router.message(F.text.contains("🥵"))
async def delete_less(message: Message, state: FSMContext) -> None:
    if get_admin(message.from_user.id) or message.from_user.id in adminchat_id:
        await message.answer(
            "выберите номер урока, который хотите удалить:",
            reply_markup=keybrd_lesson(message.message_id, 'deletelesson'))


@admin_router.callback_query(Lesson.filter(F.status == "deletelesson"))
async def delete_less1(call: CallbackQuery, callback_data: Lesson, state: FSMContext):
    print(callback_data.status)
    delete_lesson(int(callback_data.id_))
    await call.message.edit_text(text=f'Урок {callback_data.id_} удален')

@admin_router.message(Command(commands=["getlesson"]))
@admin_router.message(F.text.contains(":/"))
async def get_less(message: Message, state: FSMContext) -> None:
    if get_admin(message.from_user.id) or message.from_user.id in adminchat_id:
        await otpravka(message)
@admin_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=KICKED)
)
async def user_blocked_bot(event: ChatMemberUpdated):
    key = event.from_user.id
    pole = 'kick'
    value = str(dt.today().strftime(formattime))


@admin_router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=MEMBER)
)
async def user_unblocked_bot(event: ChatMemberUpdated):
    key = event.chat.id
    pole = event.new_chat_member.status
    value = event.from_user.id
    # db.update_one(key=event.from_user.id, pole='newmember', value=str(dt.today().strftime(formattime)))


@admin_router.chat_member(ChatMember)
async def user_unblocked_bot(event: ChatMember):
    key = event.chat.id
    pole = event.status
    value = event.user.id
    # db.update_one(key=event.from_user.id, pole='newmember', value=str(dt.today().strftime(formattime)))
