from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton, InlineKeyboardMarkup)
from create_bot import admins
import keyboards.kbs_cfg as cfg


def main_kb(user_telegram_id: int) -> ReplyKeyboardMarkup:
    """
    Create a main menu keyboard.

    :param user_telegram_id: User telegram ID.
    :return: Main menu keyboard.
    """
    kb_list = []
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text=cfg.ADMIN_PANEL_TEXT_BTN)])
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )


def admin_kb() -> ReplyKeyboardMarkup:
    """
    Create an admin panel keyboard.

    :return: Admin panel keyboard.
    """
    kb_list = [
        [KeyboardButton(text=cfg.ACTIVE_PALLS_TEXT_BTN)],
        [KeyboardButton(text=cfg.NOT_ACTIVE_PALLS_TEXT_BTN)],
        [KeyboardButton(text=cfg.CREATE_POLL_TEXT_BTN)],
        [KeyboardButton(text=cfg.MAIN_MENU_TEXT_BTN)],
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите действие:"
    )


def save_poll_kb() -> ReplyKeyboardMarkup:
    """
    Create a keyboard to save the poll.

    :return: Save poll keyboard.
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=cfg.SAVE_TEXT_BTN)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def all_polls_menu_kb() -> ReplyKeyboardMarkup:
    """
    Create a keyboard that allows you to return to the admin panel.

    :return: Return to the admin panel keyboard.
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=cfg.ADMIN_PANEL_TEXT_BTN)]],
        resize_keyboard=True
    )


def all_polls_kb(buttons: {str: int}, admin: bool) -> InlineKeyboardMarkup:
    """
    Create a keyboard that contains all available polls for a user or admin.

    :param buttons: Dictionary of buttons that
    contains the name and ID of the poll.
    :param admin: True - create keyboard for admin.
    False - create admin for user.
    :return:
    """
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
    """
    Create a keyboard for admin to manage polls.

    :param is_active: True - create active polls keyboard.
                      False - create inactive polls keyboard.
    :return: Active or inactive polls keyboard.
    """
    if is_active:
        text = cfg.DEACTIVATE_TEXT_BTN
        cb_data = 'active'
    else:
        text = cfg.ACTIVATE_TEXT_BTN
        cb_data = 'not_active'

    kb_list = [
        [InlineKeyboardButton(text=cfg.DELETE_TEXT_BTN,
                              callback_data='poll_delete')],
        [InlineKeyboardButton(text=text,
                              callback_data='poll_activate')],
        [InlineKeyboardButton(text=cfg.GET_RESULTS_TEXT_BTN,
                              callback_data='get_poll_results')],
        [InlineKeyboardButton(text=cfg.POLL_BACK_TEXT_BTN,
                              callback_data=f'back_all_polls_{cb_data}')]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb_list)


def delete_poll_kb(poll_id: int) -> InlineKeyboardMarkup:
    """
    Create a poll deletion confirmation keyboard.

    :param poll_id: ID of the poll to be deleted.
    :return: Deletion confirmation keyboard.
    """
    kb_list = [
        [InlineKeyboardButton(text=cfg.DELETE_YES_TEXT_BTN,
                              callback_data='delete_poll_yes')],
        [InlineKeyboardButton(text=cfg.DELETE_NO_TEXT_BTN,
                              callback_data=f'poll_id_{poll_id}')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb_list)


def user_poll_kb() -> InlineKeyboardMarkup:
    """
    Create a keyboard action for the user.

    :return: Action for the user keyboard.
    """
    kb_list = [
        [InlineKeyboardButton(text=cfg.TAKE_POLL_TEXT_BTN,
                              callback_data='taking_poll')],
        [InlineKeyboardButton(text=cfg.POLL_BACK_TEXT_BTN,
                              callback_data='back_all_user_polls')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb_list)
