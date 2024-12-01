from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, PollAnswer
from aiogram import Router, F
from create_bot import bot
from keyboards.kbs import main_kb, all_polls_kb, user_poll_kb
from db_handler.db_funk import (get_all_activity_polls, get_poll_by_id,
                                update_poll)
import utils.my_utils as ut
from aiogram.filters.state import StatesGroup, State


# User router for taking polls
user_router = Router()


class TakingPoll(StatesGroup):
    """

    """
    # Taking poll process state.
    process = State()


@user_router.message(CommandStart())
async def cmd_start_handler(message: Message) -> None:
    """
    Start command handler.
    :param message: Message sent by the user.
    """
    await message.answer(
        text='Привет! 👋 Я — бот для прохождения опросов.\n\n'
             'Твои ответы помогут собрать данные для исследований, улучшить '
             'продукты, контент и многое другое! Готов? Жми /take_poll и '
             'участвуй! 🚀',
        reply_markup=main_kb(message.from_user.id))


@user_router.message(Command('take_poll'))
async def take_poll_handler(message: Message, state: FSMContext) -> None:
    """
    Handler for user poll completion.
    Sends a keyboard with polls available for completion to the chat.

    :param message: Message sent by the user.
    :param state: Data that is in the storage.
    """
    try:
        data = await state.get_data()
        user_polls_kb_msg: Message = data['user_polls_kb_msg']
        await bot.delete_message(chat_id=user_polls_kb_msg.chat.id,
                                 message_id=user_polls_kb_msg.id)
    except Exception:
        pass
    polls = await get_all_activity_polls(is_active=True)
    if polls:
        poll_info = {}
        for poll in polls:
            poll_info[poll['name']] = int(poll['id'])
        # Change markup keyboard and sent new inline keyboard
        user_polls_kb_msg = await message.answer(
            text=f'Вам доступно {len(polls)} опросов',
            reply_markup=all_polls_kb(poll_info, False))
        await state.update_data(user_polls_kb_msg=user_polls_kb_msg)
    else:
        await message.answer('Нет активных опросов')


@user_router.callback_query(F.data.startswith('user_poll_id_'))
async def user_poll_handler(call: CallbackQuery, state: FSMContext) -> None:
    """
    Handler for the user selected poll.

    :param call: Response data from the selected poll button.
    :param state: Data that is in the storage.
    """
    poll_id: int = int(call.data.replace('user_poll_id_', ''))
    user_poll = await get_poll_by_id(poll_id)
    poll_info = f'{user_poll["name"]}\n\n{user_poll["description"]}'
    await call.message.edit_text(poll_info, reply_markup=user_poll_kb())
    await call.answer()
    await state.update_data(user_poll=user_poll)


@user_router.callback_query(F.data.startswith('back_all_user_polls'))
async def back_to_all_polls(call: CallbackQuery, state: FSMContext) -> None:
    """
    Handler button "Назад".
    Sends a keyboard with all available polls to the chat.

    :param call: Response data from button "Назад".
    :param state: Data that is in the storage.
    """
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await take_poll_handler(call.message, state)


@user_router.callback_query(F.data.startswith('taking_poll'))
async def taking_poll_handler(call: CallbackQuery, state: FSMContext) -> None:
    """
    Handler for the "Пройти опрос" button.
    Sends the first poll to the chat.

    :param call: Response data from button "Пройти опрос".
    :param state: Data that is in the storage.
    """
    user_poll = (await state.get_data())['user_poll']
    poll_index = 0
    questions = ut.string_to_list(user_poll['questions'])
    options = ut.string_to_nested_list_str(user_poll['options'])
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await state.set_state(TakingPoll.process)
    poll_mes = await call.message.answer_poll(question=questions[poll_index],
                                              options=options[poll_index],
                                              is_anonymous=False)
    await state.update_data(poll_index=poll_index)
    await state.update_data(poll_mes=poll_mes)
    await state.update_data(user_poll=user_poll)


@user_router.poll_answer(TakingPoll.process)
async def handle_poll_answer(poll_answer: PollAnswer,
                             state: FSMContext) -> None:
    """
    Handler of user answers to polls.
    Issues surveys one by one. Saves answers after all polls have been
    completed.

    :param poll_answer: Poll answer data.
    :param state: Data that is in the storage.
    """
    answers = poll_answer.option_ids
    poll_mes: Message = (await state.get_data())['poll_mes']
    poll_index = (await state.get_data())['poll_index']
    user_poll = (await state.get_data())['user_poll']
    questions = ut.string_to_list(user_poll['questions'])
    options = ut.string_to_nested_list_str(user_poll['options'])
    all_results = ut.string_to_nested_list_int(user_poll['results'])
    results = all_results[poll_index]
    for i in answers:
        results[i] += 1
    all_results[poll_index] = results
    user_poll['results'] = ut.nested_list_int_to_string(all_results)
    await state.update_data(user_poll=user_poll)
    try:
        poll_index += 1
        question = questions[poll_index]
        options = options[poll_index]
        await bot.delete_message(poll_mes.chat.id, poll_mes.message_id)
        poll_mes = await bot.send_poll(
            chat_id=poll_mes.chat.id,
            question=question,
            options=options,
            is_anonymous=False)
        await state.update_data(poll_mes=poll_mes)
        await state.update_data(poll_index=poll_index)
    except Exception:
        user_poll['respondents_number'] += user_poll['respondents_number']
        await update_poll(user_poll)
        await state.clear()
        await bot.send_message(chat_id=poll_mes.chat.id,
                               text='Опрос завершен!')
        await take_poll_handler(poll_mes, state)

