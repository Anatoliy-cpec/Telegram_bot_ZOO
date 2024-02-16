
    # //////////ОПИСАНИЕ//////////

    # CONSTANT_USER_ID - айди юзера которому будет отправлено сообщение если пользователь захочет
    #                 узнать больше о программе опеки
    # TOKEN - токен бота тг
    # AVAILABLE_STARS - массив доступных оценок
    # questions- массив вопросов задаваемых в ходе викторины
    # animals - массив животных которые выведутся в результате
    # quiz - экцемпляр квиза из которого бот берет нужные методы и данные

    # Database() - сласс базы данных, я использовал Mongo тк только с ней не возникло проблем




import requests
import json
import os
from typing import Any
from dotenv import load_dotenv

from send_feedback import Database

# подгружаю виртуальное окружение 
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# подгружаю из виртуального окружения свой id, он нужен для отправки сообщения в личку 
CONSTANT_USER_ID = os.environ.get('CONSTANT_USER_ID')
AVAILABLE_STARS = ['1','2','3','4','5','6','7','8','9','10']

# создаю свои исключения
class MyException(Exception):
    def __str__(self):
        return 'User exception'

class ServerTimeout(MyException):
    def __str__(self):
        return 'Сервер отверг запрос на подключение, проверьте права доступа пользователя к базе данных и список допустимых ip адресов'
    
class UnComplited(MyException):
    def __str__(self):
        return 'Невозможно выполнить это действие тк викторина не завершена!'

class QuizInProgress(MyException):
    def __str__(self):
        return 'Неизвестная команда, используйте кнопки!'
    

# класс для хранения информации о животном: имя, url фото, url информации с сайта зоопарка 
class Animal():
    def __init__(self, name: str, photo_path: str, animal_info_url: str):
        self.name: str = name
        self.photo_path: str = photo_path
        self.animal_info_url: str = animal_info_url

# класс взаимодействия с пользователем
class Socials():
    
    # метод фидбека
    @staticmethod
    def feedback(feedback: dict):
        # если соединение с базой прошло успешно то добавляем отзыв
        # оно будет успешно только если ip разрешен в базе
        try:
            __db = Database()
            if __db.client is None:
                raise ServerTimeout
            else:
                __db.connect_to_DB()
        except Exception as e:
            with open('Telegram_bot/tg_bot_2/files/log.log', 'a', encoding='utf-8') as file:
                    file.write(str(e))
        else:
            __db.send_to_DB(feedback)

    

#  Класс в котором содержатся статические методы ссылок чтобы поделиться
#  я использовал ссылки тк не каждый пользователь захочет вводить в боте свои данные от аккаунта
#  а api именно это и просят, лучше если данные будут введены в браузере на стороне пользователя
class Share():

    @staticmethod
    def share_vk(result: Animal) -> str:
        return f'http://vk.com/share.php?url=https://t.me/super_337_bot&title=Мое тотемное животное: {result.name}, узнай и ты свое по ссылке ниже&description={result.name}&image={result.photo_path}&noparse=true'
    @staticmethod
    def share_facebook(result: Animal) -> str:
        return f'https://www.facebook.com/sharer/sharer.php?u=https://t.me/super_337_bot&picture={result.photo_path}'
    @staticmethod
    def share_twitter(result: Animal) -> str:
        return f'https://twitter.com/share?url=https://t.me/super_337_bot&text=Мое тотемное животное: {result.name}, узнай и ты свое по ссылке ниже'




# основной класс викторины с основными модулями
class Quiz():
    def __init__(self):
        self.questions: list[str] = []
        self.animals: list[Animal] = {}
        self.question_answers: dict = Any
        self.question_counter: int = 0
        self.quiz_is_active: bool = False
        self.quiz_complited: bool = False
        self.feedback_is_active: bool = False
        self.quiz_result: 'Animal' = Any
    
    def set_questions(self, questions: list[str]):
        self.questions = questions
        
    
    
    def set_animals(self, animals: list[Animal]):
        self.animals = animals

    def start_quiz(self):
        self.question_counter = 0
        self.quiz_is_active = True
        self.quiz_complited = False
        self.quiz_result: 'Animal' = Any
        self.question_answers: dict = {}

    def is_not_over(self) -> bool:
        if self.question_counter == len(self.questions):
            self.quiz_is_active = False
            self.quiz_complited = True
            return False
        else:
            return True

    def calculate_result(self):

        # подсчет ответов да для разных вариантов зверей, в случае варианта в котором все ответы 
        # = да: всегда выдает последний элемент.
        # когда все элементы = нет: всегда выдается первый элемент.
        # в случае когда ответ не совпадает ни с одним вариантом выдает(в моем случае) последний 
        # элемент. 
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # На мой взгляд такая грамоздкая система подсчета здесь справедлива тк в викторине не должно
        # быть много вопросов.
        # Так же вместо "1":"да\нет" можно было бы как минимум использовать массив 1\0 но 
        # но мне кажется что так проще

        if all([
                self.question_answers[1] == 'нет', self.question_answers[2] == 'да', self.question_answers[3] == 'да',
                self.question_answers[4] == 'нет', self.question_answers[5] == 'нет'
            ]):
            print(1)
            self.quiz_result = animals[2]
        elif all([
                self.question_answers[1] == 'нет', self.question_answers[2] == 'нет', self.question_answers[3] == 'да',
                self.question_answers[4] == 'нет', self.question_answers[5] == 'да'
            ]):
            self.quiz_result = animals[1]
            print(2)
        elif all([
                self.question_answers[1] == 'да', self.question_answers[2] == 'нет', self.question_answers[3] == 'да',
                self.question_answers[4] == 'да', self.question_answers[5] == 'нет'
            ]):
            print(3)
            self.quiz_result = animals[0]
        elif all([
                self.question_answers[1] == 'да', self.question_answers[2] == 'да', self.question_answers[3] == 'да',
                self.question_answers[4] == 'да', self.question_answers[5] == 'да'
            ]):
            print(4)
            self.quiz_result = animals[len(animals)-1]
        elif all([
                self.question_answers[1] == 'нет', self.question_answers[2] == 'нет', self.question_answers[3] == 'нет',
                self.question_answers[4] == 'нет', self.question_answers[5] == 'нет'
            ]):
            print(5)
            self.quiz_result = animals[0]
        else:
            print(6)
            self.quiz_result = animals[3]
        


    def get_result(self) -> Animal:
        return self.quiz_result

    def process_answer_data(self, answer: str):
        self.question_answers[self.question_counter+1] = answer
        self.question_counter += 1


    def process_answer(self, text: str):
        if text.lower() == 'да':
            self.process_answer_data(text.lower())
        elif text.lower() == 'нет':
            self.process_answer_data(text.lower())
        else:
            pass

take_care: str = '''Стать опекуном
Участие в программе «Возьми животное под опеку» — это ваш личный вклад в дело сохранения биоразнообразия Земли и развитие нашего зоопарка.
Основная задача Московского зоопарка с самого начала его существования это — сохранение биоразнообразия нашей планеты. Когда вы берете под опеку животное, вы помогаете нам в этом благородном деле.
При нынешних темпах развития цивилизации к 2050 году с лица Земли могут исчезнуть около 10 000 биологических видов. Московский зоопарк вместе с другими зоопарками мира делает все возможное, чтобы сохранить их.
Опека — это прекрасная возможность принять участие в деле сохранения редких видов, помочь нам в реализации природоохранных программ.
'''

# для простоты записал эти данные в переменные, а вобще нужно подгружать их из mongo

questions: list[str] = [
    'Вы наверно белый и очень пушистый?',
    'Вы больше любите находиться в стае?',
    'С вашей шерстью холода вам нипочём?',
    'Вы любите овощи?',
    'Вы любите цитаты Стетхема?',
]

animals: list['Animal'] = [
    Animal('Заяц беляк',
            'http://petnaobed.ru/wp-content/uploads/2020/12/575d36825dada.jpeg',
            'https://moscowzoo.ru/animals/zaytseobraznye/zayats-belyak/'),
    Animal('Волк',
            'https://gas-kvas.com/grafic/uploads/posts/2023-09/1695815771_gas-kvas-com-p-kartinki-volk-8.jpg',
            'https://moscowzoo.ru/animals/khishchnye/volk/'),
    Animal('Амурский тигр',
            'https://img.goodfon.ru/wallpaper/nbig/9/dc/tigr-amurskiy-koshka-morda-507.jpg',
            'https://moscowzoo.ru/animals/khishchnye/amurskiy-tigr/'),
    Animal('Медоед',
            'https://pic.rutubelist.ru/video/7e/fb/7efb4c98e11b0d266adcd921e92f1614.jpg',
            'https://moscowzoo.ru/animals/khishchnye/medoed/'),

]

quiz = Quiz()
quiz.set_questions(questions)
quiz.set_animals(animals)

if __name__ == "__main__":
    print('/////////////////////////-------//////////////////////')