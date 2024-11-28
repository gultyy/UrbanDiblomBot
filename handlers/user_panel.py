from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, PollAnswer
from aiogram import Router, F
from create_bot import bot
from keyboards.kbs import main_kb, all_polls_kb, user_poll_kb
from db_handler.db_funk import *
from utils.my_utils import *
from aiogram.filters.state import StatesGroup, State

user_router = Router()

class TakingPoll(StatesGroup):
    process = State()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Я бот опросов ... тратата. Чтобы пройти опрос введите команду /take_poll',
                         reply_markup=main_kb(
        message.from_user.id))

@user_router.message(Command('take_poll'))
async def take_poll_handler(message: Message, state: FSMContext):
    try:
        user_polls_kb_msg: Message = (await state.get_data())['user_polls_kb_msg']
        await bot.delete_message(chat_id=user_polls_kb_msg.chat.id, message_id=user_polls_kb_msg.id)
    except:
        pass
    polls = await get_all_activity_polls(is_active=True)
    if polls:
        poll_info: Dict[str: int] = {}
        for poll in polls:
            poll_info[poll['name']] = int(poll['id'])
        # Change markup keyboard and sent new inline keyboard
        user_polls_kb_msg = await message.answer(f'Вам доступно {len(polls)} опросов', reply_markup=all_polls_kb(
            poll_info, False))
        await state.update_data(user_polls_kb_msg=user_polls_kb_msg)
    else:
        await message.answer(f'Нет активных опросов')


@user_router.callback_query(F.data.startswith('user_poll_id_'))
async def user_poll_handler(call: CallbackQuery, state: FSMContext):
    poll_id: int = int(call.data.replace('user_poll_id_', ''))
    user_poll = await get_poll_by_id(poll_id)
    poll_info = f'{user_poll["name"]}\n\n{user_poll["description"]}'
    await call.message.edit_text(poll_info, reply_markup=user_poll_kb())
    await call.answer()
    await state.update_data(user_poll=user_poll)


@user_router.callback_query(F.data.startswith('back_all_user_polls'))
async def back_to_all_polls(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await take_poll_handler(call.message, state)


@user_router.callback_query(F.data.startswith('taking_poll'))
async def taking_poll_handler(call: CallbackQuery, state: FSMContext):
    user_poll = (await state.get_data())['user_poll']
    poll_index = 0
    questions = string_to_list(user_poll['questions'])
    options = string_to_nested_list_str(user_poll['options'])
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await state.set_state(TakingPoll.process)
    poll_mes = await call.message.answer_poll(question=questions[poll_index], options=options[poll_index],
                                               is_anonymous=False)
    await state.update_data(poll_index=poll_index)
    await state.update_data(poll_mes=poll_mes)
    await state.update_data(user_poll=user_poll)

@user_router.poll_answer(TakingPoll.process)
async def handle_poll_answer(poll_answer: PollAnswer, state: FSMContext):
    answers: List[int] = poll_answer.option_ids
    print(answers)
    poll_mes: Message = (await state.get_data())['poll_mes']
    poll_index = (await state.get_data())['poll_index']
    user_poll = (await state.get_data())['user_poll']
    questions = string_to_list(user_poll['questions'])
    options = string_to_nested_list_str(user_poll['options'])
    print(user_poll['results'])
    all_results: List[List]= string_to_nested_list_int(user_poll['results'])
    results = all_results[poll_index]
    for i in answers:
        results[i] += 1
    all_results[poll_index] = results
    user_poll['results'] = nested_list_int_to_string(all_results)
    await state.update_data(user_poll=user_poll)
    try:
        poll_index += 1
        question = questions[poll_index]
        options = options[poll_index]
        await bot.delete_message(poll_mes.chat.id, poll_mes.message_id)
        poll_mes = await bot.send_poll(chat_id=poll_mes.chat.id, question=question, options=options,
                                   is_anonymous=False)
        await state.update_data(poll_mes=poll_mes)
        await state.update_data(poll_index=poll_index)
    except:
        await update_poll(user_poll)
        await state.clear()
        await bot.send_message(chat_id=poll_mes.chat.id, text='Опрос завершен!')
        await take_poll_handler(poll_mes, state)



