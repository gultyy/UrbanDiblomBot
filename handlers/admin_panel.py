from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, Poll, FSInputFile
from create_bot import admins, bot
from keyboards.kbs import (admin_kb, save_poll_kb, main_kb, all_polls_kb, poll_manage_kb, all_polls_menu_kb,
                           delete_poll_kb)
from keyboards.kbs_cfg import *
from aiogram.filters.state import State, StatesGroup
from typing import List, Dict
from db_handler.db_funk import *
from utils.my_utils import *

#Admin router for poll management
admin_router = Router()

class CreatePoll(StatesGroup):
    name = State()
    description = State()
    type = State()
    polls = State()



@admin_router.message((F.text.endswith(MAIN_MENU_TEXT_BTN)) & (F.from_user.id.in_(admins)))
async def main_menu(message: Message):
    await message.answer('Главное меню', reply_markup=main_kb(message.from_user.id))

@admin_router.message((F.text.endswith(ADMIN_PANEL_TEXT_BTN) | F.text.endswith(POLL_BACK_TEXT_BTN)) &
                      F.from_user.id.in_(admins))
async def admin_panel(message: Message, state: FSMContext):
    try:
        polls_menu_msg: Message = (await state.get_data())['polls_menu_msg']
        polls_kb_msg: Message = (await state.get_data())['polls_kb_msg']
        await bot.delete_message(polls_menu_msg.chat.id, polls_menu_msg.message_id)
        await bot.delete_message(polls_kb_msg.chat.id, polls_kb_msg.message_id)
    except:
        pass
    await message.answer('Панель управления опросами', reply_markup=admin_kb())


# admin kb handlers
@admin_router.message((F.text.endswith(ACTIVE_PALLS_TEXT_BTN) | F.text.endswith(NOT_ACTIVE_PALLS_TEXT_BTN)) &
                      F.from_user.id.in_(admins))
async def active_polls(message: Message, state: FSMContext):
    if message.text.endswith(ACTIVE_PALLS_TEXT_BTN):
        is_active = True
        active_text = 'Активные'
        active_text_if_not = 'активных'
    else:
        is_active = False
        active_text = 'Неактивные'
        active_text_if_not = 'неактивных'
    polls = await get_all_activity_polls(is_active=is_active)
    if polls:
        poll_info: Dict[str: int]= {}
        for poll in polls:
            poll_info[poll['name']] = int(poll['id'])
        # Change markup keyboard and sent new inline keyboard
        polls_menu_msg = await message.answer(f'{active_text} опросы', reply_markup=all_polls_menu_kb())
        polls_kb_msg = await message.answer(f'Количество: {len(polls)}',
                                            reply_markup=all_polls_kb(poll_info,True))
        await state.update_data(polls_menu_msg=polls_menu_msg)
        await state.update_data(polls_kb_msg=polls_kb_msg)
    else:
        await message.answer(f'Нет {active_text_if_not} опросов', reply_markup=admin_kb())

@admin_router.message((F.text.endswith(CREATE_POLL_TEXT_BTN)) & (F.from_user.id.in_(admins)))
async def create_poll(message: Message, state: FSMContext):
    await message.answer('Введите имя опроса')
    await state.set_state(CreatePoll.name)


# Create Poll FSM handlers
@admin_router.message(F.text, CreatePoll.name)
async def capture_poll_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите описание опроса:')
    await state.set_state(CreatePoll.description)

@admin_router.message(F.text, CreatePoll.description)
async def capture_poll_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Создайте опрос и отправьте:')
    await state.set_state(CreatePoll.polls)
    polls: List[Poll] = []
    await state.update_data(polls=polls)

@admin_router.message(F.poll, CreatePoll.polls)
async def capture_polls(message: Message, state: FSMContext):
    poll = message.poll
    data = await state.get_data()
    polls : List[Poll] = data['polls']
    polls.append(poll)
    await state.update_data(polls=polls)
    await message.answer('Добавьте следующий опрос или сохраните', reply_markup=save_poll_kb())


@admin_router.message(F.text.endswith(SAVE_TEXT_BTN), CreatePoll.polls)
async def save_poll(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f'Имя опроса: {data['name']}')
    await message.answer(f'Описание опроса: {data['description']}')

    questions = []
    options = []
    results = []

    for poll in data['polls']:
        questions.append(poll.question)
        options.append([option.text for option in poll.options])
        results.append([0] * len(poll.options))
        await message.answer_poll(question=poll.question, options=[option.text for option in poll.options])
    await state.clear()

    new_poll = {'name': data['name'],
                'description': data['description'],
                'type': 'No type',
                'is_active':False,
                'questions': list_str_to_string(questions),
                'options': nested_list_str_to_string(options),
                'results': nested_list_int_to_string(results),
                'respondents_number': 0
                }
    await insert_poll(new_poll)
    await message.answer('Опрос сохранен', reply_markup=admin_kb())


# all polls handlers
@admin_router.callback_query(F.data.startswith('poll_id_') & F.from_user.id.in_(admins))
async def poll_manage__handler(call: CallbackQuery, state: FSMContext):
    poll_id: int = int(call.data.replace('poll_id_', ''))
    poll = await get_poll_by_id(poll_id)
    is_active = poll['is_active']
    poll_info = f'{poll["name"]}\n\n{poll["description"]}\n\nТип опроса:{poll["type"]}'
    await call.message.edit_text(poll_info, reply_markup=poll_manage_kb(is_active))
    await call.answer()
    await state.update_data(current_poll_id=poll_id)
    await state.update_data(polls_activity=is_active)


@admin_router.callback_query(F.data.endswith('poll_delete') & F.from_user.id.in_(admins))
async def poll_manage__handler(call: CallbackQuery, state: FSMContext):
    poll_id = (await state.get_data())['current_poll_id']
    await call.message.edit_text('Вы действительно хотите удалить опрос?', reply_markup=delete_poll_kb(poll_id))
    await call.answer()


async def return_all_polls(is_active: bool, call: CallbackQuery,state: FSMContext):
    polls = await get_all_activity_polls(is_active=is_active)
    if polls:
        poll_info: Dict[str: int] = {}
        for poll in polls:
            poll_info[poll['name']] = int(poll['id'])
        await call.message.edit_text(f'Количество: {len(polls)}',
                                     reply_markup=all_polls_kb(poll_info, True))
    else:
        if is_active:
            active_text = 'активных'
        else:
            active_text = 'неактивных'
        try:
            polls_menu_msg: Message = (await state.get_data())['polls_menu_msg']
            polls_kb_msg: Message = (await state.get_data())['polls_kb_msg']
            await bot.delete_message(polls_menu_msg.chat.id, polls_menu_msg.message_id)
            await bot.delete_message(polls_kb_msg.chat.id, polls_kb_msg.message_id)
        except:
            pass
        await bot.send_message(call.message.chat.id, text=f'Нет {active_text} опросов', reply_markup=admin_kb())
    await call.answer()


@admin_router.callback_query(F.data.endswith('delete_poll_yes') & F.from_user.id.in_(admins))
async def poll_manage__handler(call: CallbackQuery, state: FSMContext):
    poll_id = (await state.get_data())['current_poll_id']
    poll = await get_poll_by_id(poll_id)
    await delete_poll_by_id(poll_id)
    await call.answer(text=f'Опрос {poll['name']} удален', show_alert=True)
    is_active = (await state.get_data())['polls_activity']
    await return_all_polls(is_active, call, state)


@admin_router.callback_query((F.data.endswith('poll_activate') | F.data.endswith('poll_deactivate')) &
                             F.from_user.id.in_(admins))
async def poll_manage__handler(call: CallbackQuery, state: FSMContext):
    poll_id = (await state.get_data())['current_poll_id']
    poll = await get_poll_by_id(poll_id)
    is_active = not poll['is_active']
    poll['is_active'] = is_active
    await update_poll(poll)
    if is_active:
        text = 'активирован'
    else:
        text = 'деактивирован'
    await call.answer(text=f'Опрос {poll['name']} {text}', show_alert=True)
    poll_info = f'{poll["name"]}\n\n{poll["description"]}\n\nТип опроса:{poll["type"]}'
    await call.message.edit_text(poll_info, reply_markup=poll_manage_kb(poll['is_active']))

@admin_router.callback_query(F.data.startswith('get_poll_results') & F.from_user.id.in_(admins))
async def poll_manage__handler(call: CallbackQuery, state: FSMContext):
    poll_id = (await state.get_data())['current_poll_id']
    poll = await get_poll_by_id(poll_id)
    filename = create_result_tbl(poll)
    f = FSInputFile('.results/Тест.xlsx')
    await call.message.answer_document(f)
    delete_result_tbl(filename)
    await call.answer()

@admin_router.callback_query(F.data.startswith('back_all_polls_') & F.from_user.id.in_(admins))
async def poll_manage__handler(call: CallbackQuery, state: FSMContext):
    is_active = (await state.get_data())['polls_activity']
    await return_all_polls(is_active, call, state)


