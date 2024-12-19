from aiogram import types

from aiogram.types import Message, URLInputFile, FSInputFile
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F

from extensions import *
from my_commands import cmd_share
from database import set_quiz_option, get_quiz_option

router = Router()

@router.message(F.text)
async def text_handler(message: Message):
    try:
        if not quiz.quiz_is_active:
            await message.answer('Заблудились? введите /start чтобы начать сначала')
        else:
            if message.text.lower() in ['да','нет']:
                await quiz_handler(message)
            else:
                raise QuizInProgress
    except Exception as e:
        await message.answer(str(e))


@router.message(F.text)
async def quiz_handler(message: Message):
    if quiz.quiz_is_active:
        quiz.process_answer(message.text)
        if quiz.is_not_over():
            await message.answer(quiz.questions[quiz.question_counter])
        else:
            await message.answer('Ждем результат', reply_markup=types.ReplyKeyboardRemove())
            await message.answer_sticker('CAACAgIAAxkBAAEDbotlybW4b8GWJnAbWjlhY4NcRkMdOgAC_wAD9wLIDz7Q9EOOrMfoNAQ')
            quiz.calculate_result()
            _result = quiz.get_result()

            await message.answer('start')
            await set_quiz_option(user_id=message.from_user.id, option='animal', animal=_result.name)
            await message.answer('end')
            
            builder1 = InlineKeyboardBuilder()
            builder2 = InlineKeyboardBuilder()
            await message.answer_photo(URLInputFile(_result.photo_path))
            await message.answer(f'       Ваше тотемное животное: {_result.name}!       ')
            await cmd_share(message)
            builder1.row(types.InlineKeyboardButton(
                text="Узнать", url=_result.animal_info_url)
                )
            await message.answer('    Вы можете узнать о нем больше на нашем сайте    ', reply_markup=builder1.as_markup())
            builder2.add(types.InlineKeyboardButton(
                text="Подружиться",
                callback_data="become_guardian")
                )
            builder2.add(types.InlineKeyboardButton(
                text="Попробовать снова",
                callback_data="start_quiz")
                )
            await message.answer('А как насчет подружиться с одним таким? Или попробовать еще раз?', reply_markup=builder2.as_markup())
