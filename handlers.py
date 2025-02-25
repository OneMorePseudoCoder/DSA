
from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from main import bot
import sedo
import data_module
import kb
import text
import subprocess
#import SPD2_download
router = Router()


class UserActions(StatesGroup):
    actions = State()
    menu = State()
    phone_helper = State()
    settings = State()
    base_change = State()
    notification_set = State()


# bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
last_msg_ids = [-1 for i in range(20)]


@router.message(Command("start"))
async def start_handler(msg: Message):
    data_module.chat_checker(msg.from_user.id, msg.chat.id)
    await bot.send_message(msg.from_user.id, "Привет")


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message, state: FSMContext):
    data_module.chat_checker(msg.from_user.id, msg.chat.id)
    await msg.answer(text.menu, reply_markup=kb.menu)
    await state.set_state(UserActions.menu)


@router.callback_query(F.data == "/menu")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text.menu, reply_markup=kb.menu)
    await state.set_state(UserActions.menu)
    await callback.answer(text="Успешно", show_alert=False)
    if last_msg_ids[0] != -1:
        await bot.delete_message(callback.message.chat.id, last_msg_ids[0])
    last_msg_ids[0] = callback.message.message_id
    print(last_msg_ids)


@router.callback_query(F.data == "/phone_helper")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text.phone_helper_main, reply_markup=kb.iexit_kb)
    await state.set_state(UserActions.phone_helper)
    await callback.answer(text="Успешно", show_alert=False)
    if last_msg_ids[1] != -1:
        await bot.delete_message(callback.message.chat.id, last_msg_ids[1])
    last_msg_ids[1] = callback.message.message_id


@router.callback_query(F.data == "/notification_times")
async def set_notifications(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text.notifications_settings_1.format(
        notifics_=data_module.get_notification(callback.from_user.id)
        ), reply_markup=kb.settings_notifics)
    await callback.answer(text="Успешно", show_alert=False)
    if last_msg_ids[2] != -1:
        await bot.delete_message(callback.message.chat.id, last_msg_ids[2])
    last_msg_ids[2] = callback.message.message_id


@router.callback_query(F.data == "/set_notifications")
async def set_notifications(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text.notifications_settings_2, reply_markup=kb.iexit_kb)
    await state.set_state(UserActions.notification_set)
    await callback.answer(text="Успешно", show_alert=False)
    if last_msg_ids[3] != -1:
        await bot.delete_message(callback.message.chat.id, last_msg_ids[3])
    last_msg_ids[3] = callback.message.message_id


@router.message(UserActions.notification_set)
async def start_handler(msg: Message):
    await bot.send_message(chat_id=msg.from_user.id,
                           text=data_module.set_notification(msg.from_user.id, msg.text),
                           reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "/report_brg_moa")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    if data_module.check_admin(callback.from_user.id) == 1:
        await bot.send_message(chat_id=callback.from_user.id,
                               text='Выгрузка запущена, примерное время ожидания 2-4 минуты',
                               reply_markup=kb.iexit_kb)
        await callback.answer(text="Успешно", show_alert=False)
        await callback.message.answer(text=sedo.sogl_report_send(data_module.get_email(callback.from_user.id)),
                                      reply_markup=kb.iexit_kb)
    else:
        await callback.message.answer(text.no_code, reply_markup=kb.iexit_kb)
        await callback.answer(text="Успешно", show_alert=False)
    if last_msg_ids[4] != -1:
        await bot.delete_message(callback.message.chat.id, last_msg_ids[4])
    last_msg_ids[4] = callback.message.message_id


@router.callback_query(F.data == "/sedo")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    print(data_module.check_admin(callback.from_user.id))
    if data_module.check_admin(callback.from_user.id) == 1:
        await callback.message.answer(text='Меню взаимодействия с СЭДО', reply_markup=kb.sedo_adm_kb)
    else:
        await callback.message.answer(text.no_code, reply_markup=kb.iexit_kb)
    await callback.answer(text="Успешно", show_alert=False)
    if last_msg_ids[5] != -1:
        await bot.delete_message(callback.message.chat.id, last_msg_ids[5])
    last_msg_ids[5] = callback.message.message_id


@router.message(UserActions.phone_helper, F.text == 'Арсеньев')
async def start_handler(msg: Message, state: FSMContext):
    await msg.answer('Это мой создатель')
    data_module.chat_checker(msg.from_user.id, msg.chat.id)
    await msg.answer(str(data_module.search(msg.text, msg.from_user.id)), reply_markup=kb.iexit_kb)
    await state.set_state(UserActions.phone_helper)


@router.message(UserActions.phone_helper, F.text)
async def start_handler(msg: Message, state: FSMContext):
    print(msg.text)
    # result = data_module.search(msg.text, msg.from_user.id)
    data_module.chat_checker(msg.from_user.id, msg.chat.id)
    await msg.answer(str(data_module.search(msg.text, msg.from_user.id)), reply_markup=kb.iexit_kb)
    await state.set_state(UserActions.phone_helper)


@router.message(F.text == "отправь сообщение")
async def menu(bot: bot):
    await bot.send_message(chat_id=309025156, text='<b>напиши мне что-нибудь</b>')


@router.callback_query(F.data == "/settings")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    print(callback.from_user.id)
    print(data_module.check_admin(callback.from_user.id))
    await state.set_state(UserActions.settings)
    await callback.message.answer(text.settings, reply_markup=kb.settings)
    await callback.answer(text="Успешно", show_alert=False)
    if last_msg_ids[6] != -1:
        await bot.delete_message(callback.message.chat.id, last_msg_ids[6])
    last_msg_ids[6] = callback.message.message_id


@router.callback_query(F.data == "/base_change")
async def helper_status(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserActions.base_change)
    await callback.message.answer(text.upd_text, reply_markup=kb.iexit_kb)
    await callback.answer(text="Успешно", show_alert=False)
    if last_msg_ids[7] != -1:
        await bot.delete_message(callback.message.chat.id, last_msg_ids[7])
    last_msg_ids[7] = callback.message.message_id


@router.message(UserActions.base_change, F.text)
async def start_handler(msg: Message):
    print(msg.text)
    data = msg.text.split('::')
    cols = data[1].split(', ')
    print(cols)
    vals = data[2].split(', ')
    print(vals)
    # result = data_module.search(msg.text, msg.from_user.id)
    data_module.chat_checker(msg.from_user.id, msg.chat.id)
    await msg.answer(str(data_module.update_table(data[0], cols, vals, data[3], data[4], msg.from_user.id)),
                     reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "/start_red_control")
async def red_control(callback: types.CallbackQuery):
    await callback.message.answer("Запускаю Красный и предупредительный контроль\nОжидайте минут 15 и проверьте почту",
                                  reply_markup=kb.iexit_kb)
    await callback.answer(text="Успешно", show_alert=False)
    proc = subprocess.Popen(['python', r'C:\Users\ArsenevVD\Desktop\control_mail_2.0\red_control.py'])
    if last_msg_ids[8] != -1:
        await bot.delete_message(callback.message.chat.id, last_msg_ids[8])
    last_msg_ids[8] = callback.message.message_id


@router.callback_query(F.data == "/start_control_mail")
async def red_control(callback: types.CallbackQuery):
    await callback.message.answer("Контроль писем запущен\nОжидайте минут 20 и проверьте почту",
                                  reply_markup=kb.iexit_kb)
    await callback.answer(text="Успешно", show_alert=False)
    proc = subprocess.Popen(['python', r'C:\Users\ArsenevVD\Desktop\control_mail_2.0\part2.py'])
    if last_msg_ids[9] != -1:
        await bot.delete_message(callback.message.chat.id, last_msg_ids[9])
    last_msg_ids[9] = callback.message.message_id


@router.callback_query(F.data == "/spd_2_download")
async def spd_2(callback: types.CallbackQuery):
    await callback.message.answer("Выгрузка запущена, ожидайте выгруку на электронной почте (10-15 минут)",
                                  reply_markup=kb.iexit_kb)
    await callback.answer(text="Успешно", show_alert=False)
#    await callback.message.answer(text=SPD2_download.spd_2_download(data_module.get_email(callback.from_user.id)),                          --- Потом вернуть как было!!!
#                                  reply_markup=kb.iexit_kb)
    if last_msg_ids[10] != -1:
        await bot.delete_message(callback.message.chat.id, last_msg_ids[10])
    last_msg_ids[10] = callback.message.message_id


@router.message(F.text)
async def unknown_msg(msg: Message):
    await msg.answer(text.unknown_msg, reply_markup=kb.iexit_kb)
