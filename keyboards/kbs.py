from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType,
                           WebAppInfo)
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from create_bot import admins
from.kbs_cfg import *

def main_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    kb_list = []
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text=ADMIN_PANEL_TEXT_BTN)])
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )

def admin_kb() -> ReplyKeyboardMarkup:
    kb_list = [
        [KeyboardButton(text=ACTIVE_PALLS_TEXT_BTN)],
        [KeyboardButton(text=NOT_ACTIVE_PALLS_TEXT_BTN)],
        [KeyboardButton(text=CREATE_POLL_TEXT_BTN)],
        [KeyboardButton(text=MAIN_MENU_TEXT_BTN)],
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите действие:"
    )

def save_poll_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=SAVE_TEXT_BTN)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def all_polls_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=ADMIN_PANEL_TEXT_BTN)]],
        resize_keyboard=True,
        input_field_placeholder='Введите название опроса для поиска'
    )

def all_polls_kb(buttons: {str: int}, admin: bool)-> InlineKeyboardMarkup:
    if not admin:
        cb_data = 'user_poll_id_'
    else:
        cb_data = 'poll_id_'
    builder = InlineKeyboardBuilder()
    for b_name, poll_id in buttons.items():
        builder.row(
            InlineKeyboardButton(text=b_name,
                                 callback_data=cb_data + f'{poll_id}')
        )
    return builder.as_markup()

def poll_manage_kb(is_active: bool) -> InlineKeyboardMarkup:
    if is_active:
        text = DEACTIVATE_TEXT_BTN
        cb_data = 'active'
    else:
        text = ACTIVATE_TEXT_BTN
        cb_data = 'not_active'

    kb_list = [
        [InlineKeyboardButton(text=DELETE_TEXT_BTN, callback_data='poll_delete')],
        [InlineKeyboardButton(text=text, callback_data='poll_activate')],
        [InlineKeyboardButton(text=GET_RESULTS_TEXT_BTN, callback_data='get_poll_results')],
        [InlineKeyboardButton(text=POLL_BACK_TEXT_BTN, callback_data=f'back_all_polls_{cb_data}')],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb_list)

def delete_poll_kb(poll_id: int) -> InlineKeyboardMarkup:
    kb_list = [
        [InlineKeyboardButton(text=DELETE_YES_TEXT_BTN, callback_data='delete_poll_yes')],
        [InlineKeyboardButton(text=DELETE_NO_TEXT_BTN, callback_data=f'poll_id_{poll_id}')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb_list)

def user_poll_kb() -> InlineKeyboardMarkup:
    kb_list = [
        [InlineKeyboardButton(text=TAKE_POLL_TEXT_BTN, callback_data='taking_poll')],
        [InlineKeyboardButton(text=POLL_BACK_TEXT_BTN, callback_data='back_all_user_polls')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb_list)

