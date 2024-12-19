Бот telegram на основе aiogram и yandex.cloud serverless.
Бот работает с переменными окружения в консоли яндекс клауд.

CONSTANT_USER_ID - айди пользователя в тг, ему будет отсылаться результат квиза и никнейм пользователя.
YDB_ENDPOINT, YDB_DATABASE - данные консоли яндекса, нужны для подключения к базе данных
API_TOKEN - токен вашего бота, тот который выдает BotFather

Плюсы такого подхода в том что можно протестировать работу и нагрузку на бота, а если поток увеличится всегда можно докупить нужные ресурсы. В яндекс облаке ты платишь по факту за пропускную способность а не за время работы, поэтому начальных ресурсов с лихвой должно хватить для того чтобы протестировать своего бота.

Инструкция:

Шаг 1

    Перейдите в панель управления Yandex Cloud.
    При отсутствии учетной записи выберите опцию "Подключение" или "Консоль".
    Пройдите авторизацию или регистрацию в системе Яндекс ID.

Шаг 2

    Создайте платежный аккаунт в панели управления.
    Подтвердите его банковской картой.
    На данном этапе платежи не требуются; они будут необходимы лишь при увеличении нагрузки.

Шаг 3

    Сформируйте новый каталог для вашего проекта.
    Присвойте ему произвольное название.

Шаг 4

    Внутри каталога создайте сервисный аккаунт.
    Предоставьте аккаунту роли "editor" и "serverless.functions.invoker".

Шаг 5

    Создайте API-шлюз внутри каталога.
    Укажите имя шлюза и оставьте стандартные настройки.

Шаг 6

    Разработайте новую облачную функцию (Cloud Function).
    Сохраните ее под выбранным именем.
    Определите среду исполнения как Python 3.11.
    Сохраните текущую версию с использованием настроек по умолчанию.

Шаг 7

    Обеспечьте публичный доступ к созданной функции.
    Скопируйте уникальный идентификатор функции.

Шаг 8

    Осуществите привязку шлюза к функции.
    Добавьте соответствующий код в конец спецификации шлюза, используя ранее скопированный идентификатор.

Шаг 9

    Зарегистрируйте Telegram-бота через @BotFather.

Шаг 10

    Установите соединение между ботом и функцией посредством API-шлюза.
    Применяйте URL-адрес с уникальным токеном и служебным доменом шлюза.
    https://api.telegram.org/bot<API_TOKEN>/setWebhook?url=<URL_API_GATEWAY>/<ROUTE>

    Где:

        <API_TOKEN> - Ваш токен бота
        <URL_API_GATEWAY> - Служебный домен с вкладки Обзор вашего API шлюза
        <ROUTE> (в нашем случае bot-api)

Шаг 11

    Организуйте базу данных YDB.
    Укажите название базы данных и используйте настройки по умолчанию.

Шаг 12

    Создайте таблицу 
    quiz_state с полями user_id: Uint64, stars: Int16, animal: String, feedback: String
    quiz_questions с полями id: Uint64, question: String

Шаг 13

    Откройте функцию и импортируйте архив с кодом в формате ZIP.
    Укажите точку входа: (В моем случае это main.webhook. Читайте справку про точку входа для точного описания )
    Настройте необходимые параметры и переменные окружения.
    Завершите процесс нажатием кнопки "Сохранить".

Если всё сделанно правильно то при команде /start бот будет выполнять свой функционал