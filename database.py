import os
import ydb

from constants import QUIZ_FIELDS

YDB_ENDPOINT = os.getenv("YDB_ENDPOINT")
YDB_DATABASE = os.getenv("YDB_DATABASE")

def get_ydb_pool(ydb_endpoint, ydb_database, timeout=30):
    ydb_driver_config = ydb.DriverConfig(
        ydb_endpoint,
        ydb_database,
        credentials=ydb.credentials_from_env_variables(),
        root_certificates=ydb.load_ydb_root_certificate(),
    )

    ydb_driver = ydb.Driver(ydb_driver_config)
    ydb_driver.wait(fail_fast=True, timeout=timeout)
    return ydb.SessionPool(ydb_driver)


def _format_kwargs(kwargs):
    return {"${}".format(key): value for key, value in kwargs.items()}


# Заготовки из документации
# https://ydb.tech/en/docs/reference/ydb-sdk/example/python/#param-prepared-queries
def execute_update_query(pool, query, **kwargs):
    def callee(session):
        prepared_query = session.prepare(query)
        session.transaction(ydb.SerializableReadWrite()).execute(
            prepared_query, _format_kwargs(kwargs), commit_tx=True
        )

    return pool.retry_operation_sync(callee)


# Заготовки из документации
# https://ydb.tech/en/docs/reference/ydb-sdk/example/python/#param-prepared-queries
def execute_select_query(pool, query, **kwargs):
    def callee(session):
        prepared_query = session.prepare(query)
        result_sets = session.transaction(ydb.SerializableReadWrite()).execute(
            prepared_query, _format_kwargs(kwargs), commit_tx=True
        )
        return result_sets[0].rows

    return pool.retry_operation_sync(callee)   


async def get_quiz_questions():
    query = 'SELECT question FROM quiz_questions',

    result = execute_select_query(
        pool,
        query,
    )

    return result 


async def set_quiz_option(user_id, option, **kwargs):
    # option = feedback или animal

    

    if option == 'feedback':

        feed = kwargs.get('feed')
        stars = int(kwargs.get('stars'))

        query = f'''
        DECLARE $user_id AS Uint64;
        DECLARE $stars AS Int16;
        DECLARE $feed AS String;

        UPSERT INTO `quiz_state` (`user_id`, `feed`, `stars`)
        VALUES ($user_id, $feed, $stars);
        '''

        execute_update_query(
            pool,
            query,
            user_id=user_id,
            stars=stars,
            feedback=feed,
        )


    elif option == 'animal':

        animal = kwargs.get('animal')

        query = f'''
        DECLARE $user_id AS Uint64;
        DECLARE $animal AS String;

        UPSERT INTO `quiz_state` (`user_id`, `animal`)
        VALUES ($user_id, $animal);
        '''

        execute_update_query(
        pool,
        query,
        user_id=user_id,
        animal=animal,
    )


    else: return

async def get_quiz_option(user_id, field):

    if field not in QUIZ_FIELDS: return 'Invalid field'
    else:
        query = f'SELECT $field FROM quiz_state WHERE user_id = $user_id',

        result = execute_select_query(
            pool,
            query,
            user_id=user_id,
            field=field,
        )

        return result

# Зададим настройки базы данных 
pool = get_ydb_pool(YDB_ENDPOINT, YDB_DATABASE)
