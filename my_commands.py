from aiogram import Bot, types

from aiogram.types import Message, URLInputFile, FSInputFile
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router


from extensions import *

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
                text="Еще бы!",
                callback_data="start_quiz")
                )
    photo = FSInputFile('Telegram_bot/tg_bot_2/images/intro_logo.jpg')
    await message.answer_photo(photo, reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Добро пожаловать в наш телеграм канал, тут тебя ждет увлекательная викторина в которой ты сможешь узнать свое тотемное животное! ')
    await message.answer(text='Начать прямо сейчас!', reply_markup=builder.as_markup())

@router.message(Command("quiz"))
async def cmd_start_quiz(message: Message):
    quiz.start_quiz()
    kb = [
        [types.KeyboardButton(text="Да")],
        [types.KeyboardButton(text="Нет")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer_sticker('CAACAgIAAxkBAAEDhiVlzla7_hs5cRJsqaI-xN7Bs1VyEAACBAEAAuSgzgeBAAHFZMLLBz00BA')
    await message.answer(
        text=quiz.questions[0],
        resize_keyboard=True,
        reply_markup=keyboard
    )

@router.message(Command("become_guardian"))
async def cmd_become_guardian(message: Message):
        _text: str = take_care
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
                text="Узнать больше", url=f"https://moscowzoo.ru/my-zoo/become-a-guardian/"
                ))
        builder.row(types.InlineKeyboardButton(
                text="Связаться с нашим специалистом",
                callback_data="contact_us")
                )
        await message.answer(text=_text, reply_markup=builder.as_markup())


@router.message(Command("share"))
async def cmd_share(message: Message):
    _result = quiz.get_result()
    builder1 = InlineKeyboardBuilder()
    builder1.add(types.InlineKeyboardButton(text="ВК", url=(Share().share_vk(_result))))
    builder1.add(types.InlineKeyboardButton(text="Twitter", url=(Share().share_twitter(_result))))
    builder1.add(types.InlineKeyboardButton(text="Facebook", url=(Share().share_facebook(_result))))
    await message.answer('     Поделиться результатом     ', reply_markup=builder1.as_markup())
    builder2 = InlineKeyboardBuilder()
    builder2.add(types.InlineKeyboardButton(text="Оставить отзыв", callback_data='feedback'))
    await message.answer('     Оставить небольшой анонимный отзыв     ', reply_markup=builder2.as_markup())

@router.message(Command("contact"))
async def cmd_contact_us(message: Message):
    bot = message.bot
    await bot.send_message(
        chat_id=os.environ.get('CONSTANT_USER_ID'), 
        text=f'Пользователь {message.chat.username} хочет узнать больше о программе опеки')
    _result = quiz.get_result()
    await bot.send_photo(chat_id=os.environ.get('CONSTANT_USER_ID'), photo=URLInputFile(_result.photo_path))
    await bot.send_message(chat_id=os.environ.get('CONSTANT_USER_ID'), text=f'Тотемное животное пользователя: {_result.name}!')
