import os
import psycopg2 as pg
import psycopg2.errorcodes as er_code
from psycopg2.errors import lookup

DB_NAME = 'communist_bot'
DATABASE_URL = os.getenv('DATABASE_URL')
USER = os.getenv('DB_USERNAME')
PSW = os.getenv('DB_PASSWORD')


def add_user(user_id: int, username: str):
    try:
        _insert_query('users', id=user_id, username=username)
        return True
    except pg.IntegrityError as e:
        print(e)
        return False


def start_watching(watcher_id: int, target_id: int):
    res = 'Возникли непредвиденные ошибки в архиве.'
    try:
        _insert_query('surveillance', watcher_id=watcher_id, target_id=target_id)
        res = f'<@{watcher_id}> ведет наблюдение за <@{target_id}>'
    except lookup(er_code.CHECK_VIOLATION) as e:
        res = 'Следить за самим собой обязанность каждого Коммуниста.'
    except lookup(er_code.UNIQUE_VIOLATION) as e:
        res = f'<@{watcher_id}> уже ведет наблюдение за <@{target_id}>'
    except Exception as e:
        print(e)
    finally:
        return res


def stop_watching(watcher_id: int, target_id: int):
    if _get_query('surveillance', watcher_id=watcher_id, target_id=target_id):
        _delete_query('surveillance', watcher_id=watcher_id, target_id=target_id)
        return f'<@{watcher_id}> прекратил наблюдение за <@{target_id}>'
    return f'<@{watcher_id}> еще не ведет наблюдение за товарищем <@{target_id}>'


def is_watching(target_id):
    return len(_get_query('surveillance', target_id=target_id)) > 0


def _insert_query(table_name, **kwargs):
    with _get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f'''INSERT INTO {table_name}({_get_string(kwargs.keys())}) VALUES ({_get_s(len(kwargs))});''',
                tuple(kwargs.values()))
            conn.commit()


def _delete_query(table_name, **query):
    with _get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f'DELETE FROM {table_name} WHERE {_get_filter(query)};',
                tuple(query.values())
            )
            conn.commit()


def _get_query(table_name, *columns, **query):
    with _get_connection() as conn:
        with conn.cursor() as cursor:
            cols = _get_string(columns) if columns else '*'
            cursor.execute(
                f'SELECT {cols} FROM {table_name} WHERE {_get_filter(query)}',
                tuple(query.values()) if query else None
            )
            data = cursor.fetchall()
    return data


def _get_connection():
    if os.getenv('ENV') == 'HEROKU':
        return pg.connect(DATABASE_URL, sslmode='require')
    return pg.connect(database='communist_bot')


def _get_string(arr):
    res = ''
    for k in arr.__iter__():
        res += f'{k}, '
    return res[:-2]


def _get_s(amount: int):
    res = ''
    for i in range(amount):
        res += '%s, '
    return res[:-2]


def _get_filter(query: dict):
    if not query:
        return 'true'
    res = ''
    for i in query:
        res += f'{i}=%s and '
    return res[:-5]
