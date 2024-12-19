from aiogram import types
from aiogram import Router, F

from extensions import *
from my_commands import *

router = Router()



@router.callback_query(F.data)
async def data_handler(callback: types.CallbackQuery):
    try:
        if not quiz.quiz_is_active:
            if callback.data.lower() == 'feedback':
                await callback.message.answer('введите /feedback чтобы начать')
            if callback.data.lower() == 'become_guardian':
                await cmd_become_guardian(callback.message)
            if callback.data.lower() == 'start_quiz':
                await cmd_start_quiz(callback.message)
            if callback.data.lower() == 'contact_us':
                if quiz.quiz_complited:
                    await cmd_contact_us(callback.message)
                else:
                    raise UnComplited
        else:
            raise UnComplited
    except Exception as e:
        await callback.message.answer(str(e))

