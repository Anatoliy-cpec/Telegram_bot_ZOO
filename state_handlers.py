from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from extensions import *

router = Router()  # [1]

class Feedback(StatesGroup):
    stars_count = State()
    feedback_text = State()



@router.message(Command("feedback"))
async def cmd_feedback(message: Message, state: FSMContext):
    if not quiz.quiz_is_active:
        quiz.feedback_is_active = True
        await message.answer(text="Как вы оцениваете викторину: от 1 до 10?")
        await state.set_state(Feedback.stars_count)
    else:
        await message.answer(text="Сначала закончите опрос!")

@router.message(Feedback.stars_count, F.text.in_(AVAILABLE_STARS))
async def stars_chosen(message: Message, state: FSMContext):
    await state.update_data(stars=message.text.lower())
    await message.answer(
        text="А теперь пара слов о викторине, опишите что бы вы хотели улучшить (можно оставить пустым)")
    await state.set_state(Feedback.feedback_text)

@router.message(Feedback.stars_count)
async def stars_chosen_incorrectly(message: Message):
    await message.answer(
        text="Введите число от 1 до 10"
    )

@router.message(Feedback.feedback_text, F.text)
async def feedback_complited(message: Message, state: FSMContext):
    quiz.feedback_is_active = False
    await message.answer(
        'Благодарим вас за ваш отзыв, ваше мнение очень важно для нас!'
    )
    await state.update_data(feedback=message.text.lower())
    user_data = await state.get_data()
    user_id = message.from_user.id
    Socials.feedback(user_data, user_id)
    await state.clear()

                